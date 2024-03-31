# Instructions

## LAMMPS Setup:

```
https://github.com/lammps/lammps.git
cd lammps/src
make yes-ml-snap
make yes-ml-iap
make mpi -j 4
#make serial -j 4
```

This will generate `lmp_mpi` or `lmp_serial` under `lammps/src`

## To run lammps under this directory

```
path/lmp_serial < in.snap 
```

will generate the file called `dump.sna` like the following

```
ITEM: TIMESTEP
0
ITEM: NUMBER OF ATOMS
127047
ITEM: BOX BOUNDS xy xz yz pp pp pp
-1.1007964152930020e+02 1.1007964152930020e+02 0.0000000000000000e+00
-9.2904966335464692e+01 9.2904966335464692e+01 0.0000000000000000e+00
-2.4271622472917425e+01 2.4271622472917425e+01 0.0000000000000000e+00
ITEM: ATOMS c_sna[1] c_sna[2] c_sna[3] c_sna[4] c_sna[5] c_sna[6] c_sna[7] c_sna[8] c_sna[9] c_sna[10] c_sna[11] c_sna[12] c_sna[13] c_sna[14] c_sna[15] c_sna[16] c_sna[17] c_sna[18] c_sna[19] c_sna[20] c_sna[21] c_sna[22] c_sna[23] c_sna[24] c_sna[25] c_sna[26] c_sna[27] c_sna[28] c_sna[29] c_sna[30]
2234.88 363.922 -53.2756 65.6995 7.00217 -9.63047 2.15077 13.605 -13.2488 -5.54597 -4.99489 -3.81596 -8.62127 41.0945 -4.42841 -9.18208 -1.51172 -6.04085 -2.32267 -11.1238 329.357 15.9159 12.7838 -2.39306 2.06609 33.3937 675.625 2.75217 3.37779 64.585
```

This will store the 30-length array for each atom to represent it local environment based on the snap descriptor.
One can run clustering like PCA to identify the unique groups of atomics and check if they make sense.
In future, one can try other descriptors as well.
