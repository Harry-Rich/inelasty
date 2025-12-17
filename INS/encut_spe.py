import sys
from ase.io import read
from ase.calculators.vasp import Vasp
import os
from settings import encut_kwargs

os.environ['VASP_PP_PATH'] = '/home/b55k/harryrich11.b55k/vasp'

path = sys.argv[1]
encut = int(sys.argv[2])
atoms = read(f"{path}/POSCAR")

calc = Vasp(
    command="/home/b55k/harryrich11.b55k/vasp/bin/vasp_std > vasp.out",
    directory=f"{path}",
    encut=encut,
    **encut_kwargs
)

atoms.calc = calc
energy = atoms.get_potential_energy()

with open("encut/energy.txt", "a") as f:
    f.write(f"{encut} : {energy}\n")


