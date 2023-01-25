#!/usr/bin/env python
import os
import numpy as np
from Element import Element
from ase.calculators.vasp import VaspChargeDensity
metals = ['Ba', 'Be', 'Ca', 'Cs', 'Fr', 'K', 'Li', 'Mg', 'Na', 'Ra', 
          'Rb', 'Sr', 'Al', 'Bi', 'Ga', 'In', 'Pb', 'Sn', 'Tl','Ac', 
          'Ag', 'Am', 'Au', 'Bk', 'Cd', 'Ce', 'Cf', 'Cm', 'Co', 'Cr', 
          'Cu', 'Dy', 'Er', 'Es', 'Eu', 'Fe', 'Fm', 'Gd', 'Hf', 'Hg', 
          'Ho', 'Ir', 'La', 'Lr', 'Lu', 'Md', 'Mn', 'Mo', 'Nb', 'Nd', 
          'Ni', 'No', 'Np', 'Os', 'Pa', 'Pd', 'Pm', 'Pr', 'Pt', 'Pu', 
          'Re', 'Rh', 'Ru', 'Sc', 'Sm', 'Ta', 'Tb', 'Tc', 'Th', 'Ti', 
          'Tm', 'U', 'V', 'W', 'Y', 'Yb', 'Zn', 'Zr']
def get_subdir(a_dir):
   return sorted([name for name in os.listdir(a_dir)
           if os.path.isdir(os.path.join(a_dir, name))])
 
class elf:
    """
    parse electride from a directory containing 
    ELFCAR, PARCHG and vasprun.xml
    """

    def __init__(self, path = './', 
                 cmd = 'gtimeout -t 30 -T 50 bader ',
                 ELF_min = 0.20):

        self.error = None
        self.ELF_maxima = []

        ELFCAR_path = path + '/ELFCAR'
        clean_cmd1 = 'rm ELFCAR-m bader_log ACF.dat BCF.dat AVF.dat'

        cell, coor, symbols, radii, grid = self.Read_ELFCAR(ELFCAR_path, ELF_min)
        os.system(cmd + 'ELFCAR-m > bader_log')
        if os.path.exists('BCF.dat') is False:
            self.error = 'bader error in parsing ELFCAR'
        else:
            self.ELF_maxima, self.fac1 = self.Read_BCF('BCF.dat', symbols, radii, cell)
        os.system(clean_cmd1)
        self.elf_max = self.Read_ELF(ELFCAR_path, self.ELF_maxima)
        
    @staticmethod
    def Read_ELF(filename, poss):
        test0 = VaspChargeDensity(filename)
        chg = np.array(test0.chg)
        grids = np.shape(chg)[1:]
        vol = test0.atoms[0].get_volume()
        elf_max=[]
        step = 2
        for pos in poss:
            x_min, x_max = int(pos[0]*grids[0])-step, int(pos[0]*grids[0])+step
            y_min, y_max = int(pos[1]*grids[1])-step, int(pos[1]*grids[1])+step
            z_min, z_max = int(pos[2]*grids[2])-step, int(pos[2]*grids[2])+step
            if x_min < 0: x_min=0
            if y_min < 0: y_min=0
            if z_min < 0: z_min=0
            if x_max >= grids[0]: x_max=grids[0]-1
            if y_max >= grids[1]: y_max=grids[1]-1
            if z_max >= grids[2]: z_max=grids[2]-1
            elf_max.append(vol*np.max(chg[0, x_min:x_max, y_min:y_max, z_min:z_max]))
        if elf_max:
            return max(elf_max)
        else:
            return 0
 
    @staticmethod
    def Read_BCF(filename, symbols, radii, cell):
        f = open(filename, 'rb')
        input_content = f.readlines()
        f.close()
        pos = []
        count = 0
        cell = np.linalg.inv(cell)
        for i in range(len(input_content)):
            s = input_content[i].split()
            if s[0].isdigit():
               a=[float(f) for f in s]
               if a[-1]>2.0 or ((symbols[int(a[-2])-1] in metals) and (1.2*radii[int(a[-2])-1] < a[-1])):
                  count += 1
                  if len(pos) < 4:
                     pos.append(np.dot(np.array(a[1:4]), cell))
        if len(pos) > 0:
           fac = count/len(pos)
        else:
           fac = 1.0
        return np.array(pos), fac
   
    @staticmethod
    def Read_ELFCAR(filename, ELF_min):
        """
        This module reads ELFCAR
        """
        f = open(filename, 'rb')
        f1 = open('ELFCAR-m', 'w')
        input_content = f.readlines()
        f.close()
        count = 0
        cell = []      #cell vector
        coor = []
        ELF_raw = []
        N_atoms = 0    #how many lines before getting ELF grid
        grid = []
        for line in input_content: #[:20]: 
            line=str(line,'utf-8')
            count = count + 1
            if count < 3:
               f1.write(line)
            elif (count>=3) and (count<=5):
               cell.append([float(f) for f in line.split()])
               f1.write(line)
            elif count==6:
               f1.write(line)
               symbol = line.split()
            elif count==7:
               f1.write(line)
               numIons = [int(f) for f in line.split()]
               N_atoms = sum(numIons)
               f1.write('Direct\n')
            elif (count>=9) and (count<9+N_atoms):
               f1.write(line)
               coor.append([float(f) for f in line.split()])
            elif count == 10+N_atoms:
               f1.write('\n')
               f1.write(line)
               grid = [int(f) for f in line.split()]
            elif count > 10+N_atoms:
               ELF_raw = line.split()
               for i, f in enumerate(ELF_raw):
                   if float(f)<ELF_min:
                      f = '0.00000'
                   if i==0:
                      f1.write('%8s' % (f))
                   else:
                      f1.write('%12s' % (f))
               f1.write('\n')
        f1.close()
    
        radii = np.array([])
        symbols = []
        for ele in range(len(symbol)):
            for i in range(numIons[ele]): 
                symbols.append(symbol[ele])
            tmp = Element(symbol[ele]).covalent_radius*np.ones(numIons[ele])
            radii= np.append(radii, tmp)
        cell = np.array(cell)
        return cell, coor, symbols, radii, grid


from optparse import OptionParser
if __name__ == "__main__":
    #------------------------------------------------------------------
    #-------------------------------- Options -------------------------
    parser = OptionParser()
    parser.add_option("-d", "--directory", dest="dir", default='./',
                      help="directory containing PARCHG and ELFCAR", metavar="dir")
    parser.add_option("-p",  "--pdir", dest='pdir',
                  help="by parent directory")

    (options, args) = parser.parse_args()    
    total_dir = []
    if options.pdir is None:
       total_dir.append(options.dir)
    else:
       total_dir =  get_subdir(options.pdir)
       os.chdir(options.pdir)	

    for subdir in total_dir:
        if os.path.exists(subdir+'/ELFCAR'):
            #try:
            test = elf(subdir)
            print(subdir, test.elf_max)
            #except:
            #    pass
