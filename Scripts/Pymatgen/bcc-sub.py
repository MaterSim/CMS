"""
Create an ase db file to store the information from the Sci. Rep. paper
"""
import os
import warnings
warnings.filterwarnings("ignore")

from pymatgen.ext.matproj import MPRester
from pyxtal import pyxtal

def process(pmg, id, spg, composition, comp):
    """
    check if this is a new structure

    Args:
        pmg: input structure
        refs: list of reference structures

    """
    s1 = pyxtal()
    try:
        s1.from_seed(pmg, tol=1e-3)
    except:
        print("wrong", pmg)
    if s1.group.number == 229 and len(s1.atom_sites)==1 and s1.atom_sites[0].wp.multiplicity==2:
        strs = '{:20s} {:3d} {:12s} {:6.2f}'.format(id, spg, composition.to_pretty_string(), comp)
        if comp > 0.45: 
            strs += '+++++++'
        print(strs)
        print(s1.atom_sites)


mpr = MPRester('fn8WQGgT9rvZAh6H') # insert your keys here

#define your search criteria
criteria ={#"band_gap": {"$gt":0.1},
           "spacegroup.number": {"$gt": 75},
           "nelements": {"$in": [2, 3]},
           "nsites": {"$lt": 60},
          }

#choose the properties which you are interested:
properties = [
              "material_id",
              "band_gap",
              "e_above_hull",
              "structure",
              "spacegroup.number",
              "composition_reduced",
              #"cif",
             ]
entries = mpr.query(criteria=criteria, properties=properties)
print("=============================Initial:", len(entries))
 

for i, entry in enumerate(entries):
    pmg = entry['structure']
    eles = [ele.symbol for ele in pmg.composition.elements]
    for ele in eles:
        pmg0 = pmg.copy()
        todo = [e0 for e0 in eles if e0 != ele]
        pmg0.remove_species(todo)
        comp = pmg.composition.fractional_composition.get_atomic_fraction(ele)
        process(pmg0, entry['material_id'], entry['spacegroup.number'], pmg.composition, comp)
