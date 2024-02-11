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

x = IntVar(0,1,'x')
y = IntVar(0,1,'y')

ux = IntVar(0,3,'ux')
uy = IntVar(0,3,'uy')

gx = Equation( ux == ( (y*2)-x+1 ) )
gy = Equation( uy == ( (x*2)-y+1 ) )

nx = NashConstraint( [x,y], 0, gx, minimize(ux) )
ny = NashConstraint( [x,y], 1, gy, minimize(uy) )

e = Engine( 
    [x,y] + [ux,uy], 
    [gx,gy] + [nx,ny] 
)

S = e.search(0)

for s in S :
    print( intVarArrayToStr(s,IntVar.PRINT_VALUE) )
