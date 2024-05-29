from argparse import ArgumentParser
from typing import Any, Dict, List, Optional

import ase
import ase.io
import spglib


def get_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description="Find a primitive unit cell using spglib")
    parser.add_argument(
        "input_file",
        type=str,
        default="POSCAR",
        help="Path to crystal structure file, recognisable by ASE",
    )
    parser.add_argument(
        "--input-format",
        dest="input_format",
        type=str,
        help="Format for input file (needed if ASE can't guess from filename)",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=float,
        default=1e-05,
        help=(
            "Distance threshold in AA for symmetry reduction "
            "(corresponds to spglib 'symprec' keyword)"
        ),
    )
    parser.add_argument(
        "-a",
        "--angle-tolerance",
        dest="angle_tolerance",
        type=float,
        default=-1.0,
        help="Angle tolerance for symmetry reduction",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        default=None,
        dest="output_file",
        help="Path/filename for output",
    )
    parser.add_argument(
        "--output-format",
        dest="output_format",
        type=str,
        default=None,
        help="Format for input file (needed if ASE can't guess from filename)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print output to screen even when writing to file.",
    )
    parser.add_argument(
        "-p",
        "--precision",
        type=int,
        help=("Number of decimal places for float display. "
              "(Output files are not affected)"),
        default=6,
    )
    return parser


def main(params: Optional[List[str]] = None):
    parser = get_parser()

    if params:
        args = parser.parse_args(params)
    else:
        args = parser.parse_args()

    get_primitive(**snake_case_args(vars(args)))


def snake_case_args(kwarg_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Convert user-friendly hyphenated arguments to python_friendly ones"""
    return {key.replace("-", "_"): value for key, value in kwarg_dict.items()}


def get_primitive(input_file='POSCAR',
                  input_format=None,
                  output_file=None,
                  output_format=None,
                  threshold=1e-5,
                  angle_tolerance=-1.,
                  verbose=False,
                  precision=6):

    if output_file is None:
        verbose = True

    if verbose:

        def vprint(*args):
            for arg in args:
                print(arg, end="")
            print("")

    else:

        def vprint(*args):
            pass

    float_format_str = f"{{:{precision+4}.{precision}f}}"

    def format_float(x: float) -> str:
        return float_format_str.format(x)

    atoms = ase.io.read(input_file, format=input_format)
    atoms_spglib = (
        atoms.cell.array,
        atoms.get_scaled_positions(),
        atoms.numbers,
    )

    spacegroup = spglib.get_spacegroup(
        atoms_spglib, symprec=threshold, angle_tolerance=angle_tolerance)
    vprint(f"Space group: {spacegroup}")

    cell, positions, atomic_numbers = spglib.find_primitive(
        atoms_spglib, symprec=threshold, angle_tolerance=angle_tolerance)

    vprint("Primitive cell vectors:")
    for row in cell:
        vprint(' '.join(map(format_float, row)))

    vprint("Atomic positions and proton numbers:")
    for position, number in zip(positions, atomic_numbers):
        vprint(' '.join(map(format_float, position)), '\t', number)

    if output_file is None:
        pass
    else:
        atoms = ase.Atoms(
            scaled_positions=positions,
            cell=cell,
            numbers=atomic_numbers,
            pbc=True)

        atoms.write(output_file, format=output_format)
