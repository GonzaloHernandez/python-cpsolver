import os,sys
os.system("clear")

sys.path.insert(1,".")
from PythonCPSolver import *

x = IntVar(5,7,'x')
y = IntVar(5,7,'y')
z = IntVar(5,7,'z')
u = IntVar()

c = Constraint( u == count( [x,y,z] , 6 ))

S = solveModel(
    [x,y,z,u],
    [c], 
    tops=0
)

for s in S :
    printvars(s)