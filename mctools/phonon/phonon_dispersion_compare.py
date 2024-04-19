import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import List, Optional

from euphonic import ForceConstants, ureg
from euphonic.cli.utils import _bands_from_force_constants, load_data_from_file
from euphonic.plot import plot_1d, plot_1d_to_axis
from matplotlib import pyplot as plt
from matplotlib.axes import Axes


def get_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        "filenames", nargs="+", type=Path, help="Force constants data files"
    )
    parser.add_argument(
        "--labels",
        nargs="+",
        type=str,
        default=None,
        help="Labels corresponding to filenames",
    )
    parser.add_argument(
        "--save",
        type=Path,
        nargs='?',
        default=None,
        const="bands.pdf",
        help="Save figure to file",
    )
    parser.add_argument(
        "--title",
        type=str,
        default=None,
        help="Figure title"
    )
    parser.add_argument(
        "--legend-axis",
        dest="legend_axis",
        type=int,
        default=0,
        help=("Index for band segment with legend. "
              "(Use this when the first segment is short!)")
    )
    return parser


def plot_bands(
    fc: ForceConstants, axes: Optional[List[Axes]], color="C0"
) -> List[Axes]:
    bands, x_tick_labels, split_args = _bands_from_force_constants(
        fc,
        q_distance=(0.01 * ureg("1/angstrom")),
        asr="reciprocal",
        dipole=True,
    )
    bands.reorder_frequencies()
    spectrum = bands.get_dispersion()
    spectrum.x_tick_labels = x_tick_labels

    if axes is None:
        # plot_1d creates a final invisible axis: the rest are
        # segments of the band structure.
        fig = plot_1d(spectrum.split(**split_args), color=color)
        axes = fig.axes[:-1]
    else:
        for ax, segment in zip(axes, spectrum.split(**split_args)):
            plot_1d_to_axis(segment, ax, color=color)

    return axes


def main():
    args = get_parser().parse_args()

    data = [load_data_from_file(filename) for filename in args.filenames]
    for fc, filename in zip(data, args.filenames):
        if not isinstance(fc, ForceConstants):
            print(
                "Cannot use {filename}, this script only "
                "works with force constants"
            )
            sys.exit()

    axes = None
    for i, fc in enumerate(data):
        axes = plot_bands(fc, axes, color=f'C{i}')

    # There are a lot of lines, to get a sensible legend
    # we just label one per file
    nbands = int(len(axes[0].lines) / len(data))
    labels = args.labels if args.labels else [str(f) for f in args.filenames]
    axes[args.legend_axis].legend(axes[0].lines[::nbands], labels)

    fig = axes[0].get_figure()
    if args.title:
        fig.suptitle(args.title)

    if args.save:
        fig.savefig(args.save)
    else:
        plt.show()
