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

gw = Constraint( uw == pw & pl)
gc = Constraint( uc == 0 )
gl = Constraint( ul == ((~pw & pc & pl) | (pw & ~pl)) ) 

cw = NashConstraint([pw,pc,pl],0,gw,maximize(uw))
cc = NashConstraint([pw,pc,pl],1,gc,maximize(uc))
cl = NashConstraint([pw,pc,pl],2,gl,maximize(ul))

e = EngineGame( [pw,pc,pl], [uw,uc,ul], [cw,cc,cl], [gw,gc,gl] )

S = e.search(ALL)

for s in S :
    print(s)