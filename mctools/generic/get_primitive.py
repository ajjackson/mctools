"""Get primitive cell from crystal structure using spglib"""

from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Optional

import ase
import ase.io
import spglib


def get_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description="Find a primitive unit cell using spglib")
    parser.add_argument(
        "input_file",
        type=Path,
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
        type=Path,
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


def get_primitive_atoms(
    atoms: ase.Atoms,
    threshold: float = 1e-5,
    angle_tolerance: float = -1.0,
    print_spacegroup: bool = False,
) -> ase.Atoms:
    """Convert ASE Atoms to primitive cell using spglib"""
    atoms_spglib = (
        atoms.cell.array,
        atoms.get_scaled_positions(),
        atoms.numbers,
    )

    spacegroup = spglib.get_spacegroup(
        atoms_spglib, symprec=threshold, angle_tolerance=angle_tolerance)
    if print_spacegroup:
        print(f"Space group: {spacegroup}")

    cell, positions, atomic_numbers = spglib.find_primitive(
        atoms_spglib, symprec=threshold, angle_tolerance=angle_tolerance)

    primitive_atoms = ase.Atoms(
        scaled_positions=positions,
        cell=cell,
        numbers=atomic_numbers,
        pbc=True)

    return primitive_atoms


def get_primitive(input_file: Path = Path('POSCAR'),
                  input_format: Optional[str] = None,
                  output_file: Optional[Path] = None,
                  output_format: Optional[str] = None,
                  threshold: float = 1e-5,
                  angle_tolerance: float = -1.,
                  verbose: bool = False,
                  precision: int = 6) -> None:

    if output_file is None:
        verbose = True

    float_format_str = f"{{:{precision+4}.{precision}f}}"

    def format_float(x: float) -> str:
        return float_format_str.format(x)

    atoms = ase.io.read(input_file, format=input_format)
    atoms = get_primitive_atoms(
        atoms, threshold=threshold, angle_tolerance=angle_tolerance, print_spacegroup=verbose
    )

    if verbose:
        print("Primitive cell vectors:")
        for row in atoms.cell:
            print(" ".join(map(format_float, row)))

        print("Atomic positions and proton numbers:")
        for position, number in zip(atoms.get_scaled_positions(), atoms.numbers):
            print(" ".join(map(format_float, position)) + f"\t{number}")

    if output_file is None:
        pass
    else:

        atoms.write(output_file, format=output_format)
