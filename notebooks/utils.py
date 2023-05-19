from hashlib import sha1
from typing import Tuple

from ecdsa import VerifyingKey, NIST192p
from ecdsa.ellipticcurve import Point
from ecdsa.util import sigdecode_strings


def verify_signature(pubkey: Tuple[int, int], signature: Tuple[int, int], hash: bytes) -> bool:
    """Verify the signature, of the hash, made by the pubkey. Assumes secp192r1 curve."""
    vk = VerifyingKey.from_public_point(Point(NIST192p.curve, pubkey[0], pubkey[1]), curve=NIST192p, hashfunc=sha1)
    r, s = signature
    signature = (r.to_bytes(vk.curve.baselen, byteorder="big"), s.to_bytes(vk.curve.baselen, byteorder="big"))
    return vk.verify_digest(signature, hash, sigdecode=sigdecode_strings)


class xorshift32:
    """Simple xorshift32 implementation, same as in the target."""
    state: int

    def __init__(self, seed: int):
        if seed.bit_length() > 32:
            raise ValueError("Seed is 32-bits max.")
        self.state = seed

    def next(self) -> int:
        """Advance and return one int."""
        self.state ^= (self.state << 13) & 0xffffffff
        self.state ^= (self.state >> 17) & 0xffffffff
        self.state ^= (self.state << 5) & 0xffffffff
        return self.state

    def next_bytes(self, amount: int) -> bytes:
        """Get `amount` bytes."""
        res = bytearray(amount)
        for i in range((amount + 3) // 4):
            rand = self.next()
            for j in range(4):
                idx = i * 4 + j
                if idx < amount:
                    res[idx] = (rand >> j * 8) & 0xff
        return bytes(res)
