import sys
from ase.io import read
from ase.calculators.vasp import Vasp
import os
import json


path = sys.argv[1]
atoms = read(f"{path}/POSCAR")
phonopy_kwargs = json.loads(sys.argv[2])
vasp_file_path = sys.argv[3]

os.environ['VASP_PP_PATH'] = vasp_file_path

calc = Vasp(
    command=f"{vasp_file_path}/bin/vasp_std > vasp.out",
    directory=f"{path}",
    **phonopy_kwargs
)

atoms.calc = calc
energy = atoms.get_potential_energy()



