from pymatgen import MPRester
from pymatgen.core.periodic_table import Element
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.analysis.phase_diagram import PhaseDiagram
import os
import warnings
from optparse import OptionParser

warnings.filterwarnings("ignore")


def parse_system(input):
    if input.find('-') > 0:
        return input.split('-')
    else:
        return input


def output_struc(entry, eng):
    id = entry.entry_id
    todo = mpr.get_structure_by_material_id(id)
    finder = SpacegroupAnalyzer(todo, symprec=tol, angle_tolerance=5)
    newStruc = finder.get_refined_structure()
    if len(newStruc.frac_coords) > 16:
        newStruc = newStruc.get_primitive_structure()
    p1 = ['{:6.3f}'.format(j) for j in newStruc.lattice.abc]
    p2 = ['{:6.2f}'.format(j) for j in newStruc.lattice.angles]
    sym = finder.get_space_group_symbol()
    s = ' '.join(map(str, p1+p2))
    print('%-16s %40s %6.3f %10s [%s]' % (id, s, eng, sym, newStruc.formula))
    return newStruc


if __name__ == "__main__":
    # ------------------------------------------------------------------
    # -------------------------------- Options -------------------------
    parser = OptionParser()
    parser.add_option("-c", "--cut", dest="cutoff", metavar='cutoff',
                      type='float', default=0,
                      help="cutoff energy for e_above_hull")
    parser.add_option("-d", "--dim", dest="dimension", type='int',
                      help="export all dimensions", metavar="dimension")
    parser.add_option("-e", "--element", dest="element", type='string',
                      help="chemical system", metavar="element")
    parser.add_option("-f", "--format", dest="format", default='poscar',
                      help="export structure in which format, poscar or cif",
                      metavar="dimension")

    (options, args) = parser.parse_args()

    mpr = MPRester('9RTlN5ZOXst6PAdS')
    system = parse_system(options.element)

    if type(system) is not list:
        mp_entries = mpr.get_entries(system)
    else:
        mp_entries = mpr.get_entries_in_chemsys(system)
        pd = PhaseDiagram(mp_entries)
        if options.dimension is None:
            options.dimension = len(system)

    if options.format == 'poscar':
        filename = 'MPR.vasp'
    else:
        filename = 'MPR.cif'

    if os.path.isfile(filename):
        os.remove(filename)

    tol = 0.01
    for entry in mp_entries:
        accept = False
        if type(system) is list:
            if len(entry.composition) >= options.dimension:
                eng = pd.get_e_above_hull(entry)
                if eng <= options.cutoff:
                    accept = True
        else:
            eng = entry.energy_per_atom
            accept = True

        if accept:
            struc = output_struc(entry, eng)
            if options.format == 'poscar':
                content = struc.to(fmt='poscar')
            else:
                content = CifWriter(struc, symprec=0.01).write_file()
            with open(filename, 'a+') as f:
                f.writelines(content)
