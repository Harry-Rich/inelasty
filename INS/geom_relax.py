import sys
from ase.io import read, write
from ase.calculators.vasp import Vasp
import os
from settings import geom_relax_kwargs1, geom_relax_kwargs2

os.environ['VASP_PP_PATH'] = '/home/b55k/harryrich11.b55k/vasp'

atom_path = sys.argv[1]
out_path = sys.argv[2]

atoms = read(f"{atom_path}")


calc1 = Vasp(
    command="/home/b55k/harryrich11.b55k/vasp/bin/vasp_std > vasp.out",
    directory=f"{out_path}/stage_1",
    **geom_relax_kwargs1 
)

atoms.calc = calc1
energy = atoms.get_potential_energy()

calc2 = Vasp(
    command="/home/b55k/harryrich11.b55k/vasp/bin/vasp_std > vasp.out",
    directory=f"{out_path}/stage_2",
    **geom_relax_kwargs2
)

atoms = read(f'{out_path}/stage_1/CONTCAR')
write(f"{out_path}/stage_2/POSCAR",atoms)
atoms.calc = calc2
energy = atoms.get_potential_energy()




