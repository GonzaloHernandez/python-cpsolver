#====================================================================
# Simple Constraint (Satisfaction/Optimization) Programming Solver 
# Testing version 1.3
#
# Gonzalo Hernandez
# gonzalohernandez@hotmail.com
# 2024
#
# Modules:
#   examples
#====================================================================

import os,sys
os.system("clear")

sys.path.insert(1,".")
from PythonCPSolver.engine import *

#-------------------------------------------------------

V = pa,pb,pc = IntVarArray(3,5,6,'v')

c1 = AllDifferent( [pa,pb,pc] )
c2 = Constraint( (pa <= pb) & (pb <= pc) )

#-------------------------------------------------------
U = ua,ub,uc = IntVarArray(3,0,2,'u')

ga = Constraint( ua == count([pb,pc],pa) )
gb = Constraint( ub == count([pa,pc],pb) )
gc = Constraint( uc == count([pa,pb],pc) )

fa = minimize(ga)
fb = minimize(gb)
fc = minimize(gc)
#-------------------------------------------------------

eq = Equilibrium( V, U, [ga,gb,gc], [fa,fb,fc], [c2] )

S = Engine( V, [eq,c1,c2] ).search(ALL)

for s in S : print( toInts(s) )
