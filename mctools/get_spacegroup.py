#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ase.io
try:
    import spglib.spglib as spglib
except ImportError:
    import pyspglib.spglib as spglib

import argparse

def main(filename=False, format=False):

    if filename:
        pass
    elif os.path.isfile('geometry.in'):
        filename='geometry.in'
    elif os.path.isfile('POSCAR'):
        filename='POSCAR'
    else:
        raise Exception('No input file!')
        
    if format:
        atoms = ase.io.read(filename, format=format)
    else:
        atoms = ase.io.read(filename)
        

    print "| Threshold / Å |    Space group    |"
    print "|---------------|-------------------|"

    for threshold in (1e-5, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2, 5e-2, 1e-1):
        print "|    {0:0.5f}    |  {1: <16} |".format(threshold, spglib.get_spacegroup(atoms, symprec=threshold))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', action='store', default=False,
                        help="Input structure file")
    parser.add_argument('-f', '--format', action='store', default=False,
                        help="File format for ASE importer")
    args = parser.parse_args()
    main(filename=args.input_file, format=args.format)
