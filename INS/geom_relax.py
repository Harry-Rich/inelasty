"""
geom_relax.py

Perform a two-stage VASP geometry relaxation using ASE.

This script is designed to be executed as a standalone program,
typically via a Slurm batch job. A structure is first relaxed
using an initial (usually looser) set of VASP parameters, and the
resulting CONTCAR is then used as input for a second relaxation
with tighter settings.

Both stages are executed sequentially within a single job.

Usage
-----
python geom_relax.py <out_path> <vasp_kwargs_stage1> <vasp_kwargs_stage2> <vasp_pp_path>

Arguments
---------
out_path : str
    Base directory containing `stage_1` and `stage_2` subdirectories.
    `stage_1/POSCAR` must exist prior to execution.
vasp_kwargs_stage1 : str
    JSON-encoded dictionary of ASE VASP calculator keyword arguments
    for the first relaxation stage.
vasp_kwargs_stage2 : str
    JSON-encoded dictionary of ASE VASP calculator keyword arguments
    for the second relaxation stage.
vasp_pp_path : str
    Path to the VASP pseudopotential directory. This is assigned
    to the VASP_PP_PATH environment variable.

Side Effects
------------
- Sets the VASP_PP_PATH environment variable.
- Writes VASP output files to `out_path/stage_1` and `out_path/stage_2`.
- Reads `stage_1/CONTCAR` and writes `stage_2/POSCAR`.

Notes
-----
- Assumes `vasp_std` is located at `<vasp_pp_path>/bin/vasp_std`.
- No explicit convergence or success checks are performed between stages.
- Designed for batch execution on HPC systems.
- Any VASP or ASE errors will raise exceptions and stop execution.

"""

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
os.environ["VASP_PP_PATH"] = vasp_file_path


calc1 = Vasp(
    command=f"{vasp_file_path}/bin/vasp_std > vasp.out",
    directory=f"{out_path}/stage_1",
    **geom_relax_kwargs1,
)

atoms.calc = calc1
energy = atoms.get_potential_energy()

calc2 = Vasp(
    command=f"{vasp_file_path}/bin/vasp_std > vasp.out",
    directory=f"{out_path}/stage_2",
    **geom_relax_kwargs2,
)

atoms = read(f"{out_path}/stage_1/CONTCAR")
write(f"{out_path}/stage_2/POSCAR", atoms)
atoms.calc = calc2
energy = atoms.get_potential_energy()
