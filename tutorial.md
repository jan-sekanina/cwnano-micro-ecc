# Tutorial

In this tutorial you will mount several attacks on a vulnerable implementation
of ECDSA running on a [ChipWhisperer-Nano](https://rtfm.newae.com/Capture/ChipWhisperer-Nano/) board.

First of all, make sure that you have everything ready as per the
[installation.md](installation.md) file.


## 1. Building the target implementation

Run `make` and observe several `micro-ecc-CWNANO` files being built.

The makefile has one important define `uECC_LEAKY`.
When set to `2` a very leaky scalar-multiplication algorithm is used in ECDSA
(see the [uecc/uECC_leak_more.c](uecc/uECC_leak_more.c) file). When set to `1` a leaky
scalar-multiplication algorithm is used in ECDSA (see the [uecc/uECC_leak.c](uecc/uECC_leak.c) file).
When set to `0` a non-leaky one is used (see the [uecc/uECC_noleak.c](uecc/uECC_noleak.c) file).

By default `uECC_LEAKY` is set to `1` and you should keep it that way.

The implementation is based on [micro-ecc](https://github.com/kmackay/micro-ecc),
the only modifications are in the mentioned files, you can compare the leaky and non-leaky files to
see the differences.

## 2. Interacting with the target

The [client.py](notebooks/client.py) file has a `DeviceTarget` class
that can communicate with the target. The [utils.py](notebooks/utils.py)
has some utility functions, such as the simple PRNG used by the implementation.

Activate the virtualenv where you have installed the dependencies
(or the pre-created one in the VM):

	. virt/bin/activate

In the VM the following command will work for example:

	source ~/cwnano-micro-ecc/venv/bin/activate

Start the Jupyter notebook server by running:

	jupyter notebook

inside this repository.

Open the [collect.ipynb](notebooks/collect.ipynb) Jupyter notebook.

Connect the ChipWhisperer-Nano board via USB and run the cells in order
to first flash the built implementation on the board, connect to it and then collect
**10** traces.

Use the plots to observe the start of the ECDSA signing process.
The function `EccPoint_mult` is called at around sample index 1100 (when
the [uecc/uECC_leak.c](uecc/uECC_leak.c) implementation is used) and continues way past the
collected amount of samples (the full signing would take around 8 million samples).

Don't forget to disconnect from the target once done, so that other notebooks
can work with it.

Also be aware about the possible issue with the Jupyter notebook (cells not actually running but appear to) - see [troubleshooting.md](/troubleshooting.md for more info. Essentially running each cell should produce some output. For example, running cell one should generate the following: ![alt text](figs/logo.png?raw=true "logo")



## 3. Running the nonce-reuse attack

Open the [nonce_reuse.ipynb](notebooks/nonce_reuse.ipynb) notebook
and solve the TODOs to mount the nonce-reuse attackand extract the private key.
Note that in this case, you can interact with the target in any way using the
methods on the `DeviceTarget` class that are shown in the notebook.

## 4a. Running the nonce-bitlength-leak attack (via timing)

For the nonce-bitlength-leak attacks you will need to collect several thousand
traces, this can take some time. Collecting a 1000 traces should take
about 10 minutes. Depending on the noise level in timing measurement (USB jitter,
VM stuff, overall system noise) from 900 to 3000 traces are required for the attack.
If you do not have the time to collec the traces, use the trace set provided below:

**TODO: Trace set link.**

Use the [collect.ipynb](notebooks/collect.ipynb) notebook to collect 1500 traces
and store them into `traces_collected1.pickle` (should take about 15 minutes).

Open the [nonce_bitlength_leak.ipynb](notebooks/nonce_bitlength_leak.ipynb) notebook.

Load the collected (or downloaded) trace set and run the attack with all of the traces,
using overall signing duration as a proxy of the bit-length of the nonce.

If the attack did not work, collect more traces (into `traces_collected2.pickle`)
and use the provided code to merge the trace sets.

Next, you will investigate the success rate of the attack as two of its parameters change:
the number of signatures collected by the attacker, and the number of signatures used by the
attacker to build the lattice. Solve the TODOs.

Answer the questions regarding the success rate.

## 4b. Running the nonce-bitlength-leak attack (via power-tracing)

You will now try to mount the attack without using the timing information, instead
using the collected power traces.

Open the [process.ipynb](notebooks/process.ipynb) notebook.

The notebook contains some imports that you can play with to analyze the traces.
Your overall goal is to do SPA and obtain for each of the traces a guess of the
bit-length of the nonce used in signing.

Compare `traces[0]` and `traces[2]` using the `plot_traces` function.
You should focus on the area from sample number 850 to sample number 1100 which
corresponds to the `uECC_vli_numbits` call in the [uecc/uECC_leak.c](uecc/uECC_leak.c) file.

Follow the instructions in the notebook and experiment with various techniques
to try to obtain a proxy value for the nonce bit-length from the traces. Solve the TODOs.

Once you have a good proxy, you will save it with the traces and continue
with the [nonce_bitlength_leak.ipynb](notebooks/nonce_bitlength_leak.ipynb) notebook.

You used the notebook before with timing leakage, now take your proxy for bit-length
that you computed from the power traces and use that to sort the signatures
and mount the attack. Do all of the steps as in the timing attack variant of the notebook,
especially look at the success rate of the attack.

Finally, you can try to improve your proxy to improve the success rate.
