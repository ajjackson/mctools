#! /usr/bin/env python

"""Get lattice vector in a, b, c, alpha, beta, gamma format from ase-compatible file"""

##############################################################################################
# Copyright 2015 Adam Jackson
##############################################################################################
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
##############################################################################################

import numpy as np
import ase.io
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file",
                  action="store", type="string", dest="input_file", default="geometry.in",
                  help="Path to input file [default: ./geometry.in]")
parser.add_option("-l", "--latex",
                  action="store_true", dest="latex_format", default=False,
                  help="Print in convenient format for insertion in latex tabular environments")
parser.add_option("-p", "--precision", "--precision_length",
                  action="store", type="int", dest="precision_length", default=3,
                  help="Number of decimal places to return (length in Angstroms)")
parser.add_option("-a", "--precision_angle",
                  action="store", type="int", dest="precision_angle", default=2,
                  help="Number of decimal places to return (angle in degrees)")
# Add further options here
(options, args) = parser.parse_args()

# Read file and extract lattice vectors
atoms = ase.io.read(options.input_file)
lattice_matrix = np.array(atoms.get_cell())

# Get lattice vector magnitudes (a, b, c) according to Pythagoras' theorem
(a, b, c) = np.sqrt(np.sum(np.square(lattice_matrix),1))

# Calculate angles between vectors using relation
# A.B = |A||B|cos(theta)
gamma = np.arccos(lattice_matrix[0,:].dot(lattice_matrix[1,:]) \
                    / (np.linalg.norm(lattice_matrix[0,:]) * \
                           np.linalg.norm(lattice_matrix[1,:]) \
                      )
                )

alpha = np.arccos(lattice_matrix[1,:].dot(lattice_matrix[2,:]) \
                    / (np.linalg.norm(lattice_matrix[1,:]) * \
                           np.linalg.norm(lattice_matrix[2,:]) \
                      )
                )

beta = np.arccos(lattice_matrix[2,:].dot(lattice_matrix[0,:]) \
                    / (np.linalg.norm(lattice_matrix[2,:]) * \
                           np.linalg.norm(lattice_matrix[0,:]) \
                      )
                )


# Convert to degrees
(alpha, beta, gamma) = np.array([alpha, beta, gamma]).dot(180/np.pi)

if options.latex_format:
    print '{0:6.{6}f}&{1:6.{6}f}&{2:6.{6}f}&{3:6.{7}f}&{4:6.{7}f}&{5:6.{7}f}'.format(
            a,    b,    c,    alpha, beta, gamma, options.precision_length, options.precision_angle)
else:
    print '  a  {0}b  {0}c {0}alpha{1}beta{1} gamma'.format(
             options.precision_length*" ", options.precision_angle*" ")
    print '{0:.{6}f} {1:.{6}f} {2:.{6}f} {3:.{7}f} {4:.{7}f} {5:.{7}f}'.format(\
            a,    b,    c,    alpha, beta, gamma, options.precision_length, options.precision_angle)

