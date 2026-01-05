"""
single_point.py

Run a single-point VASP energy calculation for a given structure.

This script is intended to be executed as a standalone program,
typically via a Slurm batch job. It reads a POSCAR from a specified
directory, constructs an ASE VASP calculator using JSON-encoded
keyword arguments, and evaluates the total energy.

The resulting energy is appended to `energy.txt` in the same directory.

Usage
-----
python single_point.py <path> <vasp_kwargs_json> <vasp_pp_path>

Arguments
---------
path : str
    Directory containing a POSCAR file. All VASP output files
    are written to this directory.
vasp_kwargs_json : str
    JSON-encoded dictionary of ASE VASP calculator keyword arguments
    (e.g. encut, kpts, ismear).
vasp_pp_path : str
    Path to the VASP pseudopotential directory. This is assigned
    to the VASP_PP_PATH environment variable.

Side Effects
------------
- Sets the VASP_PP_PATH environment variable.
- Writes VASP output files to `path`.
- Appends the total energy to `path/energy.txt`.

Notes
-----
- Assumes `vasp_std` is located at `<vasp_pp_path>/bin/vasp_std`.
- Designed for non-interactive execution on HPC systems.
- No error handling is performed; failures will raise exceptions.

"""

import sys
from ase.io import read
from ase.calculators.vasp import Vasp
import os
import json


path = sys.argv[1]
vasp_kwargs = json.loads(sys.argv[2])
vasp_file_path = sys.argv[3]
atoms = read(f"{path}/POSCAR")

os.environ["VASP_PP_PATH"] = vasp_file_path

calc = Vasp(
    command=f"{vasp_file_path}/bin/vasp_std > vasp.out",
    directory=f"{path}",
    **vasp_kwargs,
)

atoms.calc = calc
energy = atoms.get_potential_energy()

with open(f"{path}/energy.txt", "a") as f:
    f.write(f"energy: {energy}\n")
