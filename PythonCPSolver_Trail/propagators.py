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

    #--------------------------------------------------------------
    def __str__(self) -> str:
        return self.toStr()

    #--------------------------------------------------------------
    def setEngine(self, engine) :
        pass

#====================================================================

class AllDifferent(Propagator) :
    def __init__(self, vars) -> None:
        Propagator.__init__(self, )
        self.vars = vars

    #--------------------------------------------------------------
    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        return 'alldifferent('+intVarArrayToStr(self.vars ,printview)+')'

    #--------------------------------------------------------------
    def prune(self) :
        for v1 in self.vars :
            if v1.isAssigned() :
                for v2 in self.vars :
                    if id(v1) != id(v2) :
                        if v1.min == v2.min :
                            if not v2.project(
                                v2.min+1, 
                                v2.max ) : return False
                        if v1.max == v2.max :
                            if not v2.project(
                                v2.min, 
                                v2.max-1 ) : return False
        return True

#====================================================================

class Linear(Propagator) :
    def __init__(self, vars, vart) -> None:
        if isinstance(vart, int) : vart = IntVar(vart,vart)
        self.vars   = vars
        self.vart   = vart

    #--------------------------------------------------------------
    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        return str(self.vars)+' = '+str(self.valt)
    
    #--------------------------------------------------------------
    def prune(self) :
        maxs, mins = 0, 0
        for v in self.vars :
            maxs += v.max
            mins += v.min
        if not self.vart.project( mins, maxs ) : return False

        for v1 in self.vars :
            maxs, mins = 0, 0
            for v2 in self.vars :
                if id(v1) != id(v2) :
                    maxs += v2.max
                    mins += v2.min
            if not v1.project(
                self.vart.min-maxs, 
                self.vart.max-mins ) : return False
        return True

#====================================================================

class LinearArgs(Propagator) :
    def __init__(self, args, vars, vart) -> None:
        if isinstance(vart, int) : vart = IntVar(vart,vart)
        self.args   = args
        self.vars   = vars
        self.vart   = vart

    #--------------------------------------------------------------
    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        return str(self.vars)+' = '+str(self.valt)
    
    #--------------------------------------------------------------
    def prune(self) :
        maxs, mins = 0, 0
        for i,v in enumerate(self.vars) :
            if self.args[i] >= 0 :
                maxs += v.max * self.args[i]
                mins += v.min * self.args[i]
            else :
                maxs += v.min * self.args[i]
                mins += v.max * self.args[i]

        if not self.vart.project( mins, maxs ) : return False

        for i1,v1 in enumerate(self.vars) :
            maxs, mins = 0, 0
            for i2,v2 in enumerate(self.vars) :
                if id(v1) != id(v2) :
                    if (self.args[i1] >= 0 and self.args[i2] >= 0) or \
                       (self.args[i1]  < 0 and self.args[i2] < 0):                        
                        maxs += v2.max * self.args[i2]
                        mins += v2.min * self.args[i2]
                    else :
                        maxs += v2.min * self.args[i2]
                        mins += v2.max * self.args[i2]
            if self.args[i1] >= 0 :
                if not v1.project(
                    math.floor((self.vart.min - maxs)/self.args[i1]), 
                    math.ceil ((self.vart.max - mins)/self.args[i1])) : return False
            else :
                if not v1.project(
                    math.floor((mins - self.vart.max)/(self.args[i1]*-1)), 
                    math.ceil ((maxs - self.vart.min)/(self.args[i1]*-1))) : return False

        return True

#====================================================================
    
