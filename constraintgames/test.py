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
from constraintgames.ConstraintCPSolver import *

pw,pc,pl = IntVarArray(3,0,1)
uw,uc,ul = IntVarArray(3,0,1)
de       = IntVar(0,1)

gw = Equation( uw == pw & pl)
gc = Equation( uc == 0 )
gl = Equation( ul == ((~pw & pc & pl) | (pw & ~pl)) ) 

c = PNE( [pw,pc,pl], [uw,uc,ul], [gw,gc,gl] )

e = Engine( [pw,pc,pl], [c] )

S = e.search(0)

for s in S :
    print(intVarArrayToStr(s, IntVar.PRINT_VALUE))

print('-------')
for s in c.Nash :
    print(s)
