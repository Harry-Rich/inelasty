import sys
from ase.io import read
from ase.calculators.vasp import Vasp
import os
import json


path = sys.argv[1]
encut = int(sys.argv[2])
encut_kwargs = json.loads(sys.argv[3])
vasp_file_path = sys.argv[4]
atoms = read(f"{path}/POSCAR")

os.environ['VASP_PP_PATH'] = vasp_file_path

calc = Vasp(
    command=f"{vasp_file_path}/bin/vasp_std > vasp.out",
    directory=f"{path}",
    encut=encut,
    **encut_kwargs
)

atoms.calc = calc
energy = atoms.get_potential_energy()

with open("encut/energy.txt", "a") as f:
    f.write(f"{encut} : {energy}\n")


