This code `Extract_USPEX.py` is used for quick analysis of USPEX results solely from USPEX.mat. It has the following features:

- extract good structures by ranking of fitness (with the removal of duplicates)
- check if a desired structure has been found in USPEX

## Prerequisites
To use it, one must have python 3 installed. 
In addition, several packages will be required
- pymatgen
- pandans

One could follow the [wikipage](https://github.com/qzhu2017/CMS/wiki/Python-environment-setup) to set up your python environment.
```
$ python Extract_USPEX.py -h
Usage: Extract_USPEX.py [options]

Options:
  -h, --help            show this help message and exit
  -m FILE, --mat=FILE   MATLAB .mat file, default: USPEX.mat
  -n Max, --Nmax=Max    maximum number of strucs to output
  -c compare, --compare=compare
                        compare reference structure
  -t tol, --tolerance=tol
                        symmetry tolerance
  -e export, --export=export
                        export format: cif or poscar
```


## Extract good structures

```
$ python Extract_USPEX.py 
1420 structures have been loaded
Below are the selected low energy structures by removing the duplicates
+----+------+-----------+---------------+------------------------------------------+----------+-----------+
|    |   ID | Formula   | Space Group   | Cell                                     |   Energy |   Fitness |
|----+------+-----------+---------------+------------------------------------------+----------+-----------|
|  0 | 1211 | Ti4Se8    | C2/m          | 9.134  7.143  3.270  90.00 100.31 112.17 | -3.72337 |  -44.6804 |
|  1 |  714 | Ti4Se8    | C2/m          | 3.325  9.408  6.514  99.51 104.59  90.05 | -3.69974 |  -44.3969 |
|  2 |  923 | Ti4Se8    | C2/c          | 3.321  4.974 12.624  80.74  90.20 109.29 | -3.69794 |  -44.3753 |
|  3 | 1327 | Ti4Se8    | Cm            | 3.349  9.866  6.473  71.63 104.89  99.57 | -3.69537 |  -44.3444 |
|  4 |  544 | Ti4Se8    | Cmc2_1        | 3.306  9.416  6.494  90.03  75.37  90.00 | -3.69153 |  -44.2983 |
|  5 |  163 | Ti4Se8    | C2/m          | 6.128  6.458  6.135 118.00 114.00  79.17 | -3.69011 |  -44.2813 |
|  6 | 1053 | Ti4Se8    | C2/m          | 9.668  6.504  3.296  75.33  99.72 100.46 | -3.68417 |  -44.21   |
|  7 |  573 | Ti4Se8    | P-3m1         | 5.473  5.644  6.601  90.00  90.01  89.78 | -3.66893 |  -44.0272 |
|  8 |  949 | Ti4Se8    | Pnma          | 6.936  8.692  3.178  89.99  90.00  90.00 | -3.65972 |  -43.9166 |
```
In addition, a new file called `extracted.poscar` or `extracted.cif` will be generated.

## Check if the reference structure exists
```
$ python Extract_USPEX.py -c POSCAR
1011  5.951  6.945  6.191  67.32 116.88  89.64 P1              -3.340   Random      0
1012  6.517  6.765  4.953  89.24 108.76  75.17 P1              -3.447 Permutate     0
1013  6.630  4.928  6.421 100.32  75.61  78.40 P-1             -3.561 Permutate     0
1014  4.861  6.630  6.428 104.97  91.40  89.87 C2/m            -3.595 Permutate     0
1015  4.685  9.452  4.799  89.18  79.05  86.13 P1              -3.211  Heredity     0
1016  5.869  6.096  5.872  86.27  85.44  80.43 P1              -3.428  Heredity     0
1017  3.297  7.460  8.596  95.68 100.96 102.75 Cm              -3.438  Heredity     0
1018  6.139  6.206  6.109  88.13  75.57 112.73 P1              -3.446   Random      0
1019  8.481  7.204  3.323  90.04  89.85 107.15 C2/m            -3.696 softmutate    0
1020  9.134  7.143  3.270  90.00 100.31 112.17 C2/m            -3.723 softmutate    1
```
The search will start from the 1st structure and stop when the structure was found at the first place.



