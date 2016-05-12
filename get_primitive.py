#!/usr/bin/env python

import argparse
import sys
import ase
import ase.io 
from pyspglib import spglib

def main(input_file='POSCAR',threshold=1e-5,angle_tolerance=-1.,output_file=False, verbose=False):

    if not output_file:
        verbose=True

    if verbose:
        def vprint(*args):
            for arg in args:
                print arg,
            print ""
    else:
        def vprint(*args):
            pass

    try:
        A = ase.io.read(args.input_file)
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        sys.exit()

    vprint("# Space group: ", str(spglib.get_spacegroup(A,symprec=args.threshold,
                                                        angle_tolerance=args.angle_tolerance)
                              ), '\n')
    
    cell, positions, atomic_numbers =  spglib.find_primitive(A,symprec=args.threshold,
                                angle_tolerance=args.angle_tolerance)

    if positions==None:
        print "This space group doesn't have a more primitive unit cell."

    else:

        vprint("Primitive cell vectors:")
        vprint(cell, '\n')
        vprint("Atomic positions and proton numbers:")
        for position, number in zip(positions,atomic_numbers):
            vprint(position, '\t', number)
        
        if output_file:
            atoms = ase.Atoms(scaled_positions=positions, cell=cell, numbers=atomic_numbers, pbc=True)

            atoms.write(output_file)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Find a primitive unit cell using pyspglib")
    parser.add_argument('-i','--input_file', type=str, default='POSCAR',
                        help="Path to crystal structure file, recognisable by ASE")
    parser.add_argument('-t', '--threshold', type=float, default=1e-05,
                        help="Distance threshold in AA for symmetry reduction (corresponds to spglib 'symprec' keyword)")
    parser.add_argument('-a', '--angle_tolerance', type=float, default=-1.0,
                       help="Angle tolerance for symmetry reduction")
    parser.add_argument('-o', '--output_file', default=False,
                        help="Path/filename for output")
    parser.add_argument('-v', '--verbose', action="store_true",
                        help="Print output to screen even when writing to file.")
    args=parser.parse_args()

    main(input_file=args.input_file, threshold=args.threshold, angle_tolerance=args.angle_tolerance,
         output_file=args.output_file)
