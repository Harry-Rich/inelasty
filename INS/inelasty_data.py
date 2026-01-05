from ase.io import read, write
from ase.calculators.vasp import Vasp
import os 
import subprocess
from pathlib import Path
import numpy as np
from phonopy import Phonopy
from phonopy.structure.atoms import PhonopyAtoms
from phonopy.interface.vasp import read_vasp, write_vasp, parse_set_of_forces
import os
import glob
import json



# Utility Functions
def make_sbatch(job_name, time, nodes, ntasks_per_node, command, outdir = "."):
    return f"""#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --output={outdir}/{job_name}_%j.out
#SBATCH --nodes={nodes}
#SBATCH --time={time}
#SBATCH --ntasks-per-node={ntasks_per_node}
    
cd $SLURM_SUBMIT_DIR
{command}
            """

def save_and_submit_sbatch(script, path):
    path = Path(f"{path}/submit.sbatch")
    path.write_text(script)
    subprocess.run(["sbatch", str(path)], check=True)



class inelasty():
    def __init__(self, struc, vasp_path, conda_command, spack_command):
        self.struc = struc
        self.vasp_path = vasp_path
        self.conda_command = conda_command
        self.spack_command = spack_command
        self.location = Path(__file__).resolve().parent
        print(self.location)

        os.environ['VASP_PP_PATH'] = vasp_path

        

    def relax(self, 
              vasp_kwargs1,
              vasp_kwargs2,
              dir_name='geom_opt',
              time ="02:00:00" , 
              ntasks_per_node=12):
        
        
        stage1 = f"{dir_name}/stage_1"
        os.makedirs(stage1, exist_ok = True)
        write(f"{stage1}/POSCAR",self.struc)

        stage2 = f"{dir_name}/stage_2"
        os.makedirs(stage2, exist_ok = True)

        vasp_json1 = json.dumps(vasp_kwargs1)
        vasp_json2 = json.dumps(vasp_kwargs2)


        command = f"""
{self.conda_command}
{self.spack_command}
python {self.location}/geom_relax.py {dir_name} '{vasp_json1}' '{vasp_json2}' {self.vasp_path}
"""
        
        script = make_sbatch(
            job_name=f"geom_relax",
            time=time,
            nodes=1,
            ntasks_per_node=ntasks_per_node,
            command=command,
            outdir = stage1
        )

        save_and_submit_sbatch(script, stage1)



    def run_k_points(self, 
                     vasp_kwargs,
                     kpoints_list = None, 
                     script = None, 
                     dir_name = 'kpoints',
                     time ="02:00:00" , 
                     ntasks_per_node=12):
        """
        Run k_point single point energies for given structure, uses kpoint_spe.py so update vasp calc in that for settings etc.
        """
        if kpoints_list is None:
            kpoints_list = [(1,1,1), (2,2,2), (3,3,3), (4,4,4), (5,5,5), (6,6,6)]
        os.makedirs(dir_name, exist_ok=True)

        for i,kpts in enumerate(kpoints_list):
            kpoints_kwargs = vasp_kwargs
            kpoints_kwargs['kpts'] = kpts
            vasp_json = json.dumps(kpoints_kwargs)
            loop_dir = f"{dir_name}/{i+1}"
            os.makedirs(loop_dir, exist_ok = True)
            write(f"{loop_dir}/POSCAR",self.struc)

            command = f"""
{self.conda_command}
{self.spack_command}
python {self.location}/single_point.py {loop_dir} '{vasp_json}' {self.vasp_path}
"""

            script = make_sbatch(
                job_name=f"kpts_{kpts[0]}",
                time=time,
                nodes=1,
                ntasks_per_node=ntasks_per_node,
                command=command,
                outdir = loop_dir
            )

            save_and_submit_sbatch(script, loop_dir)

    def run_encut(self, 
                  vasp_kwargs,
                  encut_list = None, 
                  script = None, 
                  dir_name = 'encut',
                  time ="02:00:00" , 
                  ntasks_per_node=12):
        """
        Run encut single point energies for given structure
        """
        if encut_list is None:
            encut_list = [200,300,400,500,600,700,800,900,1000,1100,1200,1300]
        os.makedirs(dir_name, exist_ok=True)
        vasp_json = json.dumps(vasp_kwargs)
        for encut in encut_list:
            encut_kwargs = vasp_kwargs
            encut_kwargs['encut'] = encut
            vasp_json = json.dumps(encut_kwargs)
            loop_dir = f"{dir_name}/{encut}"

            os.makedirs(loop_dir, exist_ok = True)
            write(f"{loop_dir}/POSCAR",self.struc)

            command = f"""
{self.conda_command}
{self.spack_command}
python {self.location}/single_point.py {loop_dir} '{vasp_json}' {self.vasp_path}
"""

            script = make_sbatch(
                job_name=f"e_{encut}",
                time=time,
                nodes=1,
                ntasks_per_node=ntasks_per_node,
                command=command,
                outdir = loop_dir
            )

            save_and_submit_sbatch(script, loop_dir)

    def generate_phonopy(self, 
                         atom_path,
                         vasp_kwargs = None,
                         dir_name = "phonopy",
                         supercell_size = 2, 
                         displacement = 0.01, 
                         run = False,
                         time ="02:00:00" , 
                         ntasks_per_node=12
                         ):
        
        
        unitcell = read_vasp(atom_path)
        supercell_matrix = np.eye(3) * supercell_size
        phonon = Phonopy(unitcell, supercell_matrix)
        phonon.generate_displacements(distance=0.01)
        supercells = phonon.supercells_with_displacements
        os.makedirs(dir_name, exist_ok=True)
        phonon.save(f"{dir_name}/phonopy_disp.yaml")

        for i, supercell in enumerate(supercells):
            submit_dir = f"{dir_name}/{dir_name}-{i}"
            os.makedirs(submit_dir, exist_ok=True)
            write_vasp(
                f"{submit_dir}/POSCAR",
                supercell,
            )
            if run == True:
                vasp_json = json.dumps(vasp_kwargs)
                command = f"""
{self.conda_command}
{self.spack_command}
python {self.location}/single_point.py {submit_dir} '{vasp_json}' {self.vasp_path}
"""

                script = make_sbatch(
                    job_name=f"phon_{i}",
                    time=time,
                    nodes=1,
                    ntasks_per_node=ntasks_per_node,
                    command=command,
                    outdir = submit_dir
                )

                save_and_submit_sbatch(script, submit_dir)

    @property
    def atoms(self):
        return self.struc
    

