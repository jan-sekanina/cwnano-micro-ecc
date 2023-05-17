#!/usr/bin/env python3
import subprocess
import time

from ecdsa import VerifyingKey, NIST192p
from ecdsa.util import sigdecode_strings
from ecdsa.ellipticcurve import Point
from hashlib import sha1

from client import DeviceTarget


def load_key(curve, x, y):
    return VerifyingKey.from_public_point(Point(curve.curve, x, y), curve=curve, hashfunc=sha1)


def verify_signature(vk, r, s):
    signature = (r.to_bytes(vk.curve.baselen, byteorder="big"), s.to_bytes(vk.curve.baselen, byteorder="big"))
    return vk.verify_digest(signature, hash, sigdecode=sigdecode_strings)


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
    vk = load_key(curve, *pubkey)
    print("pubkey", pubkey)

    target.scope.default_setup()
    target.scope.adc.samples = 50000
    target.scope.con()

    msg = b"This is the message"
    hash = sha1(msg).digest()
    for i in range(100):
        start = time.perf_counter()
        target.scope.arm()
        r, s = target.sign(hash)
        target.scope.capture()
        trace = target.scope.get_last_trace()
        print(trace)
        print(r, s)
        print(time.perf_counter() - start)

    print("Disconnect")
    target.disconnect()


if __name__ == "__main__":
    main()
