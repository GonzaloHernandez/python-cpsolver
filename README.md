# Check out the documentation

[View the PDF](https://drive.google.com/file/d/1gRh-pOGc-uszRlNpsD0_x2uHuYQN9rTa/view?usp=sharing)

## Installation
pip install PythonCPSolver

## Usage

```
from PythonCPSolver import *

x1 = IntVar(1,10)
x2 = IntVar(5,15)

c1 = Constraint(x1>x2)
c2 = Constraint(x1==x2*2)

e = Engine([x1,x2],[c1,c2],minimize(x1))

ss = e.search()
for s in ss : print (toInts(s))
```