from pymatgen import MPRester
import numpy as np
import pandas as pd
from tabulate import tabulate

mpr = MPRester('fn8WQGgT9rvZAh6H')
gap_min, gap_max = 0.4, 1.2


tag = [1, 2, 3, 4]
for nele in tag:
    col_name = {'Formula': [],
                'Space group': [],
                'Material_id': [],
                'Gap': [],
                'e_above_hull': [],
                'N_sites': [],
                'Density': [],
                }
    
    entries = mpr.query(criteria={"band_gap": {"$lte": gap_max},
                                  "icsd_ids.0": {'$exists': True},
                                  "nsites": {"$lte": 10},
                                  "e_above_hull": {"$lte": 0.1},
                                  "nelements": nele,
                                 },
                        properties=["pretty_formula",
                                    "material_id",
                                    # "structure",
                                    "e_above_hull",
                                    "spacegroup.symbol",
                                    "band_gap",
                                    "nsites",
                                    "density",
                                   ]
                       )
    
    for entry in entries:
        if entry["band_gap"] > gap_min: 
            col_name['Formula'].append(entry['pretty_formula'])
            col_name['Space group'].append(entry['spacegroup.symbol'])
            col_name['Material_id'].append(entry['material_id'])
            col_name['e_above_hull'].append(entry['e_above_hull'])
            col_name['Gap'].append(entry['band_gap'])
            col_name['N_sites'].append(entry['nsites'])
            col_name['Density'].append(entry['density'])


    df = pd.DataFrame(col_name)
    df = df.sort_values(['Gap'], ascending=[True])
    df.to_csv('Gap_screen-'+str(nele)+'.csv')
    # print(tabulate(df, headers='keys', tablefmt='psql'))
