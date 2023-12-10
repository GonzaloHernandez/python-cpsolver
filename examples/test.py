import os,sys
os.system("clear")

sys.path.insert(1,".")
from PythonCPSolver import *

x = IntVar(0,5,'x')
y = IntVar(0,3,'y')
z = IntVar(0,1,'z')

c = Constraint( x & y )
d = Constraint( x == 1 )
f = minimize(z-y)

S = solveModel(
    [x,y,z],
    [c], 
    f,
    tops=0
)

for s in S :
    printvars(s)
