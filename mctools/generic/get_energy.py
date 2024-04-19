#! /usr/bin/env python

###############################################################################
# Copyright 2017 Adam Jackson
###############################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################

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
