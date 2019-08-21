Flybys in protoplanetary discs - II. Observational signatures
=============================================================

The original paper is Cuello N., et al., 2019, MNRAS, [483](https://arxiv.org/abs/1812.00961), [4114](https://ui.adsabs.harvard.edu/abs/2019MNRAS.483.4114C/abstract).

The manuscript is on [Overleaf](https://www.overleaf.com/project/5c37ccccfbc85849bdc86485).

Phantom data
------------

The Flyby simulation data is on `monashbox` computer in `~/runs/flyby/2018-12-13/input`.

The files are already stacked, with dust grains 0.1 mm, 1 mm, 1 cm, and 10 cm stacked onto the gas from the 0.1 mm calculation. We ignored the 1-fluid dust.

The files are:

- `b135-100_`
- `b135-110_`
- `b135-120_`
- `b135-150_`
- `b45-100_`
- `b45-110_`
- `b45-120_`
- `b45-150_`

Question: what Phantom version...?

Radiative transfer
------------------

To run MCFOST on the dust-stacked Phantom dumps:

```
make radiative-transfer
```

This will put the MCFOST output in `~/runs/flyby/...`.

```
    .
    ├── b1
    │   ├── t1
    │   │   ├── i1
    │   │   │   ├── data_1
    │   │   │   ├── data_2
    │   │   ├── i2
    │   │   │   ├── data_1
    │   │   │   ├── data_2
    ├── b2
    │   ├── t1
    │   │   ├── i1
    │   │   │   ├── data_1
    │   │   │   ├── data_2
    │   │   ├── i2
    │   │   │   ├── data_1
    │   │   │   ├── data_2
```

*Note*: This may take a while (i.e. several hours).

**MCFOST version used**: `e875a9434e4e3dfd3cbfd86563b012065cfcd205`

Figures
-------

To make the figures for the paper:

1. First get pymcfost and check out version `f5bc09bc35049d886410e821477acca1a5add26a`.
2. Then patch pymcfost with `pymcfost-flyby.patch`.
3. The run `make figures`.
