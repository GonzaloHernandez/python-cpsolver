import os,sys
os.system("clear")

sys.path.insert(1,".")
from PythonCPSolver_Trail.engine import *

w = IntVar(0,1,'w')
c = IntVar(0,1,'c')
l = IntVar(0,1,'l')

uw = IntVar(0,1,'uw')
uc = IntVar(0,1,'uc')
ul = IntVar(0,1,'ul')

a1,a2,a3,a4 = IntVarArray(4,0,1)

gw = maximize(uw)
gl = maximize(ul)

c1 = Equation( a1 == (w and l) )
c2 = Equation( a2 == (~w and l) )
c3 = Equation( a3 == (a2 and c) )
c4 = Equation( a4 == (w and ~l) )

e = Engine(
    [   
        w,c,l,uw,uc,ul,a1,a2,a3,a4
    ],

    [   Equation( uw == a1 ),
        Equation( a1 == (w and l) ),

        Equation( uc == 0 ),

        Equation( ul == (a3 + a4)),
        Equation( a2 == (~w and l) ),
        Equation( a3 == (a2 and c) ),
        Equation( a4 == (w and ~l) )
    ]
)

S = e.search(0)

for s in S :
    print(intVarArrayToStr(s))