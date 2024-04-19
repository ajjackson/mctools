# -*- coding: utf-8 -*-

import argparse
import os

import ase.io
import spglib


def get_spacegroup(filename=False, format=False):

    if filename:
        pass
    elif os.path.isfile('geometry.in'):
        filename = 'geometry.in'
    elif os.path.isfile('POSCAR'):
        filename = 'POSCAR'
    else:
        raise Exception('No input file!')

    if format:
        atoms = ase.io.read(filename, format=format)
    else:
        atoms = ase.io.read(filename)

    print("| Threshold / Å |    Space group    |")
    print("|---------------|-------------------|")

    for threshold in (1e-5, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2, 5e-2, 1e-1):
        print("|    {0:0.5f}    |  {1: <16} |".format(
            threshold, spglib.get_spacegroup(atoms, symprec=threshold)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', action='store', default=False,
                        help="Input structure file")
    parser.add_argument('-f', '--format', action='store', default=False,
                        help="File format for ASE importer")
    args = parser.parse_args()
    get_spacegroup(filename=args.filename, format=args.format)
