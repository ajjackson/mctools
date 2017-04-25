"""
Mctools: some tools for materials chemistry using ASE
"""

from os.path import abspath, dirname
from setuptools import setup, find_packages

project_dir = abspath(dirname(__file__))

setup(
    name='mctools',
    version='0.2.0',
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
    install_requires=['ase', 'spglib'],
    entry_points={
        'console_scripts': [
            'ase-convert = mctools.ase_convert:main',
            'get-primitive = mctools.get_primitive:main',
            'get-spacegroup = mctools.get_spacegroup:main',
            'get-vbm = mctools.get_vbm:main',
            'get-volume = mctools.get_volume:main',
            'sqs-read = mctools.sqs_read:main',
            'sendto = mctools.sendto:main',
            'vasp-charge = mctools.vasp_charge:main',
            'vectors = mctools.vectors:main'
            ]
        }    
    )
