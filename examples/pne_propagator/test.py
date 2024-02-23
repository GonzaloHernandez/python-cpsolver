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

px,py,pz = IntVarArray(3,1,3,'v')
ux,uy,uz = IntVarArray(3,-30,30,'u')

gx = Equation( ux == px + py + pz)
gy = Equation( uy == px * py * pz)
gz = Equation( uz == px - py - pz)

fx = maximize(ux)
fy = maximize(uy)
fz = maximize(uz)

# c2 = Equation( (px==2) & (py==1))
c1 = PNE_Eager([px,py,pz],[ux,py,uz],[gx,gy,gz],[],[fx,fy,fz])


e = Engine( [px,py,pz] + [ux,uy,uz],
            [gx,gy,gz] + [c1]
            )

S = e.search(0)

for s in S :
    print(intVarArrayToStr(s, IntVar.PRINT_VALUE))


