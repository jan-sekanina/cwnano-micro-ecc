## Dependencies

### Build stuff

`arm-none-eabi` toolchain with the [newlib](https://sourceware.org/newlib/) (also with the nano) variant.

### Python stuff

`python >= 3.8` and installed dependencies from [requirements.txt](/requirements.txt).
Note that the [fpylll](https://github.com/fplll/fpylll) installation is quite involved.

## Building the target

Run `make` and observe several `micro-ecc-CWNANO` files being built.

The makefile has one important define `uECC_LEAKY`. When set to `1` a leaky
scalar-multiplication algorithm is used in ECDSA. When set to `0` a non-leaky one
is used.

## Completing ChipWhisperer Installation on Debian-like systems
Download the 50-newae.rules file from https://github.com/newaetech/chipwhisperer/tree/develop/hardware

Run the following commands: 

    sudo cp 50-newae.rules /etc/udev/rules.d/50-newae.rules
    sudo udevadm control --reload-rules
    sudo groupadd -f chipwhisperer
    sudo usermod -aG chipwhisperer $USER
    sudo usermod -aG plugdev $USER
    reboot

## Virtual Machine

Below is a link to a VirtualBox virtual machine with all the prerequisities installed: 
https://www.dropbox.com/s/95qywk23lgd6es0/ubuntu-23.ova

You need the VirtualBox extension pack to use the VM.
When loading the VM, make sure USB 3.0 is enabled in its settings.

Also, make sure that you enable "NewAE Technology Inc. ChipWhisperer Nano" in the "Devices" -> "USB"
settings.
