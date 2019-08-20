"""
Read a collection of mcfost models and plot images using pymcfost.

This uses the pymcfost.Image and pymcfost.Line submodule
(https://github.com/cpinte/pymcfost).

Daniel Mentiplay, 2018-2019.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# ---------------------------------------------------------------------------- #

# --- global options --- #

SCALE = 5.0
FONT_SCALING = 4

mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.size'] = FONT_SCALING * SCALE

# ---------------------------------------------------------------------------- #

# --- plot image --- #


def plot_figure(
    pymcfost_objects=None,
    plotting_options=None,
    moment=None,
    text=None,
    positions=None,
    colorbar_figure=None,
):

    # Colorbar: figure or per subplot.
    if colorbar_figure is None:
        colorbar_figure = False
        colorbar = True
    else:
        colorbar = not colorbar_figure

    # Get rows and columns for subplots.
    columns = list(pymcfost_objects.keys())
    rows = list(pymcfost_objects[list(pymcfost_objects.keys())[0]].keys())
    nrows = len(rows)
    ncols = len(columns)

    # Get pymcfost type.
    pymcfost_type = pymcfost_objects[columns[0]][rows[0]].__class__.__name__

    # Figure and axes objects.
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, squeeze=False)

    # Loop over rows and columns to make subplots.
    for idxi, row in enumerate(rows):
        for idxj, column in enumerate(columns):

            # Make subplot.
            ax = axes[idxi][idxj]
            if pymcfost_type == 'Image':
                im = pymcfost_objects[column][row].plot(
                    ax=ax, colorbar=colorbar, **plotting_options
                )
            elif pymcfost_type == 'Line':
                im = pymcfost_objects[column][row].plot_map(
                    ax=ax, colorbar=colorbar, **plotting_options
                )

            # Axis ticks and labels.
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            if not idxi == nrows - 1:
                ax.set_xlabel('')
                ax.tick_params(labelbottom=False)
            if not idxj == 0:
                ax.set_ylabel('')
                ax.tick_params(labelleft=False)
            ax.tick_params(
                axis='both',
                which='both',
                color='white',
                length=12,
                width=1,
                bottom=True,
                top=True,
                left=True,
                right=True,
                direction='in',
            )

########################################################################################
# THIS IS A HACK FOR THE PAPER
            print('THIS CODE HAS A HACK FOR THE PAPER')
            print('CHECK THE SOURCE "pymcfost_subplots.py" line 100.')
            ax.set_xticklabels(['', '4', '2', '0', '-2', '-4'])
########################################################################################

            # Add text.
            if text is not None:
                txt = text[column][row]
                position_labels = txt.keys()
                for position_label in position_labels:
                    if 'left' in position_label:
                        ha = 'left'
                    if 'right' in position_label:
                        ha = 'right'
                    ax.text(
                        *positions[position_label],
                        txt[position_label],
                        ha=ha,
                        color='white',
                        transform=ax.transAxes
                    )

    # Set figure size.
    cbar_scale = 1.0
    if colorbar_figure:
        cbar_scale = 0.8
    fig.set_size_inches(ncols * SCALE / cbar_scale, nrows * SCALE)
    fig.subplots_adjust(
        left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0.01, hspace=0.01
    )

    # Add colorbar.
    if colorbar_figure:
        fig.subplots_adjust(right=0.8)
        cax = fig.add_axes([0.81, 0.01, 0.03, 0.98])
        cb = fig.colorbar(im, cax=cax)
        unit = pymcfost_objects[columns[0]][rows[0]].unit
        formatted_unit = (
            unit.replace("-1", "$^{-1}$")
            .replace("-2", "$^{-2}$")
            .replace("JY", "Jy")
            .replace("PIXEL", "pixel")
        )
        if pymcfost_type == 'Image':
            flux_name = plotting_options['type']
            if flux_name == 'I':
                flux_name = 'Flux density'
            cb.set_label(flux_name + " [" + formatted_unit + "]")
        elif pymcfost_type == 'Line':
            if moment == 0:
                cb.set_label("Flux [" + formatted_unit + "km.s$^{-1}$]")
            elif moment == 1:
                cb.set_label("Velocity [km.s$^{-1}]$")
            elif moment == 2:
                cb.set_label("Velocity dispersion [km.s$^{-1}$]")

    return fig, axes
