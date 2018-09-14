#!/usr/bin/env  /usr/local/bin/python
# encoding: utf-8

'''
    $Author: Qiang Zhu $
    perform basic vasp calculations for a series of POSCARs
    python auto-calc.py -f POSCARs
'''


from pymatgen.io.vasp.sets import MPRelaxSet, MPStaticSet, MPNonSCFSet
from pymatgen.io.vasp import Vasprun, BSVasprun
from pymatgen.electronic_structure.plotter import DosPlotter, BSPlotter
from pymatgen.io.vasp.inputs import Potcar, Poscar
from optparse import OptionParser
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
import os
import shutil
import numpy as np
import warnings
import matplotlib as mpl
mpl.use('Agg')
warnings.filterwarnings("ignore")


# read atom names
def run_vasp(cmd, dir):
    os.chdir(dir)
    os.system(cmd)
    os.chdir('../')


def Read_POSCARS(filename):
    """
    Read POSCARS in a single file and convert it to Pymatgen structure object
    """
    # Read INPUT  file
    Struc = []
    f = open(filename, 'rb')
    input_content = f.readlines()
    f.close()

    POSCAR_content = []
    N_atom = 0
    for str1 in input_content:
        POSCAR_content.append(str(str1, 'utf-8'))
        if len(POSCAR_content) == 7:
            N_atom = sum(int(f) for f in str1.split())
        elif len(POSCAR_content) == 8+N_atom:
            pos_str = ''.join(POSCAR_content)
            try:
                p = Poscar.from_string(pos_str)
                Struc.append(p.structure)
            except:
                print('strucuture is wrong', pos_str)
                raise
            POSCAR_content = []
    return Struc


parser = OptionParser()
parser.add_option("-f",  "--file", dest="posfile",
                  help="by filename in POSCAR format")
(options, args) = parser.parse_args()

cmd = ' mpirun -np 24 /share/apps/bin/vasp541-2013sp1/vasp_std > vasp_log'

opt_dir = 'Opt'
static_dir = 'Static'
band_dir = 'Band'
dos_dir = 'Dos'

todo = Read_POSCARS(options.posfile)

count = 0
for struc_id in todo:
    count = count + 1
    finder = SpacegroupAnalyzer(struc_id, symprec=0.06, angle_tolerance=5)
    struc = finder.get_primitive_standard_structure()
    if max(struc.lattice.angles) > 140 or min(struc.lattice.angles) < 40:
        struc = finder.get_conventional_standard_structure()
    if count < 10:
        label = '00'+str(count)
    elif count < 100:
        label = '0'+str(count)
    else:
        label = str(count)

    Name = label + '-' + str(struc.formula).replace(" ", "")
    print('Creating new directory: ', Name)
    if os.path.isdir(Name) is False:
        os.mkdir(Name)
    os.chdir(Name)
    if os.path.exists('static-vasprun.xml') is False:

        myset = {"ISPIN": 1,
                 "ALGO": 'Normal',
                 "PREC": 'Normal',
                 "ENCUT": 400,
                 "ICHARG": 0,
                 "LAECHG": "False",
                 'NELM': 60,
                 "LVHAR": "False",
                 "ISMEAR": 1,
                 }

        opt = MPRelaxSet(struc, user_incar_settings=myset)
        opt.write_input(opt_dir)
        run_vasp(cmd, opt_dir)

        if os.stat(opt_dir+'/CONTCAR').st_size == 0:
            myset = {"ISPIN": 1,
                     "ALGO": 'Normal',
                     "PREC": 'Normal',
                     "ENCUT": 400,
                     "ICHARG": 0,
                     "LAECHG": "False",
                     'NELM': 60,
                     "LVHAR": "False",
                     "ISMEAR": 1,
                     "SYMPREC": 1e-8,
                     }
        opt = MPRelaxSet(struc, user_incar_settings=myset)
        opt.write_input(opt_dir)
        run_vasp(cmd, opt_dir)

        myset = {"ISPIN": 1,
                 "ALGO": 'Normal',
                 "LAECHG": "False",
                 'NELM': 60,
                 "LVHAR": "False",
                 "ISMEAR": 1,
                 }

        struc = Poscar.from_file(opt_dir+'/CONTCAR').structure
        opt = MPRelaxSet(struc, user_incar_settings=myset)
        opt.write_input(opt_dir)
        run_vasp(cmd, opt_dir)
        shutil.rmtree(opt_dir)

        myset = {"ISPIN": 1,
                 "LAECHG": "False",
                 "LVHAR": "False",
                 "LWAVE": "True",
                 "ISMEAR": 1,
                 "LELF": "True"}

        static = MPStaticSet(struc, user_incar_settings=myset)
        static.write_input(static_dir)
        run_vasp(cmd, static_dir)
        if os.stat(static_dir+'/CONTCAR').st_size == 0:
            myset = {"ISPIN": 1,
                     "LAECHG": "False",
                     'NELM': 60,
                     "LVHAR": "False",
                     # "LWAVE": "True",
                     "ISMEAR": 1,
                     "SYMPREC": 1e-8,
                     # "LELF": "True",
                     }
            static = MPStaticSet(struc, user_incar_settings=myset)
            static.write_input(static_dir)
            run_vasp(cmd, static_dir)

        os.system('cp ' + static_dir + '/vasprun.xml  ./static-vasprun.xml')

        # 2nd run to obtain dos
        dos = MPNonSCFSet.from_prev_calc(static_dir,
                                         mode="uniform",
                                         reciprocal_density=200,
                                         user_incar_settings=myset)
        dos.write_input(dos_dir)
        run_vasp(cmd, dos_dir)
        os.system('cp ' + dos_dir + '/vasprun.xml  ./dos-vasprun.xml')

        # 3rd run to obtain Band structure
        band = MPNonSCFSet.from_prev_calc(static_dir,
                                          mode="line",
                                          standardize=True,
                                          user_incar_settings=myset)
        band.write_input(band_dir)
        run_vasp(cmd, band_dir)
        os.system('cp ' + band_dir + '/vasprun.xml  ./band-vasprun.xml')
        os.system('cp ' + band_dir + '/KPOINTS  ./')

        v = BSVasprun(band_dir+"/vasprun.xml")
        bs = v.get_band_structure(line_mode=True)
        plt = BSPlotter(bs)
        plt.get_plot(vbm_cbm_marker=True, ylim=[-4, 4])
        plt.save_plot(Name+'-band.png', img_format='png')

        shutil.rmtree(band_dir)
        shutil.rmtree(dos_dir)
        shutil.rmtree(static_dir)

    os.chdir('../')
