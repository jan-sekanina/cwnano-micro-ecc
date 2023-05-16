#!/usr/bin/env python3
import subprocess
from ecdsa import VerifyingKey, NIST192p
from ecdsa.util import sigdecode_strings
from ecdsa.ellipticcurve import Point
from hashlib import sha1

from client import DeviceTarget


def main():
    curve = NIST192p
    subprocess.run(["make", "PLATFORM=CWNANO"])
    target = DeviceTarget()
    print("Flash")
    target.flash("./micro-ecc-CWNANO.hex")
    target.timeout = 2000
    print("Connect")
    target.connect()
    print("Init PRNG")
    target.init_prng(bytes.fromhex("cafebabe"))
    print("Generate")
    target.generate_keypair()
    print("Export")
    pubkey = target.export()
    print(pubkey)
    vk = VerifyingKey.from_public_point(Point(curve.curve, pubkey[0], pubkey[1]), curve=curve, hashfunc=sha1)
    print("pubkey", pubkey)

    msg = b"This is the message"
    hash = sha1(msg).digest()
    for i in range(100):
        r, s = target.sign(hash)
        print(r, s)
        signature = (r.to_bytes(curve.baselen, byteorder="big"), s.to_bytes(curve.baselen, byteorder="big"))
        print(vk.verify_digest(signature, hash, sigdecode=sigdecode_strings))

    print("Disconnect")
    target.disconnect()


if __name__ == "__main__":
    main()
