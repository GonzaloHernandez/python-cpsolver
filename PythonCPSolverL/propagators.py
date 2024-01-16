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
#       conflictdriven.py
#====================================================================

from PythonCPSolverL.variables import *

#====================================================================

class AllDifferent :
    def __init__(self, vars) -> None:
        self.vars = vars

    def __str__(self) -> str:
        return self.toStr()

    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        return "alldifferent("+intVarArrayToStr(self.vars ,printview)+")"

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

class Linear :
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

class LinearArgs :
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

class Equation :
    def __init__(self, exp) -> None:
        self.exp = exp

    def __str__(self) -> str:
        return self.toStr()

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

class Clause :
    def __init__(self, lits) -> None:
        self.lits   = lits
        pass

    #--------------------------------------------------------------
    def __str__(self) -> str:
        return self.toStr()

    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        text = "[ "
        for l in self.lits : 
            text += l.toStr(printview)
            text += " | " if id(l) != id(self.lits[len(self.lits)-1]) else " "
        text += "]"
        return text 

    #--------------------------------------------------------------
    def prune(self) :
        lit  = None
        flag = False
        confict = True
        for l in self.lits :
            if not l.var.isAssigned() :
                confict = False
                if not lit is None :
                    flag = False
                    break
                else :
                    flag = True
                    lit = l
            else :
                if l.alt is True and l.var.min == 1 :
                    confict = False
                    flag = False
                    break
                if l.alt is False and l.var.min == 0 :
                    confict = False
                    flag = False
                    break

        if confict is True :
            return False
        
        if flag is True:
            if lit.alt is True :
                if not lit.setMin(1,self) : return False
            else :
                if not lit.setMax(0,self) : return False

        return True