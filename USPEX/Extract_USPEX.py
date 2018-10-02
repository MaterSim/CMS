#!/usr/bin/env  python
# encoding: utf-8

'''
$Author: Qiang Zhu $
$Date: 2018-10-01 18:38:44  $
1, to check if USPEX calc generates the reference structure:
$ python Extract_USPEX.py -c POSCAR

2, to extract good structures from the calculation
$ python Extract_USPEX.py 
'''

import os
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
import pymatgen as mg
import pymatgen.analysis.structure_matcher as sm
from optparse import OptionParser
import scipy.io as sio
import numpy as np
import pandas as pd
from tabulate import tabulate
from pymatgen.io.vasp import Poscar
from pymatgen.io.cif import CifWriter

def export_structure(struc, filename, fileformat='poscar'):
    """export incar"""
    with open(filename, 'w') as f:
        for s in struc:
            if fileformat == 'poscar':
                content = s.to(fmt='poscar') 
            else:
                content = CifWriter(struc, symprec=0.01).write_file()
            f.writelines(content)

#------------------------------------------------------------------
#-------------------------------- Options -------------------------
parser = OptionParser()
parser.add_option("-m", "--mat", dest="matfile", default='USPEX.mat',
                  help="MATLAB .mat file, default: USPEX.mat", metavar="FILE")
parser.add_option("-n", "--Nmax", dest="Nmax", default=30, type='int',
                  help="maximum number of strucs to output", metavar="Max")
parser.add_option("-c", "--compare", dest="compare",
                  help="compare reference structure", metavar="compare")
parser.add_option("-t", "--tolerance", dest="tol", default=0.05, type='float',
                  help="symmetry tolerance", metavar="tol")
parser.add_option("-e", "--export", dest="export", default='poscar', 
                  help="export format: cif or poscar", metavar="export")

(options, args) = parser.parse_args()

if not os.path.exists(options.matfile):
    error_str = 'No ' + options.matfile + ' file found.'
    parser.error(error_str)

matfile = options.matfile
mat = sio.loadmat(matfile, struct_as_record=True)
POP = mat['USPEX_STRUC']

POPULATION = POP['POPULATION']
N_struc    = POPULATION[0][0].shape[1]
print('{0:d} structures have been loaded'.format(N_struc))

Nmax = options.Nmax
parser.destroy()

#-------------------------------------------------------------------
Element = []
for i in POP['SYSTEM'][0][0][0][0][1][0,:]: Element.append(' '.join(map(str, i)))

Struc  = []
Energy = []
Origin = []
Fitness = []
for i in range(N_struc):
    coord   = POPULATION[0][0]['COORDINATES'][0][i]
    lattice = POPULATION[0][0]['LATTICE'][0][i]
    numIons = POPULATION[0][0]['numIons'][0][i]
    howcome = POPULATION[0][0]['howCome'][0][i][0]
    energy  = POPULATION[0][0]['Enthalpies'][0][i][0][-1]
    fitness = POPULATION[0][0]['Fitness'][0][i][0][-1]

    s = [];
    for el,num in zip(Element,numIons[0]): s = s + ([el]*num)
    Struc.append(mg.Structure(lattice, s, coord))
    Origin.append(howcome)
    Energy.append(energy/sum(numIons[0]))
    Fitness.append(fitness)

if options.compare:
    # check 
    s1 = mg.Structure.from_file(options.compare)
    for i, s0 in enumerate(Struc):
        dist = sm.StructureMatcher().fit(s1, s0)
        p1 = ['{:6.3f}'.format(j) for j in s0.lattice.abc]
        p2 = ['{:6.2f}'.format(j) for j in s0.lattice.angles]
        s  =  ' '.join(map(str,p1+p2))
        spg = SpacegroupAnalyzer(s0, symprec=options.tol).get_space_group_symbol()
        print('{0:4d} {1:40s} {2:12s} {3:9.3f} {4:10s} {5:4b}'.format(i+1, s, spg, Energy[i], Origin[i], dist))
        if dist:
            break
else:
    Fitness  = np.array(Fitness)
    Ranking = np.argsort(Fitness)
    ids = [Ranking[0] + 1]
    struc_out = [Struc[Ranking[0]]]
    energy_out = [Energy[Ranking[0]]]
    fitness_out = [Fitness[Ranking[0]]]
    for i in Ranking[1:]:
        inc = True
        s0 = Struc[i]
        for s1 in struc_out:
            if sm.StructureMatcher().fit(s0, s1):
                inc = False
                break
        if inc:
            struc_out.append(s0)
            energy_out.append(Energy[i])
            fitness_out.append(Fitness[i])
            ids.append(i+1)

        if len(struc_out) == Nmax:
            break

    label_out = []
    spg_out = []
    formula_out = []
    for s0 in struc_out:
        p1 = ['{:6.3f}'.format(j) for j in s0.lattice.abc]
        p2 = ['{:6.2f}'.format(j) for j in s0.lattice.angles]
        s  =  ' '.join(map(str,p1+p2))
        label_out.append(s)
        spg_out.append(SpacegroupAnalyzer(s0, symprec=options.tol).get_space_group_symbol())
        formula_out.append(s0.formula.replace(" ",""))
    col = {'ID': ids,
           'Formula': formula_out,
           'Space Group': spg_out,
           'Cell': label_out,
           'Energy': energy_out,
           'Fitness': fitness_out,
          }
    
    df = pd.DataFrame(col)
    print('Below are the selected low energy structures by removing the duplicates')
    print(tabulate(df, headers='keys', tablefmt='psql'))
    filename = 'extracted.' + options.export 
    export_structure(struc_out, filename, fileformat=options.export)
    print('The extracted structure info has been saved to {0:s}'.format(filename))
