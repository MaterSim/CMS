#!/usr/bin/env  python
# encoding: utf-8

'''
    $Author: Qiang Zhu $
    Export cif file from POSCAR
'''


from optparse import OptionParser
import pymatgen as mg
from pymatgen.io.cif import CifWriter

# ------------------------------------------------------------------
# -------------------------------- Options -------------------------
parser = OptionParser()
parser.add_option('-i', '--input',   help='input POSCAR file')
parser.add_option('-o', '--output',  help='output cif file')

(options, args) = parser.parse_args()
structure = mg.Structure.from_file(options.input)
structure.to(filename=options.output)
