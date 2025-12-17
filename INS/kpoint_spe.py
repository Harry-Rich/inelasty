import sys
from ase.io import read
from ase.calculators.vasp import Vasp
import os
from settings import kpoint_kwargs

os.environ['VASP_PP_PATH'] = '/home/b55k/harryrich11.b55k/vasp'

path = sys.argv[1]
kx, ky, kz = map(int, sys.argv[2:5])
atoms = read(f"{path}/POSCAR")

calc = Vasp(
    command="/home/b55k/harryrich11.b55k/vasp/bin/vasp_std > vasp.out ",
    directory=f"{path}",
    kpts=(kx, ky, kz),
    **kpoint_kwargs
)

atoms.calc = calc
energy = atoms.get_potential_energy()

with open("kpoints/energy.txt", "a") as f:
    f.write(f"{kx} {ky} {kz} {energy}\n")


