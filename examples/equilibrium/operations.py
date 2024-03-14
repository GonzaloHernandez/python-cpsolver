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

px,py,pz = IntVarArray(3,  1, 3,'v')
ux,uy,uz = IntVarArray(3,-30,30,'u')

gx = Constraint( ux == px + py + pz)
gy = Constraint( uy == px * py * pz)
gz = Constraint( uz == px - py - pz)

fx = maximize(ux)
fy = maximize(uy)
fz = maximize(uz)

c1 = Constraint( (px==2) & (py==1))
c2 = Equilibrium([px,py,pz],[ux,uy,uz],[gx,gy,gz],[fx,fy,fz],[c1])

e = Engine( 
    [px,py,pz]  + [ux,uy,uz],
    [c1,c2] + [gx,gy,gz]
)

S = e.search(ALL)

for s in S :
    print(intVarArrayToStr(s, IntVar.PRINT_VALUE))


