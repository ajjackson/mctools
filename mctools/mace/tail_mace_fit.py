"""Realtime visualisation of fitting progress for MACE potential"""
from argparse import ArgumentParser
import os
from pathlib import Path
import re
import subprocess

import asciichartpy


FLOAT = r"-?\d+\.\d+"
EPOCH_RE = (rf".*Epoch (\d+): loss=({FLOAT}), "
            rf"RMSE_E_per_atom=({FLOAT}) meV, RMSE_F=({FLOAT}) meV / A.*")
PLOT_CFG = {'height': 10, 'colors': [asciichartpy.blue]}


def main():
    """Realtime visualisation of fitting progress for MACE potential"""
    parser = ArgumentParser()
    parser.add_argument("logfile", type=Path, help="Path to MACE training log")
    parser.add_argument("--buffer", type=int, default=100, help="Max steps to show")
    args = parser.parse_args()


    epoch_re = re.compile(EPOCH_RE)

    epochs, losses, energies, forces = [], [], [], []

    with subprocess.Popen(['tail', '-n', str(args.buffer), '-F', args.logfile],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE) as tail_process:
        for line in tail_process.stdout:
            if (match := epoch_re.match(line.decode())):
                epoch, loss, energy, force = match.groups()

                epochs.append(int(epoch))
                losses.append(float(loss))
                energies.append(float(energy))
                forces.append(float(force))

                os.system("clear")
                epoch_slice = epochs[-args.buffer:]
                print(f"Epochs {epoch_slice[0]}-{epoch_slice[-1]}")

                for title, data in [(f"Loss                    {losses[-1]}", losses),
                                    (f"Energy/atom RMSE (meV)  {energies[-1]}", energies),
                                    (f"Force RMSE (meV / A)    {forces[-1]}", forces)]:

                    print(f"\n{title}")
                    print(asciichartpy.plot(data[-args.buffer:], PLOT_CFG))

            else:
                pass
