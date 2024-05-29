import textwrap

import ase
import ase.build
from numpy.random import RandomState
import pytest

from mctools.generic.get_primitive import main


FILENAME = "rattled_cu.extxyz"
OUTFILENAME = "POSCAR"
REF_STDOUT = textwrap.dedent(
    """\
    Space group: Fm-3m (225)
    Primitive cell vectors:
      0.000   1.805   1.805
      1.805   0.000   1.805
      1.805   1.805   0.000
    Atomic positions and proton numbers:
      0.500   0.500   0.500\t29
    """
)
REF_POSCAR = textwrap.dedent(
    """\
    Cu 
     1.0000000000000000
         0.0000000000000000    1.8050080045893520    1.8050080045893520
         1.8050080045893520    0.0000000000000000    1.8050080045893520
         1.8050080045893520    1.8050080045893520    0.0000000000000000
     Cu 
       1
    Cartesian
      1.8050080045893520  1.8050080045893520  1.8050080045893520
    """  # noqa:W291
)


@pytest.fixture
def rattled_cu() -> ase.Atoms:
    rng = RandomState(seed=1)

    atoms = ase.build.bulk("Cu", cubic=True) * (2, 2, 2)
    atoms.rattle(stdev=1e-3, seed=1)
    atoms.set_cell(atoms.cell.array + 1e-4 * rng.rand(3, 3))

    return atoms


def test_get_primitive(rattled_cu, tmp_path, capsys) -> None:
    rattled_cu.write(tmp_path / FILENAME)

    main([str(tmp_path / FILENAME),
          "--input-format=extxyz",
          "--threshold=1e-2",
          "--angle-tolerance=1",
          "-o",
          str(tmp_path / OUTFILENAME),
          "-v",
          "--precision=3"
          ])

    captured = capsys.readouterr()
    assert captured.out == REF_STDOUT

    with open(tmp_path / OUTFILENAME, "r") as fd:
        assert fd.read() == REF_POSCAR
