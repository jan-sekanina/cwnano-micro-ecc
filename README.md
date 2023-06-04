# Practical Side-Channel Attacks on Real-World ECDSA Implementations

This repository contains the code needed during the tutorial.

See [installation.md](/installation.md) for installation instructions and
[troubleshooting.md](/troubleshooting.md) for common issues.

Finally there is [tutorial.md](/tutorial.md) describing the steps of the tutorial.

Some structure:
 - hal: Contains the Hardware Abstraction Layer files for the STM target boards we are using.
        You don't need to touch this in any way. This is taken from ChipWhisperer firmware directory.
 - simpleserial: Contains the ChipWhisperer SimpleSerial protocol implementation for the victim. 
                 You don't need to touch this in any way.
 - notebooks: Contains the Jupyter notebooks useful for trace collection, analysis and attacks.
 - uecc: Contains a modified version of the [micro-ecc](https://github.com/kmackay/micro-ecc) library.
         You may want to look at it.
 - main.c: Contains the target code that runs on the board and offers several commands.
 - Makefile: Makefile to build the target.
 - Makefile.inc: Additional makefile boilerplate.
 - README.md: This README.
 - installation.md
 - troubleshooting.md
 - tutorial.md
