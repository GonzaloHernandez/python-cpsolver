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
from PythonCPSolver_Trail.engine import *

x = IntVar(1,9)
y = IntVar(1,9)
z = IntVar(1,3)

ux,uy,uz = IntVarArray(3,0,1)

gx = Equation( ux == (x == y*z) )
gy = Equation( uy == (y == x*z) )
gz = Equation( uz == ( (x*y <= z) & (z <= x+y) & ((x+1)*(y+1) != z*3) ))

fx = maximize(ux)
fy = maximize(uy)
fz = maximize(uz)

c = PNE([x,y,z],[ux,uy,uz],[gx,gy,gz],[],[fx,fy,fz])

S = Engine( [x,y,z], [c] ).search(ALL)

# for s in S :
#     print(intVarArrayToStr(s,IntVar.PRINT_VALUE))