# Installation

You have several options on getting ready for the tutorial:
 - Use a VM provided by us which has everything preinstalled. This is the recommended option.
 - Install everything yourself. When it works, it is a better option than the VM, but getting
it ready is tricky.

## Using a VM

Below is a link to a VirtualBox virtual machine with all the pre-requisities installed:
[https://www.dropbox.com/s/95qywk23lgd6es0/ubuntu-23.ova](https://www.dropbox.com/s/95qywk23lgd6es0/ubuntu-23.ova)

You need the VirtualBox extension pack to use the VM.
When loading the VM, make sure USB 3.0 is enabled in its settings.

Also, make sure that you enable "NewAE Technology Inc. ChipWhisperer Nano" in the "Devices" -> "USB"
settings.

See [troubleshooting.md](/troubleshooting.md) for more info.

## Installing everything yourself

You will need some ARM cross-compilation packages as well as a Python environment to run the code during the tutorial.

### Build stuff

`arm-none-eabi` toolchain with the [newlib](https://sourceware.org/newlib/) (also with the nano) variant.

On Debian-like systems you should be OK with the following packages:

    binutils-arm-none-eabi
    gcc-arm-none-eabi
    libnewlib-arm-none-eabi
    libnewlib-nano-arm-none-eabi
    make

Optionally, having gcc or some other compiler for your host architecture enables you to compile the
target code to your host and run it there.

### Python stuff

`python >= 3.8` and installed dependencies from [requirements.txt](/requirements.txt), which
include [ChipWhisperer](https://github.com/newaetech/chipwhisperer) and [pyecsca](https://neuromancer.sk/pyecsca/).
See the [ChipWhisper installation docs](https://chipwhisperer.readthedocs.io/en/latest/linux-install.html) for info.

Note that the [fpylll](https://github.com/fplll/fpylll) installation is quite involved. There,
you first need to install [fplll](https://github.com/fplll/fplll) (note the missing `y`), ideally
from the git source, and only then follow with installing fpylll (which needs cysignals as a build dependency).

### Completing ChipWhisperer Installation on Debian-like systems

See the [ChipWhisper docs](https://chipwhisperer.readthedocs.io/en/latest/linux-install.html) for instructions.
On Linux, it especially is important to handle the udev rules as described below.

Download the 50-newae.rules file from https://github.com/newaetech/chipwhisperer/tree/develop/hardware

Run the following commands: 

    sudo cp 50-newae.rules /etc/udev/rules.d/50-newae.rules
    sudo udevadm control --reload-rules
    sudo groupadd -f chipwhisperer
    sudo usermod -aG chipwhisperer $USER
    sudo usermod -aG plugdev $USER
    reboot

### How do I know the setup is ready?

There are several things you can check on your own, and some for which you need our hardware.

1. Run `jupyter notebook` in the virtualenv with the mentioned Python packages installed. Open the
   `collect.py` notebook and run the first cell with the imports. No errors (especially import ones)
   should be produced.
2. Run `make` inside of this repository. It should produce a `micro-ecc-CWNANO.elf` and some other files.
   Note that compiler warnings are OK and expected at this point. You will not be able to run the binary
   without the provided hardware, but that it is produced is a good sign.
