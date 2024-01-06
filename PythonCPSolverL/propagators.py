#====================================================================
# Simple Constraint (Satisfaction/Optimization) Programming Solver 
# Current version 1.3
#
# Gonzalo Hernandez
# gonzalohernandez@hotmail.com
# 2023
#
# Modules:
#   PythonCPSolver
#       engine.py
#       propagators.py
#       variables.py
#       brancher.py
#====================================================================

from PythonCPSolverL.variables import *


class Propagator :
    def setEngine(self, engine) :
        pass

#====================================================================

class AllDifferent(Propagator) :
    def __init__(self, vars) -> None:
        self.vars = vars

    def __str__(self) -> str:
        return str(self.vars)
    
    def prune(self) :
        for v1 in self.vars :
            if v1.isAssigned() :
                for v2 in self.vars :
                    if id(v1) != id(v2) :
                        if v1.min == v2.min :
                            if not v2.project( v2.min+1 , v2.max ) : return False
                        if v1.max == v2.max :
                            if not v2.project( v2.min , v2.max-1 ) : return False
        return True

#====================================================================

class Linear(Propagator) :
    def __init__(self, vars, vart) -> None:
        if isinstance(vart, int) : vart = IntVar(vart,vart)
        self.vars   = vars
        self.vart   = vart

    def __str__(self) -> str:
        return str(self.vars)+" = "+str(self.valt)
    
    def prune(self) :
        for v1 in self.vars :
            maxs, mins = 0, 0
            for v2 in self.vars :
                if id(v1) != id(v2) :
                    maxs += v2.max
                    mins += v2.min
            if not v1.project( self.vart.min-maxs, self.vart.max-mins ) : return False
        return True

#====================================================================

class LinearArgs(Propagator) :
    def __init__(self, args, vars, vart) -> None:
        if isinstance(vart, int) : vart = IntVar(vart,vart)
        self.args   = args
        self.vars   = vars
        self.vart   = vart

    def __str__(self) -> str:
        return str(self.vars)+" = "+str(self.valt)
    
    def prune(self) :
        for i1,v1 in enumerate(self.vars) :
            maxs, mins = 0, 0
            for i2,v2 in enumerate(self.vars) :
                if id(v1) != id(v2) :
                    maxs += v2.max * self.args[i2]
                    mins += v2.min * self.args[i2]
            if not v1.project( 
                math.ceil((self.vart.min - maxs)/self.args[i1]), 
                math.ceil((self.vart.max - mins)/self.args[i1])) : return False
        return True

#====================================================================

class Equation(Propagator) :
    def __init__(self, exp) -> None:
        self.exp = exp

    def __str__(self) -> str:
        return str(self.exp)
    
    def prune(self) :
        self.exp.evaluate()
        return self.exp.project(1,1)
    
    def match(self, localvars, globalvars) :
        return Equation( self.exp.match(localvars, globalvars) )
    
#====================================================================

def count(vars,cond) -> Expression:
    exp = vars[0]==cond
    for i in range(1,len(vars)):
        exp = exp + (vars[i]==cond)
    return exp

#--------------------------------------------------------------

def alldifferent(vars) -> Expression:
    exp = vars[0] if len(vars)==1 else None
    for i in range(len(vars)-1):
        for j in range(i+1,len(vars)):
            if exp is None :
                exp = (vars[i] != vars[j])
            else :
                exp = exp & (vars[i] != vars[j])

    return exp

#--------------------------------------------------------------

def sum(vars) -> Expression:
    exp = vars[0]
    for i in range(1,len(vars)):
        exp = exp + vars[i]
    return exp

#====================================================================

class Lazzy(Propagator) :
    def __init__(self,vars) -> None:
        self.vars   = vars  # Real variables
        self.lvars  = []    # Lazzy variables
        self.lcons  = []    # Lazzy constraint to link real variables
        self.ngood  = []    # No good constraints 
        self.delta  = []

        for v in self.vars :
            lv = IntVarArray( v.card(), 0,1, '#' )
            for i,vi in enumerate(lv) :
                self.lcons.append( Equation(vi == (v == i+v.min)) )
            self.lvars.append( lv )
            self.delta.append( v.min )

        # self.addNoGood( [self.lvars[0][1], self.lvars[1][1]] )

    def __str__(self) -> str:
        return "lazzyvars"

    def prune(self) :
        for c in self.lcons :
            if not c.prune() : return False

        for ng in self.ngood :
            target  = None
            perfect = False
            for v in ng :
                if not v.isAssigned() :
                    if not target is None :
                        perfect = False
                        break
                    else :
                        perfect = True
                        target = v
                else :
                    if v.min == 0 :
                        perfect = False
                        break
            if perfect :
                target.setMax(0)

        return True
    
    def setEngine(self, engine) :
        for lv in [item for row in self.lvars for item in row]:
            lv.setEngine( engine )
    
    def addNoGood(self, vars) :
        lv = []
        for i,v in enumerate(vars) :
            lv.append( self.lvars[i][v.val() - self.delta[i]] )

        self.ngood.append(lv)
