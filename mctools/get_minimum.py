from __future__ import print_function, absolute_import
import argparse
import ase.io


def main():
    parser = argparse.ArgumentParser(
        description="Get the minimum-energy structure from a trajectory")
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
        '-o', '--output_file', default='POSCAR.min',
        help="Path/filename for output")
    parser.add_argument(
        '--output_format',
        type=str,
        help="Format for input file (needed if ASE can't guess from filename)")
    args = parser.parse_args()
    get_minimum(**vars(args))


def get_minimum(input_file='POSCAR',
                input_format=None,
                output_file=None,
                output_format=None):
    try:
        if input_format is None:
            traj = ase.io.read(input_file, index=':')
        else:
            traj = ase.io.read(input_file, index=':', format=input_format)
    except IOError as e:
        raise Exception("I/O error({0}): {1}".format(e.errno, e.strerror))

    atoms = min(traj, key=(lambda a: a.get_total_energy()))

    if output_format is None:
        try:
            atoms.write(output_file, vasp5=True, direct=True)
        except TypeError:
            atoms.write(output_file)
    elif output_format is "vasp":
        atoms.write(output_file, format="vasp", vasp5=True, direct=True)
    else:
        atoms.write(output_file, format=output_format)


if __name__ == "__main__":
    main()
