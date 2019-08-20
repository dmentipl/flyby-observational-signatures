Flybys in protoplanetary discs - II. Observational signatures
=============================================================

Phantom data
------------

The Flyby simulation data is on `linuxbox` and `monashbox` computers in `/home/daniel/runs/flyby`. The files are already stacked, with dust grains 0.1 mm, 1 mm, 1 cm, and 10 cm stacked onto the gas from the 0.1 mm calculation. We ignored the 1-fluid dust.

The files are:

- `b135-100_`
- `b135-110_`
- `b135-120_`
- `b135-150_`
- `b45-100_`
- `b45-110_`
- `b45-120_`
- `b45-150_`

Radiative transfer
------------------

Figures
-------

To make the figures for the paper:

1. First get pymcfost and check out version `f5bc09bc35049d886410e821477acca1a5add26a`.
2. Then patch pymcfost with `pymcfost-flyby.patch`.
3. The run `make figures`.
