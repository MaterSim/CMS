#!/usr/bin/env python
# encoding: utf-8

'''
    $Author: Qiang Zhu $
    Export cif file from POSCAR
'''


from optparse import OptionParser
from pymatgen.io.cif import CifWriter
from pymatgen.io.vasp import Poscar
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

# ------------------------------------------------------------------
# -------------------------------- Options -------------------------
parser = OptionParser()
parser.add_option('-i', '--input',   help='input POSCAR file')
parser.add_option('-o', '--output',  help='output cif file')
parser.add_option('-t', '--tolerance', type=float, default=0.001, help='')

(options, args) = parser.parse_args()

tol = options.tolerance
p = Poscar.from_file(options.input)
finder = SpacegroupAnalyzer(p.structure,
                            symprec=tol,
                            angle_tolerance=5)
print('Space group:', finder.get_space_group_symbol(), 'tolerance:', tol)
print(finder.get_symmetrized_structure())

CifWriter(p.structure, symprec=tol).write_file(options.output)
