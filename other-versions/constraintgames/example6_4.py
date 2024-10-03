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

x = IntVar(2,3,'x')
y = IntVar(0,2,'y')
z = IntVar(1,2,'z')

ux = IntVar(0,1,name='ux')
uy = IntVar(0,1,name='uy')
uz = IntVar(0,1,name='uz')

V = [x,y,z]
U = [ux,uy,uz]
G = [
    Constraint( ux == (x==y+z) ),
    Constraint( uy == (y==x-z) ),
    Constraint( uz == (x+1==y+z) )
]
C = []
F = []

e = EngineGame(V,U,C,G,F)
# e = Engine(V+U,C+G)

S = e.search(ALL)

for s in S :
    print(s)
    # print(intVarArrayToIntArray(s))