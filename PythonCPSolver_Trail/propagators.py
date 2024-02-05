#====================================================================
# Simple Constraint (Satisfaction/Optimization) Programming Solver 
# Current version 1.3 (Using a trail to undo a search)
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

from PythonCPSolver_Trail.variables import *

#====================================================================

class Propagator :
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return self.toStr()

    def setEngine(self, engine) :
        pass

#====================================================================

class AllDifferent(Propagator) :
    def __init__(self, vars) -> None:
        Propagator.__init__(self, )
        self.vars = vars

    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        return 'alldifferent('+intVarArrayToStr(self.vars ,printview)+')'

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

    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        return str(self.vars)+' = '+str(self.valt)
    
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

    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        return str(self.vars)+' = '+str(self.valt)
    
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

    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        return self.exp.toStr(printview)
    
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

import importlib, copy

engine = importlib.import_module('PythonCPSolver_Trail.engine')

class NashConstraint(Propagator) :
    def __init__(self, vars,pi,goal,func) -> None:
        self.vars   = vars
        self.oriv   = vars[pi]
        self.pi     = pi
        self.goal   = goal
        self.func   = func
        self.util   = self.func[1]
        self.optc   = None

        if self.func[0] ==  MAXIMIZE:
            self.optc = Equation(
                self.util >= IntVar( self.util.getVal(), IntVar.INFINITE) )
        else :      # if is MINIMIZE
            self.optc = Equation(
                self.util <= IntVar(-IntVar.INFINITE, self.util.getVal()) )

    #--------------------------------------------------------------
    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        return 'NashConstraint propagator'
    
    #--------------------------------------------------------------
    def setEngine(self, engine) :
        optv = self.optc.exp.exp2
        optv.setEngine( engine )

    #--------------------------------------------------------------
    def prune(self) :
        newvars,newgoal,newutil,newfunc = copy.deepcopy([self.vars, self.goal, self.util, self.func])

        newfunc[0]  = MINIMIZE if newfunc[0] == MAXIMIZE else MAXIMIZE

        optv        = self.optc.exp.exp2

        newvars[self.pi].min = self.oriv.min
        newvars[self.pi].max = self.oriv.max

        e = engine.Engine(
            [newutil] + newvars ,
            newgoal,
            newfunc
        )

        s = e.search()

        if s != [] :
            v = s[0][0]
            if self.func[0] ==  MAXIMIZE and self.util.getVal() > optv.min :
                optv.setge( v.getVal() )
                
            elif self.func[0] ==  MINIMIZE and self.util.getVal() < optv.min :
                optv.setle( v.getVal() )

        return self.optc.prune()
