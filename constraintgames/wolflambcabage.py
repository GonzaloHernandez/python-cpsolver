#====================================================================
# Simple Constraint (Satisfaction/Optimization) Programming Solver 
# Testing version 1.3
#
# Gonzalo Hernandez
# gonzalohernandez@hotmail.com
# 2023
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

gw = Equation( uw == pw & pl)
gc = Equation( uc == 0 )
gl = Equation( ul == ((~pw & pc & pl) | (pw & ~pl)) ) 

e = EngineGame( [pw,pc,pl], [uw,uc,ul], [], [gw,gc,gl] )

S = e.search(ALL)

for s in S :
    print(s)