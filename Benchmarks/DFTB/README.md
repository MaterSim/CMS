# DFTB+

This is an exmple of geometry optimization of a molecuar crystal with DFTB+.

Although DFTB+ calculation can be automated throught ASE, there exist a bug when choosing the `MaxAngularMomentum`. For the given input, ASE generates:

```
   MaxAngularMomentum = { 
      C = "p" 
      H = "s" 
      O = "p" 
      S = "p" 
   }
```
But the MaxAngularMomentun for S is `d`, not `p`. Otherwise, the geometry will become wrong!

The relevant dicussion can be found at: 
https://gitlab.com/ase/ase/-/issues/542
