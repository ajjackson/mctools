import ase.build
from ase.calculators.singlepoint import SinglePointCalculator
import ase.io
import pytest

from mctools.generic.get_energy import get_energy


ENERGY = 3.141
FILENAME = "methane.extxyz"


@pytest.fixture
def methane_with_energy() -> ase.Atoms:
    atoms = ase.build.molecule("CH4")
    atoms.calc = SinglePointCalculator(atoms, energy=ENERGY)
    return atoms


def test_get_energy(methane_with_energy, tmp_path) -> None:
    ase.io.write(tmp_path / FILENAME, methane_with_energy)

    assert get_energy(tmp_path / FILENAME) == pytest.approx(ENERGY)
