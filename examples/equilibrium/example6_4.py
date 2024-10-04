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
from PythonCPSolver.engine import *

x = IntVar(2,3,'x')
y = IntVar(0,2,'y')
z = IntVar(1,2,'z')

ux = IntVar(0,1,name='ux')
uy = IntVar(0,1,name='uy')
uz = IntVar(0,1,name='uz')

gx = Constraint( ux == (x==y+z) )
gy = Constraint( uy == (y==x-z) )
gz = Constraint( uz == (x+1==y+z) )


V = [x,y,z]
U = [ux,uy,uz]
G = [gx,gy,gz]
F = []

C = [
    EquilibriumDB(V,U,G)
]

e = Engine(V,C)

S = e.search(ALL)

for s in S :
    print(toInts(s))

