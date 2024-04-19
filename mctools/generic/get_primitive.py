#!/usr/bin/env python

from __future__ import print_function, absolute_import
import argparse
import sys
import ase
import ase.io
try:
    from spglib import spglib
except ImportError:
    from pyspglib import spglib


def main():
    parser = argparse.ArgumentParser(
        description="Find a primitive unit cell using pyspglib")
    parser.add_argument(
        'input_file',
        type=str,
        default='POSCAR',
        help="Path to crystal structure file, recognisable by ASE")
    parser.add_argument(
        '--input_format',
        type=str,
        help="Format for input file (needed if ASE can't guess from filename)")
    parser.add_argument(
        '-t',
        '--threshold',
        type=float,
        default=1e-05,
        help=("Distance threshold in AA for symmetry reduction "
              "(corresponds to spglib 'symprec' keyword)"))
    parser.add_argument(
        '-a',
        '--angle_tolerance',
        type=float,
        default=-1.0,
        help="Angle tolerance for symmetry reduction")
    parser.add_argument(
        '-o', '--output_file', default=None, help="Path/filename for output")
    parser.add_argument(
        '--output_format',
        type=str,
        help="Format for input file (needed if ASE can't guess from filename)")
    parser.add_argument(
        '-v',
        '--verbose',
        action="store_true",
        help="Print output to screen even when writing to file.")
    args = parser.parse_args()

    get_primitive(**vars(args))


def get_primitive(input_file='POSCAR',
                  input_format=None,
                  output_file=None,
                  output_format=None,
                  threshold=1e-5,
                  angle_tolerance=-1.,
                  verbose=False):

    if output_file is None:
        verbose = True

    if verbose:

        def vprint(*args):
            for arg in args:
                print(arg,)
            print("")
    else:

        def vprint(*args):
            pass

    try:
        if input_format is None:
            A = ase.io.read(input_file)
        else:
            A = ase.io.read(input_file, format=input_format)
    except IOError as e:
        raise Exception("I/O error({0}): {1}".format(e.errno, e.strerror))

    vprint(
        "# Space group: ",
        str(
            spglib.get_spacegroup(
                A, symprec=threshold, angle_tolerance=angle_tolerance)),
        '\n')

    cell, positions, atomic_numbers = spglib.find_primitive(
        A, symprec=threshold, angle_tolerance=angle_tolerance)

    if positions is None:
        print("This space group doesn't have a more primitive unit cell.")

    else:
        vprint("Primitive cell vectors:")
        vprint(cell, '\n')
        vprint("Atomic positions and proton numbers:")
        for position, number in zip(positions, atomic_numbers):
            vprint(position, '\t', number)

        if output_file is None:
            pass
        else:
            atoms = ase.Atoms(
                scaled_positions=positions,
                cell=cell,
                numbers=atomic_numbers,
                pbc=True)
            if output_format is None:
                try:
                    atoms.write(output_file, vasp5=True)
                except TypeError:
                    atoms.write(output_file)
            elif output_format is "vasp":
                atoms.write(output_file, format="vasp", vasp5=True)
            else:
                atoms.write(output_file, format=output_format)


if __name__ == "__main__":
    main()
