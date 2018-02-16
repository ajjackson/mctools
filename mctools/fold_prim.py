#! /usr/bin/env python
from argparse import ArgumentParser
from os.path import isfile
from json import loads
from ase import Atoms
import ase.io
from numpy import matrix
from numpy.linalg import inv


def fold_prim(supercell_file, supercell_matrix, output='prim_cell_lattice.in'):
    """Get a primitive cell corresponding to a supercell

    Args:
        supercell_file (str): Path to supercell structure file. This should be
            a format recognised by ASE.
        supercell_matrix (str): Supercell expansion of the primitive cell. This
            is a 3x3 matrix, which can be expressed as a string with the format
            "[[ax, ay, az], [bx, by, bz], [cx, cy, cz]]" or without punctuation
            as "ax ay az bx by bz cx cy cz" or a path to an atat str file in
            which case lines 4-6 will be read in as a 3x3 matrix.
        output (str): Filename for output of dummy structure with correct
            lattice vectors. If None, do not write file.

    Returns:
        ase.Atoms:
            dummy structure with correct lattice vectors
    """

    R_supercell = matrix(ase.io.read(supercell_file).cell)

    if isfile(supercell_matrix):
        with open(supercell_matrix, 'r') as f:
            for i in range(3):
                f.readline()
            rows = [f.readline() for i in range(3)]

        S = [[float(x) for x in row.split()] for row in rows]
        S = matrix(S)
        print(S)

    elif '[' in supercell_matrix:
        S = matrix(loads(supercell_matrix))

    else:
        S = [float(x) for x in supercell_matrix.split()]
        assert len(S) == 9
        S = matrix(S)
        S = S.reshape((3, 3))

    new_cell = inv(S) * R_supercell

    atoms = Atoms('X', cell=new_cell)

    if output is not None:
        ase.io.write(output, atoms, format='vasp', vasp5=True)

    return atoms


def main():
    parser = ArgumentParser(description="""
        Get a dummy primitive cell, given a supercell structure and matrix.
        The purpose of this is to set up calculations with BANDUP, which may
        require a primitive cell for a disordered phase. The given supercell
        matrix is inverted to obtain appropriate lattice vectors for the
        development of a k-point path.
        """)

    parser.add_argument('file', type=str,
                        help="Structure file for relaxed supercell")
    parser.add_argument(
        'matrix', type=str,
        help=("""Supercell matrix. Either provide a path to an ATAT structure
                 file, or provide matrix as a quoted string in form
                              '[[ax, ay, az], [bx, by, bz], [cx, cy, cz]]'
                              or 'ax ay az bx by bz cx cy cz' """))
    parser.add_argument('-o', '--output', type=str,
                        default='prim_cell_lattice.in',
                        help="Path for output file in VASP format.")

    args = parser.parse_args()

    fold_prim(supercell_file=args.file,
              supercell_matrix=args.matrix,
              output=args.output)
