import sys
from ase.io import read
from ase.calculators.vasp import Vasp
import os
from settings import phonopy_kwargs, vasp_file_path, vasp_std_path

os.environ['VASP_PP_PATH'] = vasp_file_path

path = sys.argv[1]
atoms = read(f"{path}/POSCAR")

calc = Vasp(
    command=f"{vasp_std_path} > vasp.out",
    directory=f"{path}",
    **phonopy_kwargs
)

atoms.calc = calc
energy = atoms.get_potential_energy()



