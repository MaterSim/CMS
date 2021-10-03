#!/usr/bin/env  python
class Element:
    def __init__(self, input_value):
        self.input = input_value
        # list with atomic number z, short name, full name, valence, 
                # valence electrons, covalent radius, good bonds, Maximum CN:
        self.elements_list = [
            (1, 'H', 'Hydrogen',    1.0, 1, 0.31, 0.20, 1),
            (2, 'He', 'Helium',     0.5, 2, 0.28, 0.05, 0),
            (3, 'Li', 'Lithium',    1.0, 1, 1.28, 0.10, 6),
            (4, 'Be', 'Beryllium',  2.0, 2, 0.96, 0.20, 6),
            (5, 'B', 'Boron',       3.0, 3, 0.84, 0.30, 3),
            (6, 'C', 'Carbon',      4.0, 4, 0.70, 0.50, 4),
            (7, 'N', 'Nitrogen',    3.0, 5, 0.71, 0.50, 3),
            (8, 'O', 'Oxygen',      2.0, 6, 0.66, 0.30, 2),
            (9, 'F', 'Fluorine',    1.0, 7, 0.57, 0.10, 1),
            (10, 'Ne', 'Neon',      0.5, 8, 0.58, 0.05, 0),
            (11, 'Na', 'Sodium',    1.0, 1, 1.66, 0.05, 6),
            (12, 'Mg', 'Magnesium', 2.0, 2, 1.41, 0.10, 6),
            (13, 'Al', 'Aluminium', 3.0, 3, 1.21, 0.20, 6),
            (14, 'Si', 'Silicon',   4.0, 4, 1.11, 0.30, 4),
            (15, 'P', 'Phosphorus', 3.0, 5, 1.07, 0.30, 3),
            (16, 'S', 'Sulfur',     2.0, 6, 1.05, 0.20, 2),
            (17, 'Cl', 'Chlorine',  1.0, 7, 1.02, 0.10, 1),
            (18, 'Ar', 'Argon',     0.5, 8, 1.06, 0.05, 0),
            (19, 'K', 'Potassium',  1.0, 1, 2.03, 0.05, 0),
            (20, 'Ca', 'Calcium',   2.0, 2, 1.76, 0.10, 0),
            (21, 'Sc', 'Scandium',  3.0, 3, 1.70, 0.20, 0),
            (22, 'Ti', 'Titanium',  4.0, 4, 1.60, 0.30, 0),
            (23, 'V', 'Vanadium',   4.0, 5, 1.53, 0.30, 0),
            (24, 'Cr', 'Chromium',  3.0, 6, 1.39, 0.25, 0),
            (25, 'Mn', 'Manganese', 4.0, 5, 1.39, 0.30, 0),
            (26, 'Fe', 'Iron',      3.0, 3, 1.32, 0.25, 0),
            (27, 'Co', 'Cobalt',    3.0, 3, 1.26, 0.25, 0),
            (28, 'Ni', 'Nickel',    2.0, 3, 1.24, 0.15, 0),
            (29, 'Cu', 'Copper',    2.0, 2, 1.32, 0.10, 0),
            (30, 'Zn', 'Zinc',      2.0, 2, 1.22, 0.10, 0),
            (31, 'Ga', 'Gallium',   3.0, 3, 1.22, 0.25, 0),
            (32, 'Ge', 'Germanium', 4.0, 4, 1.20, 0.50, 0),
            (33, 'As', 'Arsenic',   3.0, 5, 1.19, 0.35, 0),
            (34, 'Se', 'Selenium',  2.0, 6, 1.20, 0.20, 0),
            (35, 'Br', 'Bromine',   1.0, 7, 1.20, 0.10, 0),
            (36, 'Kr', 'Krypton',   0.5, 8, 1.16, 0.05, 0),
            (37, 'Rb', 'Rubidium',  1.0, 1, 2.20, 0.05, 0),
            (38, 'Sr', 'Strontium', 2.0, 2, 1.95, 0.10, 0),
            (39, 'Y', 'Yttrium',    3.0, 3, 1.90, 0.20, 0),
            (40, 'Zr', 'Zirconium', 4.0, 4, 1.75, 0.30, 0),
            (41, 'Nb', 'Niobium',   5.0, 5, 1.64, 0.35, 0),
            (42, 'Mo', 'Molybdenum',4.0, 6, 1.54, 0.30, 0),
            (43, 'Tc', 'Technetium',4.0, 5, 1.47, 0.30, 0),
            (44, 'Ru', 'Ruthenium', 4.0, 3, 1.46, 0.30, 0),
            (45, 'Rh', 'Rhodium',   4.0, 3, 1.42, 0.30, 0),
            (46, 'Pd', 'Palladium', 4.0, 3, 1.39, 0.30, 0),
            (47, 'Ag', 'Silver',    1.0, 2, 1.45, 0.05, 0),
            (48, 'Cd', 'Cadmium',   2.0, 2, 1.44, 0.10, 0),
            (49, 'In', 'Indium',    3.0, 3, 1.42, 0.20, 0),
            (50, 'Sn', 'Tin',       4.0, 4, 1.39, 0.30, 0),
            (51, 'Sb', 'Antimony',  3.0, 5, 1.39, 0.20, 0),
            (52, 'Te', 'Tellurium', 2.0, 6, 1.38, 0.20, 0),
            (53, 'I', 'Iodine',     1.0, 7, 1.39, 0.10, 0),
            (54, 'Xe', 'Xenon',     0.5, 8, 1.40, 0.05, 0),
            (55, 'Cs', 'Caesium',   1.0, 1, 2.44, 0.05, 0),
            (56, 'Ba', 'Barium',    2.0, 2, 2.15, 0.10, 0),
            (57, 'La', 'Lanthanum', 3.0, 3, 2.07, 0.20, 0),
            (58, 'Ce', 'Cerium',    4.0, 3, 2.04, 0.30, 0),
            (59,'Pr','Praseodymium',3.0, 3, 2.03, 0.20, 0),
            (60, 'Nd', 'Neodymium', 3.0, 3, 2.01, 0.20, 0),
            (61, 'Pm', 'Promethium',3.0, 3, 1.99, 0.20, 0),
            (62, 'Sm', 'Samarium',  3.0, 3, 1.98, 0.20, 0),
            (63, 'Eu', 'Europium',  3.0, 3, 1.98, 0.20, 0),
            (64, 'Gd', 'Gadolinium',3.0, 3, 1.96, 0.20, 0),
            (65, 'Tb', 'Terbium',   3.0, 3, 1.94, 0.20, 0),
            (66, 'Dy', 'Dysprosium',3.0, 3, 1.92, 0.20, 0),
            (67, 'Ho', 'Holmium',   3.0, 3, 1.92, 0.20, 0),
            (68, 'Er', 'Erbium',    3.0, 3, 1.89, 0.20, 0),
            (69, 'Tm', 'Thulium',   3.0, 3, 1.90, 0.20, 0),
            (70, 'Yb', 'Ytterbium', 3.0, 3, 1.87, 0.20, 0),
            (71, 'Lu', 'Lutetium',  3.0, 3, 1.87, 0.20, 0),
            (72, 'Hf', 'Hafnium',   4.0, 3, 1.75, 0.30, 0),
            (73, 'Ta', 'Tantalum',  5.0, 3, 1.70, 0.40, 0),
            (74, 'W', 'Tungsten',   4.0, 3, 1.62, 0.30, 0),
            (75, 'Re', 'Rhenium',   4.0, 3, 1.51, 0.30, 0),
            (76, 'Os', 'Osmium',    4.0, 3, 1.44, 0.30, 0),
            (77, 'Ir', 'Iridium',   4.0, 3, 1.41, 0.30, 0),
            (78, 'Pt', 'Platinum',  4.0, 3, 1.36, 0.30, 0),
            (79, 'Au', 'Gold',      1.0, 3, 1.36, 0.05, 0),
            (80, 'Hg', 'Mercury',   2.0, 3, 1.32, 0.10, 0),
            (81, 'Tl', 'Thallium',  3.0, 3, 1.45, 0.20, 0),
            (82, 'Pb', 'Lead',      4.0, 4, 1.46, 0.30, 0),
            (83, 'Bi', 'Bismuth',   3.0, 5, 1.48, 0.20, 0),
            (84, 'Po', 'Polonium',  2.0, 6, 1.40, 0.20, 0),
            (85, 'At', 'Astatine',  1.0, 7, 1.50, 0.10, 0),
            (86, 'Rn', 'Radon',     0.5, 8, 1.50, 0.05, 0),
            (87, 'Fr', 'Francium',  1.0, 1, 2.60, 0.05, 0),
            (88, 'Ra', 'Radium',    2.0, 2, 2.21, 0.10, 0),
            (89, 'Ac', 'Actinium',  3.0, 3, 2.15, 0.20, 0),
            (90, 'Th', 'Thorium',   4.0, 3, 2.06, 0.30, 0),
            (91,'Pa','Protactinium',4.0, 3, 2.00, 0.30, 0),
            (92, 'U', 'Uranium',    4.0, 3, 1.96, 0.30, 0),
            (93, 'Np', 'Neptunium', 4.0, 3, 1.90, 0.30, 0),
            (94, 'Pu', 'Plutonium', 4.0, 3, 1.87, 0.30, 0),
            (95, 'Am', 'Americium', 4.0, 3, 1.80, 0.30, 0),
            (96, 'Cm', 'Curium',    4.0, 3, 1.69, 0.30, 0),
            (97, 'Bk', 'Berkelium', 4.0, 3, None, 0.30, 0),
            (98,'Cf','Californium', 4.0, 3, None, 0.30, 0),
            (99,'Es','Einsteinium', 4.0, 3, None, 0.30, 0),
            (100, 'Fm', 'Fermium',  4.0, 3, None, 0.30, 0),
            (101,'Md','Mendelevium',4.0, 3, None, 0.30, 0),
            (102, 'No', 'Nobelium', 4.0, 3, None, 0.30, 0),
            (103, 'Lr','Lawrencium',4.0, 3, None, 0.30, 0),
            (104,'Rf','Rutherfordium',4.0,3,None, 0.30, 0),
            (105, 'Db', 'Dubnium',  2.0, 3, None, 0.10, 0),
        ]
        self.z = None
        self.short_name = None
        self.long_name = None
        self.valence = None
        self.valence_electrons = None
        self.covalent_radius = None
        self.good_bonds = None
        self.CN = None
        pos = None
        try:
            int(self.input)
            self.z = self.input
            for i, el in enumerate(self.elements_list):
                if el[0] == self.z:
                    pos = i
                    self.short_name = el[1]
                    self.long_name = el[2]
                    break
        except ValueError:
            self.short_name = self.input
            for i, el in enumerate(self.elements_list):
                if el[1] == self.short_name:
                    pos = i
                    self.z = el[0]
                    self.long_name = el[2]
                    break
            if not self.z:
                self.short_name = None
                self.long_name = self.input
                for i, el in enumerate(self.elements_list):
                    if el[2] == self.long_name:
                        pos = i
                        self.z = el[0]
                        self.short_name = el[1]
                        break
                if not self.z:
                    self.long_name = None
        if pos is not None:
            self.valence = self.elements_list[pos][3]
            self.valence_electrons = self.elements_list[pos][4]
            self.covalent_radius = self.elements_list[pos][5]
            self.good_bonds = self.elements_list[pos][6]
            self.CN = self.elements_list[pos][7]
    def get_all(self, pos):
        els = []
        for el in self.elements_list:
            els.append(el[pos])
        return els
    def all_z(self):
        return self.get_all(0)
    def all_short_names(self):
        return self.get_all(1)
    def all_long_names(self):
        return self.get_all(2)
    def all_valences(self):
        return self.get_all(3)
    def all_valence_electrons(self):
        return self.get_all(4)
    def all_covalent_radii(self):
        return self.get_all(5)
    def all_good_bonds(self):
        return self.get_all(6)
    def all_CN(self):
        return self.get_all(7)
