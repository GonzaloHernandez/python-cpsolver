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
from PythonCPSolver.engine import *

pw = IntVar(0,1,'pw')
pc = IntVar(0,1,'pc')
pl = IntVar(0,1,'pl')

uw = IntVar(0,1,'uw')
uc = IntVar(0,1,'uc')
ul = IntVar(0,1,'ul')

gw = Constraint( uw == pw & pl)
gc = Constraint( (uc == 0) | (uc==1) )
gl = Constraint( ul == ((~pw & pc & pl) | (pw & ~pl)) ) 

e = Engine( 
    [pw,pc,pl] + [uw,uc,ul], 
    [gw,gc,gl] #+ [Equilibrium([pw,pc,pl],[uw,uc,ul],[gw,gc,gl])]
)

S = e.search(ALL)

for s in S :
    print( toStrs(s,IntVar.PRINT_VALUE) )
