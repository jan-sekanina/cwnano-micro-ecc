from hashlib import sha1
from typing import Union, List

from abc import ABC

from ecdsa import VerifyingKey, NIST192p
from ecdsa.ellipticcurve import Point
from ecdsa.util import sigdecode_strings
from pyecsca.sca.target import SimpleSerialTarget, ChipWhispererTarget, BinaryTarget, SimpleSerialMessage as SMessage
import chipwhisperer as cw
from chipwhisperer.capture.targets.SimpleSerial import SimpleSerial
from chipwhisperer.capture.api.programmers import STM32FProgrammer


class TargetBase(SimpleSerialTarget, ABC):
    timeout: int = 2000

    def init_prng(self, seed: bytes) -> None:
        """Initialize the PRNG with a 4-byte seed."""
        cmd = "i" + seed.hex()
        self.send_cmd(SMessage.from_raw(cmd), self.timeout)

    def generate_keypair(self):
        """Generate a keypair."""
        cmd = "g"
        self.send_cmd(SMessage.from_raw(cmd), self.timeout)

    def export(self):
        """Export the public key, get `x` and `y` coordinates."""
        cmd = "e"
        resp = self.send_cmd(SMessage.from_raw(cmd), self.timeout)
        x_data = resp["x"].data
        y_data = resp["y"].data
        x = int(x_data, 16)
        y = int(y_data, 16)
        return x, y

    def sign(self, hash: bytes):
        """Sign a message hash, needs to be 20 bytes, get `r` and `s` signature components."""
        if len(hash) != 20:
            raise ValueError("Hash needs to be 160-bits (20 bytes) long.")
        cmd = "s" + hash.hex()
        resp = self.send_cmd(SMessage.from_raw(cmd), self.timeout)
        r_data = resp["r"].data
        s_data = resp["s"].data
        r = int(r_data, 16)
        s = int(s_data, 16)
        return r, s

    def halt(self):
        """Halt the execution of the target."""
        self.write(b"x\n")


class DeviceTarget(TargetBase, ChipWhispererTarget):
    """A device target, one of ChipWhisperer-Nano or CW308 with the STM32F0/STM32F3 boards."""

    def __init__(self):
        scope = cw.scope()
        scope.default_setup()
        target = SimpleSerial()
        programmer = STM32FProgrammer
        super().__init__(target, scope, programmer)


class HostTarget(TargetBase, BinaryTarget):
    """A host target, runs the binary directly and interacts via stdin/stdout."""

    def __init__(self, binary: Union[str, List[str]], debug_output: bool = False):
        super().__init__(binary, debug_output)


def verify_signature(pubkey, signature, hash):
    """Verify the signature, of the hash, made by the pubkey. Assumes secp192r1 curve."""
    vk = VerifyingKey.from_public_point(Point(NIST192p.curve, pubkey[0], pubkey[1]), curve=NIST192p, hashfunc=sha1)
    r, s = signature
    signature = (r.to_bytes(vk.curve.baselen, byteorder="big"), s.to_bytes(vk.curve.baselen, byteorder="big"))
    return vk.verify_digest(signature, hash, sigdecode=sigdecode_strings)