class Equation(Propagator) :
    def __init__(self, exp) -> None:
        self.exp = exp

    #--------------------------------------------------------------
    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        return self.exp.toStr(printview)
    
    #--------------------------------------------------------------
    def prune(self) :
        self.exp.evaluate()
        return self.exp.project(1,1)
    
    #--------------------------------------------------------------
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
        self.util   = self.func[EXPR]
        self.optc   = None

        if self.func[TYPE] ==  MAXIMIZE:
            self.optc = Equation(
                self.util >= IntVar( self.util.min, IntVar.INFINITE) )
        else :      # if is MINIMIZE
            self.optc = Equation(
                self.util <= IntVar(-IntVar.INFINITE, self.util.max) )

    #--------------------------------------------------------------
    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        return 'NashConstraint propagator'
    
    #--------------------------------------------------------------
    def setEngine(self, engine) :
        optv = self.optc.exp.exp2
        optv.setEngine( engine )

    #--------------------------------------------------------------
    def prune(self) :
        newvars,newgoal,newutil,newfunc \
            = copy.deepcopy([self.vars, self.goal, self.util, self.func])

        newfunc[TYPE] = MINIMIZE if self.func[TYPE] == MAXIMIZE else MAXIMIZE

        optv = self.optc.exp.exp2

        newvars[self.pi].min = self.oriv.min
        newvars[self.pi].max = self.oriv.max

        e = engine.Engine(
            [newutil] + newvars ,
            [newgoal],
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
        # return True


#====================================================================

class PNE(Propagator) :
    def __init__(self, V,U,G,C=[],F=[]) -> None:
        self.V,     \
        self.U,     \
        self.G,     \
        self.C,     \
        self.F      = copy.deepcopy( [V,U,G,C,F] )
        
        self.vars   = V
        self.cons   = []

        self.Nash   = []
        self.BR     = []
        self.cnt    = []
        self.n      = len(V)

        for i in range(self.n) : 
            self.BR.append([])
            self.cnt.append(1)
            for m in range(self.n) :
                if i !=m :
                    self.cnt[i] *= V[m].card()
        
        pass

    #--------------------------------------------------------------
    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        return 'NashConstraint propagator'
    
    #--------------------------------------------------------------
    def prune(self) :

        allAssigned = True
        for v in self.vars :
            if not v.isAssigned() :
                allAssigned = False
                break

        if allAssigned :
            s = []
            for v in self.vars :
                s.append( IntVar(v.min, v.max, v.name) )

            t = intVarArrayToIntArray(s)
            self.checkNash(t, self.n-1)

        for c in self.cons :
            if not c.prune() : return False

        return True

    #--------------------------------------------------------------
    def checkNash(self,t,i) :
        if i<0 :
            if t not in self.Nash :
                self.Nash.append(t)
                print('PNE: ',end='')
                print(t)
        else :
            d = self.search_table(t,i)
            if d == [] :
                d = self.findBestResponse(t,i)
                
                if d == [] :
                    
                    C = []
                    for j in range(len(self.V)) :
                        if j != i :
                            C.append( Equation( self.V[j] == t[j] ) )
                    
                    S = engine.Engine(self.V + self.U , self.C + self.G + C ).search(ALL)

                    for s in S :
                        dt = intVarArrayToIntArray(s,self.n)
                        d.append(dt)

                self.insert_table(i,d)
                if self.cnt[i] == 0 :
                    self.cons.append( Equation( self.vars[i] <= t[i]) )
                else :
                    self.cnt[i] -= 1

            if t in d :
                self.checkNash(t,i-1)

    #--------------------------------------------------------------
    def findBestResponse(self,t,i) :
        C = []
        for j in range(len(self.V)) :
            if j != i :
                C.append( Equation( self.V[j] == t[j] ) )

        S = []
        if self.F == [] :
            C.append( Equation( self.U[i] == 1))
            S = engine.Engine( self.V + self.U , self.C + self.G + C).search(ALL)
        else :
            F = self.F[i]
            E = engine.Engine( self.V + self.U , self.C + self.G + C, F )
            S = E.search()

            if S != [] :
                if F[TYPE]==MAXIMIZE :  val = E.optc.exp.exp2.min
                else :                  val = E.optc.exp.exp2.max

                C.append( Equation( self.U[i] == val ) )
                S = engine.Engine( self.V + self.U , self.C + self.G + C).search(ALL)

        d = []
        for s in S :
            dt = []
            for j in range(self.n) :
                dt.append(s[j].min)
            d.append(dt)

        return d

    #--------------------------------------------------------------
    def checkEndOfTable(self,i) :
        for t in self.BR[i] :
            self.checkNash(t,self.n-1)

    #--------------------------------------------------------------
    def search_table(self,t,i) :
        if len(self.BR[i]) <= 0 : return []

        br = []

        for b in range(len(self.BR[i])) :
            if self.BR[i][b][0:i]+self.BR[i][b][i+1:self.n] == t[0:i]+t[i+1:self.n] :
                br.append( self.BR[i][b] )
        return br

    #--------------------------------------------------------------
    def insert_table(self,i,d) :
        for t in d :
            if t not in self.BR[i] :
                self.BR[i].append(t)
