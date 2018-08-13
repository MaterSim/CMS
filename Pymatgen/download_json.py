import json
from pymatgen import MPRester

mpr = MPRester('fn8WQGgT9rvZAh6H')
bs=mpr.get_bandstructure_by_material_id('mp-3315').as_dict() #,line_mode=True)
with open("test.json", "w") as outfile:
    json.dump(bs, outfile, indent=4)
