import sys
from ase.io import read
from ase.calculators.vasp import Vasp
import os
from settings import kpoint_kwargs, vasp_file_path, vasp_std_path

os.environ['VASP_PP_PATH'] = vasp_file_path

path = sys.argv[1]
kx, ky, kz = map(int, sys.argv[2:5])
atoms = read(f"{path}/POSCAR")

calc = Vasp(
    command=f" {vasp_std_path}> vasp.out",
    directory=f"{path}",
    kpts=(kx, ky, kz),
    **kpoint_kwargs
)

atoms.calc = calc
energy = atoms.get_potential_energy()

with open("kpoints/energy.txt", "a") as f:
    f.write(f"{kx} {ky} {kz} {energy}\n")


