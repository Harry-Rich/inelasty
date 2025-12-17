import sys
from ase.io import read, write
from ase.calculators.vasp import Vasp
import os
from settings import geom_relax_kwargs1, geom_relax_kwargs2, vasp_std_path, vasp_file_path

os.environ['VASP_PP_PATH'] = vasp_file_path

atom_path = sys.argv[1]
out_path = sys.argv[2]

atoms = read(f"{atom_path}")


calc1 = Vasp(
    command=f"{vasp_std_path} > vasp.out",
    directory=f"{out_path}/stage_1",
    **geom_relax_kwargs1 
)

atoms.calc = calc1
energy = atoms.get_potential_energy()

calc2 = Vasp(
    command=f"{vasp_std_path}> vasp.out",
    directory=f"{out_path}/stage_2",
    **geom_relax_kwargs2
)

atoms = read(f'{out_path}/stage_1/CONTCAR')
write(f"{out_path}/stage_2/POSCAR",atoms)
atoms.calc = calc2
energy = atoms.get_potential_energy()




