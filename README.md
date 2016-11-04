# MCTOOLS

Collection of generic pre- and post- processing tools using the [Atomic Simulation Environment](https://wiki.fysik.dtu.dk/ase). 
Developed while working with [Walsh Materials Design](https://github.com/wmd-group), kept on as a personal toolkit
while at [Scanlon Materials Theory Group](https://github.com/smtg-ucl).

The recommended way of installing is to clone the repository and make a local installation using pip:

``` shell
git clone https://github.com/ajjackson/mctools.git
cd mctools
pip install --user -e .
```

ase-convert (Convert structure files)
-------------------------------------
Use ASE to read a crystal structure file and write out to target format. Call with `-h` flag for usage information. ASE can also get this information from some output file formats, which is useful.

```
# EXAMPLE: read relaxed structure from aims output and write VASP input
bash> ase_convert.py aims.out POSCAR

# EXAMPLE: Convert between files with non-standard names
bash> ase_convert.py -f vasp MY_SUPER_POSCAR -t cif MY_SUPER_CIF
```

get-spacegroup (Spacegroup tolerances)
--------------------------------------
Use [Spglib](http://spg.sourceforge.net) to analyse the symmetry of a
crystal structure file over a range of distance thresholds. This can
be useful for identifying when numerical noise or limited convergence
has resulted in a lower-symmetry spacegroup, as well as for quickly
checking the identity of an unknown structure. Call with `-h` flag for
usage information.

```
# EXAMPLE
bash> get_spacegroup.py -i geometry.in.next_step
| Threshold / Å |    Space group    |
|---------------|-------------------|
|    0.00001    |  P-1 (2)          |
|    0.00010    |  P-1 (2)          |
|    0.00050    |  C2/m (12)        |
|    0.00100    |  C2/m (12)        |
|    0.00500    |  P-3m1 (164)      |
|    0.01000    |  P-3m1 (164)      |
|    0.05000    |  P-3m1 (164)      |
|    0.10000    |  P-3m1 (164)      |
```

get-primitive (Primitive cell generator)
----------------------------------------
Use [Spglib](http://spg.sourceforge.net) to generate a primitive cell
from/to any ASE-supported structure file format. It can be helpful to
use **get_spacegroup.py** first in order to identify an appropriate
symmetry threshold. Call with `-h` flag for usage information.

sendto (submission to remote server)
------------------------------------

Copy the current directory to a specified remote server. The server
accounts must be set up in sendto.conf. This is a convenience tool for
copying files around, and does not submit to a queue.

vasp-charge (Electron counting)
-------------------------------

WORK IN PROGRESS

Report the number of electrons in a proposed vasp calculation
(NELECT).  The name refers to an intended feature (specify system
charge). At the moment there is no real user interface.

Uses the VASP_PP_PATH environment variable; if you use ASE for VASP
calculations this should be set up. Otherwise it will not work.

vectors (Lattice vectors)
-------------------------

Report lattice vectors in a, b, c, alpha, beta, gamma format.  This is
useful for comparing structures and makes for more compact and
intuitive reporting.  Call with `-h` flag for usage information.

```
# EXAMPLE
bash> vectors.py geometry.in
  a     b     c    alpha  beta   gamma
11.451 3.856 6.193 90.00 103.21 90.00
```

Related Repositories 
------
###### [k-grid (Mesh densities)](https://github.com/WMD-Bath/kgrid)
Optimal k-point meshes with a single convergence parameter
###### [RVO (Optimisation tool)](https://github.com/WMD-Bath/rvo)
Rapid volume optimisation with an auxiliary equation of state
