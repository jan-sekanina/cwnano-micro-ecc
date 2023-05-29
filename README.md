# Practical Side-Channel Attacks on Real-World ECDSA Implementations

This repository contains the code needed during the tutorial.

Some structure:
 - hal: Contains the Hardware Abstraction Layer files for the STM target boards we are using.
        You don't need to touch this in any way. This is taken from ChipWhisperer firmware directory.
 - simpleserial: Contains the ChipWhisperer SimpleSerial protocol implementation for the victim. 
                 You don't need to touch this in any way.
 - notebooks: Contains the Jupyter notebooks useful for trace collection, analysis and attacks.
 - uecc: Contains a modified version of the [micro-ecc](https://github.com/kmackay/micro-ecc) library.
         You do likely need to look at it.
 - main.c: Contains the target code that runs on the board and offers several commands.
 - Makefile: Makefile to build the target.
 - Makefile.inc: Additional makefile boilerplate.
 - README.md: This README.

## Dependencies

### Build stuff

`arm-none-eabi` toolchain with the [newlib](https://sourceware.org/newlib/) (also with the nano) variant.

### Python stuff

`python >= 3.8` and installed dependencies from [requirements.txt](/requirements.txt).

### SageMath stuff

`sagemath` and ability to run a Jupyter notebook with a SageMath kernel.

## Building the target

Run `make` and observe several `micro-ecc-CWNANO` files being built.

The makefile has one important define `uECC_LEAKY`. When set to `1` a leaky
scalar-multiplication algorithm is used in ECDSA. When set to `0` a non-leaky one
is used.

## Completing ChipWhisperer Installation
Download the 50-newae.rules file from  https://github.com/newaetech/chipwhisperer/tree/develop/hardware

Run the following commands: 

        sudo cp 50-newae.rules /etc/udev/rules.d/50-newae.rules
        sudo udevadm control --reload-rules
        sudo groupadd -f chipwhisperer
        sudo usermod -aG chipwhisperer $USER
        sudo usermod -aG plugdev $USER
        reboot

## Interacting with the target

The `client.py` file has a `DeviceTarget` class that can communicate with the target.
See the `collect.ipynb` Jupyter notebook.

## Running the attacks

See the `nonce_reuse.ipynb` and `nonce_bitlength_leak.ipynb` notebooks.