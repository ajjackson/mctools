import textwrap

import ase.build
from numpy import logical_not
from numpy.random import RandomState
import pytest

from mctools.generic.get_spacegroup import get_spacegroup


FILENAME = "cu_rattled.extxyz"

REF_TEXT = textwrap.dedent(
    """\
    | Threshold / Å |    Space group    |
    |---------------|-------------------|
    |    0.00001    |  P1 (1)           |
    |    0.00010    |  P1 (1)           |
    |    0.00050    |  Pm (6)           |
    |    0.00100    |  Pm (6)           |
    |    0.00500    |  Pmc2_1 (26)      |
    |    0.01000    |  Fm-3m (225)      |
    |    0.05000    |  Fm-3m (225)      |
    |    0.10000    |  Fm-3m (225)      |
    """
)


@pytest.fixture
def symmetry_broken_cu() -> ase.Atoms:
    atoms = ase.build.bulk("Cu", cubic=True) * (2, 2, 2)

    rng = RandomState(seed=1)

    # Break symmetry by up to 0.01 on a mirror plane
    xy_plane = atoms.positions[:, 2] == 0.0
    atoms.positions[xy_plane, :2] += 5e-3 - 1e-2 * rng.rand(xy_plane.sum(), 2)

    # Break symmetry by up to 0.0001 elsewhere
    off_plane = logical_not(xy_plane)
    atoms.positions[off_plane] += 5e-5 - 1e-4 * rng.rand(off_plane.sum(), 3)

    return atoms


def test_get_spacegroup(symmetry_broken_cu, tmp_path, capsys) -> None:
    symmetry_broken_cu.write(tmp_path / FILENAME)
    get_spacegroup(filename=str(tmp_path / FILENAME))
    captured = capsys.readouterr()

    assert captured.out == REF_TEXT
