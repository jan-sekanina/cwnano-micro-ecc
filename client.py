from typing import Union, List

from pyecsca.sca.target import SimpleSerialTarget, ChipWhispererTarget, BinaryTarget, SimpleSerialMessage as SMessage
import chipwhisperer as cw
from chipwhisperer.capture.targets.SimpleSerial import SimpleSerial
from chipwhisperer.capture.api.programmers import STM32FProgrammer


class TargetBase(SimpleSerialTarget):
    timeout: int = 1000

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
        pubkey_data = resp["w"].data
        pubkey_len = len(pubkey_data)
        x = int(pubkey_data[:pubkey_len // 2], 16)
        y = int(pubkey_data[pubkey_len // 2:], 16)
        return x, y

    def sign(self, hash: bytes):
        """Sign a message hash, needs to be 32 bytes, get `r` and `s` signature components."""
        if len(hash) != 32:
            raise ValueError("Hash needs to be 256-bits (32 bytes) long.")
        cmd = "s" + hash.hex()
        resp = self.send_cmd(SMessage.from_raw(cmd), self.timeout)
        sig_data = resp["s"].data
        sig_len = len(sig_data)
        r = int(sig_data[:sig_len // 2], 16)
        s = int(sig_data[sig_len // 2:], 16)
        return r, s


class DeviceTarget(TargetBase, ChipWhispererTarget):

    def __init__(self):
        scope = cw.scope()
        scope.default_setup()
        target = SimpleSerial()
        programmer = STM32FProgrammer
        super().__init__(target, scope, programmer)


class HostTarget(TargetBase, BinaryTarget):

    def __init__(self, binary: Union[str, List[str]], debug_output: bool = False):
        super().__init__(binary, debug_output)
