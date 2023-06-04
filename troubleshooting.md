## USB error after running notebook cell

Might be several things:
 - Other notebook is holding the USB busy.
 - VM USB version issue described below.
 - VM USB device not enabled (described below).
 - ???
 
What usually works for the "???" case is to physically disconnect 
the ChipWhisperer Nano and reconnect it, possibly restarting
the notebook in between, then proceed with the steps. Note, that
during such a restart all of the state of the target is lost
(even keys, or RNG state).

## VM USB version

The VM needs to have USB 3.0 enabled for the ChipWhisperer communication
to work properly. Shutdown the VM, and change this in the settings.

## VM shared folder error

The VM complains about a shared folder "C:/test" not existing.
This can be ignored.

## VM device USB enable

The VM needs to be able to talk to the ChipWhisperer device.
Make sure that you enable "NewAE Technology Inc. ChipWhisperer Nano"
in the "Devices" -> "USB" settings. You may not see this option
unless you have the ChipWhisperer device physically connected.
