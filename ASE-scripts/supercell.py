from ase.io import read, write
from ase import Atoms
from ase import geometry
from ase.build.supercells import make_supercell
import numpy as np

#Read structure from POSCAR, this is ase.atom object
struc = read('gra.vasp',format='vasp')

#make supercell here
P = np.array([[1,-1,0],[1,1,0],[0,0,1]])*2
gra1 = make_supercell(struc, P)

#After the lattice transformation
#the supercell might have unpleasant shape
#let's apply another transformation here
cell_par = gra1.get_cell_lengths_and_angles()
pos1 = gra1.get_scaled_positions()
cell1 = geometry.cell.cellpar_to_cell(cell_par)
gra1.set_cell(cell1)
gra1.set_scaled_positions(pos1)

#output in any format whichever you want
write('POSCAR',gra1, format='vasp')
