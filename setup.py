"""
Mctools: some tools for materials chemistry using ASE
"""

from __future__ import absolute_import
from setuptools import setup, find_packages
# from os.path import abspath, dirname

def main():
    """Install the package using setuptools"""
    setup(
        name='mctools',
        version='1.1',
        description='Convenience tools for computational materials chemistry',
        long_description="""
    Just a few handy scripts using ASE.
    """,
        url="https://github.com/ajjackson/mctools",
        author="Adam J. Jackson",
        author_email="a.j.jackson@physics.org",
        license='GPL v3',

        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Natural Language :: English',
            'Programming Language :: Python :: 3',
            'Topic :: Scientific/Engineering :: Chemistry',
            'Topic :: Scientific/Engineering :: Physics'
            ],
        keywords='chemistry ase dft',
        packages=find_packages(),
        install_requires=['ase', 'spglib', 'matplotlib'],
        entry_points={
            'console_scripts': [
                'fold-prim = mctools.generic.fold_prim:main',
                'get-energy = mctools.generic.get_energy:main',
                'get-minimum = mctools.generic.get_minimum:main',
                'get-primitive = mctools.generic.get_primitive:main',
                'get-spacegroup = mctools.generic.get_spacegroup:main',
                'get-vbm = mctools.vasp.get_vbm:main',
                'get-volume = mctools.generic.get_volume:main',
                'plot-cplap-ternary = mctools.other.plot_cplap_ternary:main',
                'sqs-read = mctools.other.sqs_read:main',
                'sendto = mctools.other.sendto:main',
                'vasp-charge = mctools.vasp.vasp_charge:main',
                'vectors = mctools.generic.vectors:main'
                ]
            }
        )

if __name__ == "__main__":
    main()
