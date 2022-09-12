from pymatgen.core.periodic_table import Element
from optparse import OptionParser
from pymatgen.io.vasp.outputs import Vasprun
from vasprun import vasprun
from pymatgen.entries.compatibility import MaterialsProjectCompatibility
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen import MPRester
from pymatgen.analysis.phase_diagram import PhaseDiagram
import os
import pandas as pd
from tabulate import tabulate
import collections

def first_2chars(x):
    return(x[:3])
def get_subdir(a_dir):
    return sorted([name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))])
def get_symbol(elements):
    symbol=[]
    for i in my_entry.composition.elements:
        symbol.append(i.symbol)
    return symbol
#-------------------------------------------------------------------
parser = OptionParser()
parser.add_option("-d",  "--dir", dest='dir', default='.',
                  help="by directory")
(options, args) = parser.parse_args()

pd.set_option('precision', 3)
output = collections.OrderedDict(
          {'formula': [],
          'Space group': [],
          'E_formation': [],
          'E_above_hull': [],
          })

filename = 'static-vasprun.xml'
csvname = 'stability.csv'
#-------------------------------------------------------------------
if os.path.exists(csvname):
    output0 = pd.read_csv(csvname)
    output = collections.OrderedDict(
          {'formula':     output0.formula.values.tolist(),
          'Space_group':  output0.Space_group.values.tolist(),
          'E_formation':  output0.E_formation.values.tolist(),
          'E_above_hull': output0.E_above_hull.values.tolist(),
          'Dir':          output0.Dir.values.tolist(),
          })

else:
    output = collections.OrderedDict(
          {'formula': [],
          'Space_group': [],
          'E_formation': [],
          'E_above_hull': [],
          'Dir': [],
          })

mpr = MPRester('fn8WQGgT9rvZAh6H')
compat = MaterialsProjectCompatibility()  # sets energy corrections and +U/pseudopotential choice
dirs = get_subdir(options.dir)
os.chdir(options.dir)
fname = ''
for dir in dirs:
    path = dir+'/'+filename
    if dir not in output['Dir']:
        try:
    	    if vasprun(path).error:
                print('vasp calculation is not converged')
    	    else:
                vaspcal = Vasprun(path)
                my_entry = vaspcal.get_computed_entry(inc_structure=True)
                struc = my_entry.structure
                spg = SpacegroupAnalyzer(struc,symprec=0.01).get_space_group_symbol()
                symbol = get_symbol(my_entry.composition.elements)
       	        entries = mpr.get_entries_in_chemsys(symbol)
                entries = compat.process_entries(entries)  
                N_exist = len(entries)
                corrections_dict = compat.get_corrections_dict(my_entry)
                if len(corrections_dict) > 0:
                    pretty_corrections = ["{}:{}".format(k, round(v, 3)) for k, v in corrections_dict.items()]
                    print("We are applying the following corrections (eV) to the user entry: {}".format(pretty_corrections))

                my_entry.correction = sum(corrections_dict.values())
                entries.append(my_entry)
                tmp = []
                for ele in symbol:
                    tmp.append(Element(ele))
                pda = PhaseDiagram(entries, elements=tmp)

                e_above_hull = pda.get_e_above_hull(entries[-1])
                e_form = pda.get_form_energy_per_atom(entries[-1])
                output['E_above_hull'].append(e_above_hull)
                output['E_formation'].append(e_form)
                output['formula'].append(struc.composition.get_reduced_formula_and_factor()[0])
                output['Space group'].append(spg)
                output['Dir'].append(dir)
        except:
    	    print('vasp error in ', dir)


df = pd.DataFrame(output)
df = df.sort_values(['E_above_hull', 'E_formation', 'formula'],
        ascending=[True, True, True])
print(tabulate(df, headers='keys', tablefmt='psql'))
df.to_csv(csvname)
print(len(df), ' structures have been processed')
