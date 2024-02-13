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

os.system('clear')

sys.path.insert(1,'.')
from PythonCPSolver_Trail.engine import *

pw = IntVar(0,1,'pw')
pc = IntVar(0,1,'pc')
pl = IntVar(0,1,'pl')

uw = IntVar(0,1,'uw')
uc = IntVar(0,1,'uc')
ul = IntVar(0,1,'ul')

gw = Equation( uw == pw & pl)
gc = Equation( uc == 0 )
gl = Equation( ul == ((~pw & pc & pl) | (pw & ~pl)) ) 

nw = NashConstraint( [pw,pc,pl], 0, gw, maximize(uw) )
nl = NashConstraint( [pw,pc,pl], 2, gl, maximize(ul) )

e = Engine( 
    [pw,pc,pl] + [uw,uc,ul], 
    [gw,gc,gl] + [nw,nl] 
)

S = e.search(0)

for s in S :
    print( intVarArrayToStr(s,IntVar.PRINT_VALUE) )
