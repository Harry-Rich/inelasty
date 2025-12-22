import sys
from ase.io import read, write
from ase.calculators.vasp import Vasp
import os
import json

out_path = sys.argv[1]
geom_relax_kwargs1 = json.loads(sys.argv[2])
geom_relax_kwargs2 = json.loads(sys.argv[3])
vasp_file_path = sys.argv[4]

atoms = read(f"{out_path}/stage_1/POSCAR")
os.environ['VASP_PP_PATH'] = vasp_file_path


calc1 = Vasp(
    command=f"{vasp_file_path}/bin/vasp_std > vasp.out",
    directory=f"{out_path}/stage_1",
    **geom_relax_kwargs1 
)

atoms.calc = calc1
energy = atoms.get_potential_energy()

calc2 = Vasp(
    command=f"{vasp_file_path}/bin/vasp_std > vasp.out",
    directory=f"{out_path}/stage_2",
    **geom_relax_kwargs2
)

atoms = read(f'{out_path}/stage_1/CONTCAR')
write(f"{out_path}/stage_2/POSCAR",atoms)
atoms.calc = calc2
energy = atoms.get_potential_energy()




