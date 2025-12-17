# paths
vasp_file_path = "/home/b55k/harryrich11.b55k/vasp"
vasp_std_path = "/home/b55k/harryrich11.b55k/vasp/bin/vasp_std"

# vasp settings 
kpoint_kwargs = dict(
    encut=800,
    ismear=0,
    sigma=0.01,
    prec="Accurate",
    gga="PE",
    ivdw=12,
    ediff=1e-6,
    lasph=True,
    nsw=0,          # single-point
    ibrion=-1,
)

encut_kwargs = dict(
    kpts=(3,3,3),
    ismear=0,
    sigma=0.01,
    prec="Accurate",
    gga="PE",
    ivdw=12,
    ediff=1e-6,
    lasph=True,
    nsw=0,          # single-point
    ibrion=-1,
)

geom_relax_kwargs1 = dict(
    kpts=(3, 3, 3),
    encut=500,
    ismear=0,
    sigma=0.01,
    prec="Accurate",
    gga="PE",
    ivdw=12,
    ediff=1e-6,
    lasph=True,
    ibrion=2,
    isif=8,
    nsw=20,
)

geom_relax_kwargs2 = dict(
    kpts=(3, 3, 3),
    encut=800,
    ismear=0,
    sigma=0.01,
    prec="Accurate",
    gga="PE",
    ivdw=12,
    ediff=1e-6,
    lasph=True,
    ibrion=1,
    isif=8,
    nsw=100,
)

phonopy_kwargs = dict(
    kpts=(2,2,2),
    encut=800,
    ismear=0,
    sigma=0.01,
    prec="Accurate",
    gga="PE",
    ivdw=12,
    ediff=1e-8,
    lasph=True,
    nsw=0,          # single-point
    ibrion=-1,
)



