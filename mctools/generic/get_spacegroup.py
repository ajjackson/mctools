# -*- coding: utf-8 -*-

import argparse
from pathlib import Path
from typing import Optional

import ase.io
import spglib


def get_default_file() -> Path:
    for candidate in ("geometry.in", "POSCAR", "castep.cell"):
        if (structure_file := Path.cwd() / candidate).is_file():
            return structure_file

    raise ValueError("Input file not specified, no default found.")


def get_spacegroup(filename: Optional[Path] = None,
                   filetype: Optional[str] = None):

    if filename is None:
        filename = get_default_file()

    atoms = ase.io.read(str(filename), format=filetype)
    cell = (atoms.cell.array, atoms.get_scaled_positions(), atoms.numbers)

    print("| Threshold / Å |    Space group    |")
    print("|---------------|-------------------|")

    for threshold in (1e-5, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2, 5e-2, 1e-1):
        print("|    {0:0.5f}    |  {1: <16} |".format(
            threshold, spglib.get_spacegroup(cell, symprec=threshold)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path, default=None, nargs="?",
                        help="Input structure file")
    parser.add_argument("-f", "--filetype", type=str, default=None,
                        help="File format for ASE importer")
    args = parser.parse_args()
    get_spacegroup(filename=args.filename, filetype=args.filetype)
