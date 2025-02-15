#!/usr/bin/env python
"""
Plot flyby model data from Cuello+2018.

See https://arxiv.org/abs/1812.00961 for paper reference.

Relies on pymcfost (https://github.com/cpinte/pymcfost), and my module
pymcfost_subplots.py (in https://github.com/dmentipl/mcfost-utils).

Assumes data directory structure in the current directory is:

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

D. Mentiplay, 2018.
"""

import os
import pathlib

import matplotlib as mpl
import matplotlib.pyplot as plt

import pymcfost as mcfost
import pymcfost_subplots

########################################################################################

###############
# SET OPTIONS #
###############

ROOT_DATA_DIRECTORY = pathlib.Path('~/runs/flyby/2018-12-13/output').expanduser()

DO_THERMAL = False  # plot thermal emission
DO_SCATTERED = True  # plot scattered light
DO_LINES = False  # plot CO emission

SAVEFIG = True  # save figures to pdf
DROPBOX = True  # cp files to dropbox

SCALE = 5.0  # figure size
FONT_SCALING = 3.0  # font size

BETAS = ['45', '135']  # angle of flyby
TIMES = ['100', '110', '120']  # time of flyby (100 is periastron)
INCLINATIONS = ['00', '90']  # inclination w.r.t. observer
MOMENTS = [0, 1, 2]  # molecular emission moments

SCATTERED = ['1.6']
THERMAL = ['850', '2100']
MOLECULAR = ['CO']

COLORBAR_FIGURE = True

OPTS_THERMAL = {
    'type': 'I',
    'dynamic_range': None,
    'vmin': 1e-07,
    'vmax': 1e-04,
    'fpeak': None,
    'psf_FWHM': 0.20,
    'plot_beam': True,
    'per_beam': True,
    'scale': 'log',
    'cmap': 'inferno',
    'coronagraph': None,
}

OPTS_SCATTERED = {
    'type': 'I',
    'dynamic_range': None,
    'vmin': 2e-18,
    'vmax': 2e-15,
    'fpeak': None,
    'psf_FWHM': 0.05,
    'plot_beam': True,
    'per_beam': True,
    'scale': 'log',
    'cmap': 'gist_heat',
    'coronagraph': None,
}

OPTS_MOLECULAR = {  # [M0, M1, M2]
    'fmin': [0, -2.5, 0],
    'fmax': [0.002, 2.5, 5],
    'psf_FWHM': [0.20, None, None],
    'plot_beam': [True, None, None],
    'color_scale': [None, None, None],
    'cmap': ['Blues_r', 'RdBu', 'viridis'],
}


def format_strings(beta, time, incl):
    time_string = f't = {(int(time)-100)*55} yr'
    incl_beta_string = rf'i = {int(incl)}$\degree$, $\beta$ = {int(beta)}$\degree$'
    return time_string, incl_beta_string


########################################################################################

radiations = list()

if DO_THERMAL:
    radiations += THERMAL

if DO_SCATTERED:
    radiations += SCATTERED

if DO_LINES:
    radiations += MOLECULAR

opts = {
    'thermal': OPTS_THERMAL,
    'scattered': OPTS_SCATTERED,
    'molecular': OPTS_MOLECULAR,
}

mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.size'] = FONT_SCALING * SCALE

position_labels = ['top_left', 'top_right', 'bottom_left', 'bottom_right']
positions = dict()
positions['top_left'] = (0.05, 0.90)
positions['top_right'] = (0.95, 0.90)
positions['bottom_left'] = (0.05, 0.10)
positions['bottom_right'] = (0.95, 0.10)

for beta in BETAS:

    print(f'=== beta = {beta} ===', flush=True)

    text = dict()
    for time in TIMES:
        text[time] = dict()
        for inclination in INCLINATIONS:
            text[time][inclination] = dict()
            for position in position_labels:
                text[time][inclination][position] = None
            text[time][inclination]['top_left'] = format_strings(
                beta, time, inclination
            )[0]
            text[time][inclination]['top_right'] = format_strings(
                beta, time, inclination
            )[1]

    for radiation in radiations:

        print(f'   --- radiation = {radiation} ---', flush=True)

        if radiation in THERMAL:
            itype = 'thermal'
            data = 'Image'

        elif radiation in SCATTERED:
            itype = 'scattered'
            data = 'Image'

        elif radiation in MOLECULAR:
            itype = 'molecular'
            data = 'Line'

        else:
            raise ValueError(f'{radiation} not in thermal, scattered, molecular lists')

        pymcfost_objects = dict()

        for time in TIMES:
            pymcfost_objects[time] = dict()

            for inclination in INCLINATIONS:
                data_directory = ROOT_DATA_DIRECTORY / (
                    'b' + beta + '/t' + time + '/i' + inclination + '/data_' + radiation
                )

                if data == 'Image':
                    pymcfost_objects[time][inclination] = mcfost.Image(data_directory)

                elif data == 'Line':
                    pymcfost_objects[time][inclination] = mcfost.Line(data_directory)

        plotting_options = opts[itype]

        if data == 'Image':

            figure, axes = pymcfost_subplots.plot_figure(
                pymcfost_objects=pymcfost_objects,
                plotting_options=plotting_options,
                text=text,
                positions=positions,
                colorbar_figure=COLORBAR_FIGURE,
            )

            filename = itype + '_b' + beta + '_' + radiation + '.pdf'
            figures = [figure]
            filenames = [filename]

        elif data == 'Line':

            figures = []
            filenames = []

            for moment in MOMENTS:
                figure, axes = pymcfost_subplots.plot_figure(
                    pymcfost_objects=pymcfost_objects,
                    plotting_options=plotting_options,
                    text=text,
                    positions=positions,
                    colorbar_figure=COLORBAR_FIGURE,
                    moment=moment,
                )

                filename = (
                    itype + '_b' + beta + '_' + radiation + '_m' + str(moment) + '.pdf'
                )
                figures.append(figure)
                filenames.append(filename)

        if SAVEFIG:

            for idx, figure in enumerate(figures):
                filename = filenames[idx]
                figure.savefig(filename, bbox_inches='tight')

                if DROPBOX:
                    cmd = f'\\cp {filename} ~/Dropbox/swap'
                    try:
                        os.system(cmd)
                        print(f'copying {filename} to ~/Dropbox/swap', flush=True)
                    except OSError:
                        print("Can't copy pdfs to ~/Dropbox/swap", flush=True)

            plt.close('all')
