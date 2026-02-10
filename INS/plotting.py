import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from pathlib import Path
import os

"""
This module provides functions to read energy data from VASP output files
and plot the convergence of total energy with respect to k-points and encut.

"""
def read_energy(energy_path):
    """Reads the energy value from a VASP output energy file."""
    with open(energy_path, 'r') as f:
        line = f.read().strip()

    parts = line.split()
    energy = float(parts[1])
    return energy   


def subfolders(folder_path):
    """returns a list of subfolder names (as integers) in the given folder path."""
    values = []

    for number in os.listdir(folder_path):
        full_path = os.path.join(folder_path, number)
        if os.path.isdir(full_path):
            values.append(int(number))

    return values

def read_energies(inelasty_path, parameter_type):
    """
    Reads energy values from VASP output files for a given parameter type (kpoints or encut).
    
    :param inelasty_path: Path to the inelasty calculation directory.
    :param parameter_type: Type of parameter ('kpoints' or 'encut').
    :return: Tuple of (parameter indices/values, corresponding total energies).
    """
    folder_path = os.path.join(inelasty_path, parameter_type)
    parameter_indices = subfolders(folder_path) # get list of parameter indices/values
    parameter_indices_sorted = sorted(parameter_indices) # returns kpoints and encut sorted from lowest to highest value

    energies = []

    for i in parameter_indices_sorted:
        energy_filename = os.path.join(folder_path, str(i), "energy.txt")

        energy = read_energy(energy_filename)
    
        energies.append(energy) # store corresponding energy value

    return parameter_indices_sorted, energies

def plot_kpoints(inelasty_path):
    """
    Plot the convergence of total energy with respect to k-points.
    
    Use read_energies to get k-point indices and energies, then plot them.
    """
    kpoint_index, kpoint_energies = read_energies(inelasty_path, 'kpoints')

    kpoints_df = pd.DataFrame({"K-Point Index": kpoint_index, "Total Energy (eV)": kpoint_energies})

    plt.figure() # Create a new figure for the plot
    plt.plot(kpoints_df["K-Point Index"], kpoints_df["Total Energy (eV)"], marker='o')  # marker='o' shows dots at each point
    plt.xlabel("K-points index")             # Label for x-axis
    plt.ylabel("Total Energy (eV)")          # Label for y-axis
    plt.title(f"Energy vs K-points")          # Plot title
    plt.grid(True)                            # Add a grid to make it easier to read
    kpoint_output_folder = os.path.join(inelasty_path, 'kpoints')
    plt.savefig(os.path.join(kpoint_output_folder, f"kpoints_convergence.png")) # Save the plot as a PNG file
    plt.show()

    return kpoints_df # Return the DataFrame for further use if needed

def plot_encut(inelasty_path):
    """
    Plot the convergence of total energy with respect to ENCUT values.
    
    Use read_energies to get ENCUT values and energies, then plot them.
    """
    encut_index, encut_energies = read_energies(inelasty_path, 'encut') # get list of encut indices and energies

    encut_df = pd.DataFrame({"ENCUT (eV)": encut_index, "Total Energy (eV)": encut_energies})
    
    plt.figure() # Create a new figure for the plot
    plt.plot(encut_df["ENCUT (eV)"], encut_df["Total Energy (eV)"], marker='o')  # marker='o' shows dots at each point
    plt.xlabel("ENCUT value (eV)")             # Label for x-axis
    plt.ylabel("Total Energy (eV)")          # Label for y-axis
    plt.title(f"Energy vs ENCUT")          # Plot title
    plt.grid(True)                            # Add a grid to make it easier to read
    encut_output_folder =  os.path.join(inelasty_path, 'encut')
    plt.savefig(os.path.join(encut_output_folder, f"encut_convergence.png")) # Save the plot as a PNG file
    plt.show()

    return encut_df # Return the DataFrame for further use if needed

""" 

def plot_stage_1_geom_relaxation(inelasty_path): function to plot geometry relaxation for stage 1 and check for convergence.

def plot_stage_2_geom_relaxation(inelasty_path): function to plot geometry relaxation for stage 2 and check for convergence.

"""

def plot_geom_relaxation(inelasty_path, stage: int):
    stage_folder = os.path.join(inelasty_path, 'geom_opt', f'stage_{stage}')
    outcar_path = os.path.join(stage_folder, "OUTCAR")

    stage_data = [] 
    stage_ionic_step = 0
    stage_electronic_step = 0

    with open(outcar_path, "r") as f: # Open the OUTCAR file for reading
        for line in f:
            if "Ionic step" in line:
                stage_ionic_step += 1
                stage_electronic_step = 0 # Reset electronic step counter for new ionic step

            if "Iteration" in line:
                stage_electronic_step += 1
        
            if "free energy    TOTEN" in line:
                parts = line.split() # Split the line into parts
                energy = float(parts[4]) # Convert the fifth part (energy number) to a float
                stage_data.append({"Ionic Step": stage_ionic_step,"Electronic Step": stage_electronic_step,"Total Energy (eV)": energy})

    stage_df = pd.DataFrame(stage_data)

    stage_last_step_df = stage_df.groupby("Ionic Step").last().reset_index() # Get the last electronic step for each ionic step 

    plt.figure()
    scatter = plt.scatter(stage_last_step_df["Ionic Step"], stage_last_step_df["Total Energy (eV)"], c=stage_last_step_df["Electronic Step"], cmap='coolwarm', s=40, marker='o', zorder=2,) # scatter plot with color mapping
    plt.plot(stage_last_step_df["Ionic Step"], stage_last_step_df["Total Energy (eV)"], color='gray', zorder=1) # line plot connecting the points
    plt.xlabel("Ionic Step")
    plt.ylabel("Total Energy (eV)")
    plt.title(f"Total Energy vs Ionic Step for Stage {stage} Geometry Optimisation")
    ax = plt.gca() 
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.3f')) # Format y-axis ticks to 3 decimal place and remove scientific notation
    plt.colorbar(scatter, label="Electronic Step"); # colorbar shows electronic step
    plt.savefig(os.path.join(stage_folder, f"stage_{stage}_geom_relaxation.png")) # Save the plot as a PNG file
    plt.show()
    plt.close()

    return stage_df # Return the DataFrame for further use if needed
    
