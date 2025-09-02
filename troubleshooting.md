## USB error after running Jupyter notebook cell

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

## Jupyter notebook: Cells do not actually run (but appear to)

You can also spot this issue in the Jupyter notebook log:

    Uncaught exception in ZMQStream callback

Also, you can spot this when the plots in the notebook stop
updating (and freeze on some fixed resolution).

Making the notebook "trusted" (top-right in the notebook interface)
helps as it is then able to restart when the error happens.

If that does not help, restarting the kernel might help.
The only thing that seems to work reliably is to shut down the notebook
(File -> Close and Halt), and then reopen it. **Note that both 
restarting the kernel and shutting down the notebook looses all of
the internal state of the notebook (variables).**

## Use correct device for this project
Take a look at the box from the device you are attempting to run
this project on and make sure that you are not using for examle
Chip Whisperer Lite.
