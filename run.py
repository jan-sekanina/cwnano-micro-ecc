#!/usr/bin/env python3
import subprocess
from ecdsa import SECP160r1, VerifyingKey
from ecdsa.util import sigdecode_strings
from ecdsa.ellipticcurve import Point
from hashlib import sha1

from client import DeviceTarget


def main():
    subprocess.run(["make", "PLATFORM=CWNANO"])
    target = DeviceTarget()
    print("Flash")
    target.flash("./micro-ecc-CWNANO.hex")
    print("Connect")
    target.connect()
    print("Init PRNG")
    target.init_prng(bytes.fromhex("cafebabe"))
    print("Generate")
    target.generate_keypair()
    print("Export")
    pubkey = target.export()
    print(pubkey)
    vk = VerifyingKey.from_public_point(Point(SECP160r1.curve, pubkey[0], pubkey[1]), curve=SECP160r1, hashfunc=sha1)
    print("pubkey", pubkey)

    msg = b"This is the message"
    hash = sha1(msg).digest()
    for i in range(100):
        r, s = target.sign(hash)
        print(r, s)
        signature = (r.to_bytes(SECP160r1.baselen, byteorder="big"), s.to_bytes(SECP160r1.baselen, byteorder="big"))
        print(vk.verify_digest(signature, hash, sigdecode=sigdecode_strings))

    print("Disconnect")
    target.disconnect()


if __name__ == "__main__":
    main()
