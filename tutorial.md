## Building the target

Run `make` and observe several `micro-ecc-CWNANO` files being built.

The makefile has one important define `uECC_LEAKY`. When set to `1` a leaky
scalar-multiplication algorithm is used in ECDSA. When set to `0` a non-leaky one
is used.

## Interacting with the target

The `client.py` file has a `DeviceTarget` class that can communicate with the target.
See the `collect.ipynb` Jupyter notebook.

## Running the attacks

See the `nonce_reuse.ipynb` and `nonce_bitlength_leak.ipynb` notebooks.
