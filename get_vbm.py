#!/usr/bin/env python
from itertools import ifilter

import argparse
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def get_eigs(vasp_xml):
    """Read vasprun.xml file and get the eigenvalues

    Args:
        vasp_xml: path to "vasprun.xml" output file
    Returns:
        eig_sets: list of lists, grouped by k-point
            [[[kpt1_eig1 occ11], [kpt1_eig2, occ12]...]
             [[kpt2_eig1_occ21], [kpt2_eig2, occ22]...] ...]

    """

    tree = ET.ElementTree(file=vasp_xml)

    # Get last set of eigenvalues
    eigs = list(tree.iter(tag='eigenvalues'))[-1]

    type(eigs)
    eig_sets = [eig_set.getchildren()
                for eig_set in eigs.iter('set')
                if ('comment' in eig_set.attrib
                    and 'kpoint' in eig_set.attrib['comment'])]
    
    def eig_set_to_lists(eig_set):
        return map(lambda el: map(float, el.text.split()), eig_set)

    eig_sets = map(eig_set_to_lists, eig_sets)
    return eig_sets

def get_max_eig_from_xml(vasp_xml):
    """
    Read vasprun.xml and return highest occupied eigenvalue.

    If you included the right k-points this should be the VBM...
    """
    eigs = get_eigs(vasp_xml)

    # Flatten from grouping by k-points with this nasty
    # double list comprehension

    all_eigs = [eig for kpt_eigs in eigs for eig in kpt_eigs]
    occupied = ifilter(lambda x: x[1] > 0., all_eigs)
    return max(x[0] for x in occupied)
    
def main(xml_file='vasprun.xml'):
    print get_max_eig_from_xml(xml_file)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Get the maximum occupied eigenvalue from a vasp run."
        )
    parser.add_argument("xml_file", nargs='?', default='vasprun.xml',
                        help="Path to vasprun.xml file")
    args = parser.parse_args()
    main(**vars(args))
