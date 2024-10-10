# Check out the documentation

[View the PDF](https://drive.google.com/file/d/1gRh-pOGc-uszRlNpsD0_x2uHuYQN9rTa/view?usp=sharing)

## Installation

If your goal is to use this software for solving basic combinatorial problems or to evaluate its functionality, there is no need to clone the repository. In that case, you can directly install the package from the Python Package Index using the following command:

```
pip install PythonCPSolver
```

However, if you intend to modify the code to develop your own algorithms or methods, which aligns with the primary purpose of this software, you are welcome to clone the source code. The code has been designed to be as straightforward as possible, making it easy to understand and work with each module.

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