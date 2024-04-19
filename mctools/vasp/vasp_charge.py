#! /usr/bin/env python

from __future__ import print_function, absolute_import, division
import argparse
import os
from math import ceil
import ase.io

def get_neutral_electrons(atoms, pp='PBE', setups={}):
    """Get the number of valence electrons in a neutral structure

    A summary is printed to the standard output.

    Arguments:

        atoms (ase.Atoms): ASE Atoms object corresponding to VASP
            calculation

        pp (str): Specify the potpaw directory. The usual aliases (LDA,
            PBE, PW91) are available, or the full name
            (e.g. 'potpaw_PBE') can be used

        setups (dict): Special POTCAR identities specified per-species
            as a dict. e.g. {'O': '_pv'}

      

    """
    zvals = get_zval_dict(atoms, setups=setups, pp=pp)

    # Sum over atoms
    nelect = sum([zvals[el] for el in atoms.get_chemical_symbols()])

    return nelect

        
def get_zval(potcar):
    """Read ZVAL from a POTCAR file"""

    with open(potcar, 'r') as f:
        for line in f:
            if 'ZVAL' in line:
                break
        else:
            raise Exception('No ZVAL found in file {0}'.format(potcar))

    line = line.strip()
    zval = line.split()[5].strip()

    return float(zval)

def get_zval_dict(atoms, setups={}, pp='PBE'):
    """Set up a dictionary of ZVALs (default electron count)"""

    pp_aliases = {'LDA': 'potpaw',
                  'PBE': 'potpaw_PBE',
                  'PW91': 'potpaw_GGA'}

    if pp in pp_aliases:
        pp = pp_aliases[pp]

    pp_dir = os.path.join(os.environ['VASP_PP_PATH'], pp)
    
    elements = set(atoms.get_chemical_symbols())
    zvals = {} 
    for element in elements:
        if element in setups:
            potcar_path = os.path.join(pp_dir,
                                       element + setups[element],
                                       'POTCAR')
        else:
            potcar_path = os.path.join(pp_dir, element, 'POTCAR')
        zvals[element] = get_zval(potcar_path)
    return zvals


def report(atoms, nelect, charge=0, setups={}, pp='PBE'):
    """Report stats from nelect, suggest numbers of bands"""
    nelect = nelect - charge
    zvals = get_zval_dict(atoms, setups=setups, pp=pp)
    
    formula_str = atoms.get_chemical_formula()
    print("Chemical formula: {0}".format(formula_str))
    for el, z in zvals.items():
        print("{0:3s}:{1:10.2f}".format(el, z))

    nbands_nospin = int(ceil(nelect / 2))
    print("")
    print("Total electrons: {0}".format(nelect))
    print("")    
    print("Occupied bands for non-spin-polarised "
          "calc:{0:4d}".format(nbands_nospin))
    print("Suggested NBANDS for parallelism in:")
    for ppn in (8, 12, 16, 24):
        nbands = int(ceil((nbands_nospin + 4) / ppn) * ppn)
        print("{0:3}:{1:10}".format(ppn, nbands))

def main():
    parser = argparse.ArgumentParser(
        description="Get the expected numbers of electrons and bands")
    parser.add_argument(
        'input_file',
        type=str,
        default='POSCAR',
        help="Path to crystal structure file, recognisable by ASE")
    args = parser.parse_args()

    atoms = ase.io.read(args.input_file)
    nelect = get_neutral_electrons(atoms)

    report(atoms, nelect)

if __name__ == '__main__':
    main()
