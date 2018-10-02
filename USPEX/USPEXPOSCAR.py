#!/usr/bin/env  /usr/local/bin/python
# encoding: utf-8
'''
$Rev: 629 $
'''
from optparse import OptionParser
#from pymatgen.io.cif import CifWriter
from pymatgen.io.vasp import Poscar
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
import pymatgen.analysis.structure_matcher as sm
import os, sys
import numpy as np

def getInput(begin_keyword, end_keyword, input_file, output_file):
        
    # Read INPUT  file
    f = open(input_file, 'rb')
    input_content = f.readlines()
    f.close()
    # Write OUTPUT file
    f1 = open(output_file, 'w')

    #--------------------------------------------------------------------
    # Process the case of keyblock:
    begin_num = None
    end_num   = None
    for i in xrange(len(input_content)):
        if input_content[i].find(begin_keyword) >= 0:
            begin_num = i  
            break
    if cmp(begin_keyword, end_keyword) == 0:
       end_num = len(input_content) - 1
       #print end_num
    else:
       for i in xrange(len(input_content)):
           if input_content[i].find(end_keyword) >= 0:
               end_num = i - 1
               break
    
    if begin_num is not None and end_num is not None:
        for i in xrange(begin_num, end_num+1):
            f1.write(input_content[i].strip()+'\n')
    else:
        print begin_keyword
        print end_keyword 
        print "does not exist...."
    f1.close()


def getList(input_file):
    # Read INPUT  file
    f = open(input_file, 'rb')
    input_content = f.readlines()
    f.close()
    # Process the case of keyblock:
    #-------------------------------------------------------------------
    ID = []
    for i in xrange(len(input_content)):
        s = input_content[i].split()[0]
        if s.isdigit():
           ID.append(int(s)) 
    return ID

def getNum(keyword, input_file):
        
    # Read INPUT  file
    f = open(input_file, 'rb')
    input_content = f.readlines()
    f.close()
    #------------------------------------------------------------------
    # Process the case of keyblock:
    begin_num = None
    end_num   = None
    count = 0;
    for i in xrange(len(input_content)):
        if input_content[i].find(keyword) >= 0:
           count = count + 1
    return count   
#-------------------------------------------------------------------------   
#------------------------------ Main Program -----------------------------
#-------------------------------- Options --------------------------------
input_file = sys.argv[1]
N_structure = getNum('EA', input_file)
print 'Reading input from ', input_file
print 'Total number of structures: ', N_structure
input_content = getList(sys.argv[2])

if len(sys.argv) == 4 :
   tol = float(sys.argv[3])
else:
   tol = 0.05
#-------------------------------------------------------------------------
output_file1= 'POSCAR_tmp'
output_file2= 'POSCAR_todo'
output_file= 'good_POSCAR'

print 'Writing output in  ', output_file
print 'Total number of structures: ', len(input_content)

#-------------------------------------------------------------------------
if os.path.isfile(output_file):
        os.remove(output_file)

Struc  = []
List = []
for i in xrange(len(input_content)):
    begin = str(int(input_content[i]))
    List.append(begin)
    if input_content[i] == N_structure :
        end   = begin
    else :
        end   = str(int(input_content[i]) + 1)

    s1    = 'EA' + begin
    s2    = 'EA' + end
    getInput(s1,s2, input_file, output_file1)
    p = Poscar.from_file(output_file1)
    Struc.append(p.structure)

ID = 1
occu = np.ones((len(Struc),), dtype=np.int)
Nmax = len(Struc)
bad_struc = 0
while ID < Nmax:
    for i in range(0,ID):
        if occu[i]> 0 and sm.StructureMatcher().fit(Struc[ID],Struc[i]):
           occu[i] += occu[ID]
           occu[ID] = 0
           bad_struc += 1
           print 'Same structure between ', List[ID], ' and ', List[i]
           break
    ID = ID + 1


print '---------------------------------------------'
print 'Symmetrized structure in tolerance:', tol
print '---------------------------------------------'
for i in range(len(Struc)):
    if occu[i] > 0:
       finder = SpacegroupAnalyzer(Struc[i],symprec=tol,angle_tolerance=5)
       newStruc = finder.get_refined_structure()
       if len(newStruc.frac_coords) > 20:
          newStruc = newStruc.get_primitive_structure()

       newStruc.to(filename=output_file2)
       #print finder.get_refined_structure()
       p1 = ['{:6.3f}'.format(j) for j in newStruc.lattice.abc]
       p2 = ['{:6.2f}'.format(j) for j in newStruc.lattice.angles]
       sym = finder.get_space_group_symbol()
       s  =  ' '.join(map(str,p1+p2))
       print 'ID%-4s %40s %10s [%s]' % (List[i], s, sym, newStruc.formula)
       with open(output_file, 'a+') as outFile:
            with open(output_file2, 'rb') as com:
                  outFile.write(com.read())
#--------------------------------------------------------------------------
os.remove(output_file1)
os.remove(output_file2)
       
sys.exit(0)

