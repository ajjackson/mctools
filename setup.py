"""
Mctools: some tools for materials chemistry using ASE
"""

from __future__ import absolute_import
from setuptools import setup, find_packages
# from os.path import abspath, dirname

def main():
    """Install the package using setuptools"""
    # project_dir = abspath(dirname(__file__))

    setup(
        name='mctools',
        version='1.0.0',
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
            'Programming Language :: Python :: 2.7',
            'Topic :: Scientific/Engineering :: Chemistry',
            'Topic :: Scientific/Engineering :: Physics'
            ],
        keywords='chemistry ase dft',
        packages=find_packages(),
        install_requires=['ase', 'spglib', 'matplotlib'],
        entry_points={
            'console_scripts': [
                'ase-convert = mctools.ase_convert:main',
                'fold-prim = mctools.fold_prim:main',
                'get-energy = mctools.get_energy:main',
                'get-primitive = mctools.get_primitive:main',
                'get-spacegroup = mctools.get_spacegroup:main',
                'get-vbm = mctools.get_vbm:main',
                'get-volume = mctools.get_volume:main',
                'plot-cplap-ternary = mctools.plot_cplap_ternary:main',
                'sqs-read = mctools.sqs_read:main',
                'sendto = mctools.sendto:main',
                'vasp-charge = mctools.vasp_charge:main',
                'vectors = mctools.vectors:main'
                ]
            }
        )

if __name__ == "__main__":
    main()
