from argparse import ArgumentParser
import ase.io


def get_energy(filename):
    """Wrap ASE to get calculated energy from output file"""
    atoms = ase.io.read(filename)
    return atoms.get_total_energy()


def main():
    """Get calculated energy from output file using ASE"""

    parser = ArgumentParser(description="Read energy from output")
    parser.add_argument("filename", type=str, nargs='?',
                        default="vasprun.xml",
                        help="Path to ab initio output file")

    args = parser.parse_args()

    energy = get_energy(args.filename)
    print(energy)


if __name__ == '__main__':
    main()
