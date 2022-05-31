from argparse import ArgumentParser
import re
from collections import OrderedDict
from math import ceil
import numpy as np
from scipy.spatial import ConvexHull
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.gridspec import GridSpec


def main():
    parser = ArgumentParser(
        description="Plot a ternary system from CPLAP outputs")
    parser.add_argument('-o', '--output', type=str, default=None,
                        help='Output plot filename. Default: plot to screen')
    parser.add_argument('-g', '--grid-file', type=str, default='grid.dat',
                        dest='grid_file',
                        help='Path to grid.dat file from CPLAP')
    parser.add_argument('-t', '--txt-file', type=str, default='2Dplot.txt',
                        dest='txt_file',
                        help='Path to 2Dplot.txt file from CPLAP')
    parser.add_argument('--xmin', type=float, default=None,
                        help='x-axis lower limit')
    parser.add_argument('--ymin', type=float, default=None,
                        help='y-axis lower limit')
    parser.add_argument('--style', type=str, nargs='+', default=['ggplot'],
                        help=('Path to Matplotlib style file(s) and/or name(s)'
                              ' of inbuilt styles.'))
    parser.add_argument('--cmap', type=str, default='viridis',
                        help=('Matplotlib colormap'))
    parser.add_argument('--width', type=float, default=6)
    parser.add_argument('--height', type=float, default=4)
    parser.add_argument('--ratio', type=int, nargs='+', default=[4],
                        help=('Fraction of width occupied by plot vs colorbar:'
                              ' give one or two integers. E.g. --ratio 4 gives'
                              ' 4:1 ratio, --ratio 7 3 gives 7:3 ratio. '
                              'You may need to tune this when using --width.'))
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--gridlines', action='store_true',
                       dest='gridlines', default=None)
    group.add_argument('--no-gridlines', action='store_false',
                       dest='gridlines')
    args = parser.parse_args()
    plot_cplap_ternary(**vars(args))


def plot_cplap_ternary(output='plot-2d.pdf',
                       grid_file='grid.dat', txt_file='2Dplot.txt',
                       xmin=None, ymin=None,
                       style=['ggplot'], cmap='viridis',
                       width=6, height=4, ratio=[4],
                       gridlines=None):
    # Set Truetype PDF/PS fonts unless overruled by style file
    matplotlib.rcParams['pdf.fonttype'] = 42
    matplotlib.rcParams['ps.fonttype'] = 42
    if len(style) > 0:
        matplotlib.style.use(style)

    fig = plt.figure(figsize=(width, height))

    if len(ratio) == 1:
        ratio += [1]
    elif len(ratio) > 2:
        raise ValueError('Ratio can be given as one or two integers. '
                         '{} is too many!'.format(len(ratio)))
    gs = GridSpec(1, ratio[0] + ratio[1])
    ax = fig.add_subplot(gs.new_subplotspec((0, ratio[1]), colspan=ratio[0]))
    cax = fig.add_subplot(gs.new_subplotspec((0, 0), colspan=ratio[1]))

    with open(grid_file, 'rt') as f:

        # Scroll to formula and read
        for _ in range(3):
            line = f.readline()
            el_matches = re.findall(r'\d+ (\w+)', line)

        # Scroll to number of points and read
        for _ in range(4):
            line = f.readline()
        npts = 5
        npts_matches = re.findall(r'first\s+(\d+) points', line)

        if len(npts_matches) == 1:
            npts = int(npts_matches[0])
        else:
            raise Exception("Couldn't read number of polyhedron corners")

        # Scroll to data lines and read coordinates from npts lines
        for _ in range(5):
            f.readline()
        region = np.zeros((npts, 2))

        for i in range(npts):
            line = f.readline().split()
            x, y = float(line[0]), float(line[1])
            region[i, :] = x, y

    # # Use convex hull solver to draw polyhedron edges in correct order
    # hull = np.array([region[i] for i in ConvexHull(region).vertices])
    # region_patch = Polygon(hull, facecolor=(0.6, 0.6, 0.6))
    # ax.add_patch(region_patch)

    # Read in rest of mesh, skipping header, region and '|' column
    mesh = np.genfromtxt('grid.dat', skip_header=(12 + npts),
                         usecols=(0, 1, 3))
    mesh_x = sorted(set(mesh[:, 0]))
    mesh_y = sorted(set(mesh[:, 1]))
    mesh_z = np.zeros((len(mesh_y), len(mesh_x))) * np.NaN
    for x, y, z in mesh:
        ix = mesh_x.index(x)
        iy = mesh_y.index(y)
        mesh_z[iy, ix] = z
    mesh_z = np.ma.masked_invalid(mesh_z)
    dep_mu = ax.pcolormesh(mesh_x, mesh_y, mesh_z, rasterized=True, cmap=cmap)
    cbar = fig.colorbar(dep_mu, cax=cax)
    cbar.set_label(r'$\mu$ ({}) / eV'.format(el_matches[2]))

    with open('2Dplot.txt', 'rt') as f:
        lines = f.readlines()

    data = OrderedDict()

    for i in range(len(lines) // 4 + 1):
        species = lines[i * 4][1:-1]

        x1, y1 = map(float, lines[i * 4 + 1].split())
        x2, y2 = map(float, lines[i * 4 + 2].split())

        data[species] = [[x1, x2], [y1, y2]]

    if xmin is None:
        xmin = ceil(min(min(coords[0]) for coords in data.values()))
    if ymin is None:
        ymin = ceil(min(min(coords[1]) for coords in data.values()))

    for species, (x, y) in data.items():
        ax.plot(x, y, '-', label=format_chem(species))

    ax.legend()
    ax.set_xlim(xmin, 0)
    ax.set_ylim(ymin, 0)
    ax.set_xlabel(r'$\mu$ ({}) / eV'.format(el_matches[0]))
    ax.xaxis.set_label_position('top')
    ax.xaxis.set_ticks_position('top')
    ax.set_ylabel(r'$\mu$ ({}) / eV'.format(el_matches[1]))
    ax.yaxis.set_label_position('right')
    ax.yaxis.set_ticks_position('right')

    # Gridlines option can overrule style defaults
    if gridlines is not None:
        ax.grid(gridlines)

    fig.tight_layout()

    if output is None:
        plt.show()
    else:
        fig.savefig(output)


def format_chem(species):
    text = re.findall(r'\D+', species)
    nums = re.findall(r'\d+', species)
    chem = ''
    for t, n, in zip(text, nums):
        chem += t
        chem += r'$_{{{}}}$'.format(n)
    if len(text) > len(nums):
        chem += text[-1]
    return chem

if __name__ == '__main__':
    main()
