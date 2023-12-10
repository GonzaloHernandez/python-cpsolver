#====================================================================
# 
# Simple Constraint Programming Solver V1.1
# Gonzalo Hernandez
# 
# This file is inherited from solver.py
#====================================================================

import copy, math

#====================================================================

class Operable :
    def __add__(self, exp) :
        if isinstance(exp, int) : exp = IntVar(exp,exp)
        return Expression(self,"+",exp)

    def __sub__(self, exp) :
        if isinstance(exp, int) : exp = IntVar(exp,exp)
        return Expression(self,"-",exp)

    def __mul__(self, exp) :
        if isinstance(exp, int) : exp = IntVar(exp,exp)
        return Expression(self,"*",exp)

    def __mul__(self, exp) :
        if isinstance(exp, int) : exp = IntVar(exp,exp)
        return Expression(self,"*",exp)

    def __eq__(self, exp) :
        if isinstance(exp, int) : exp = IntVar(exp,exp)
        return Expression(self,"==",exp)

    def __ne__(self, exp) :
        if isinstance(exp, int) : exp = IntVar(exp,exp)
        return Expression(self,"!=",exp)

    def __lt__(self, exp) :
        if isinstance(exp, int) : exp = IntVar(exp,exp)
        return Expression(self,"<",exp)

    def __le__(self, exp) :
        if isinstance(exp, int) : exp = IntVar(exp,exp)
        return Expression(self,"<=",exp)

    def __gt__(self, exp) :
        if isinstance(exp, int) : exp = IntVar(exp,exp)
        return Expression(self,">",exp)

    def __ge__(self, exp) :
        if isinstance(exp, int) : exp = IntVar(exp,exp)
        return Expression(self,">=",exp)

    def __and__(self, exp) :
        if isinstance(exp, int) : exp = IntVar(exp,exp)
        return Expression(self,"&",exp)

    def __or__(self, exp) :
        if isinstance(exp, int) : exp = IntVar(exp,exp)
        return Expression(self,"|",exp)

#====================================================================

class IntVar (Operable) :
    
    INFINITE                            = 2147483647
    PRINT_NAME, PRINT_VALUE, PRINT_MIX  = 1,2,3

    #--------------------------------------------------------------
    def __init__(self, min=-INFINITE, max=INFINITE, name='_') -> None:
        self.min    = min
        self.max    = max
        self.name   = name

    #--------------------------------------------------------------
    def __str__(self) -> str:
        if self.isFailed() :
            return f"{self.name}()"
        elif self.isAssigned() :
            return f"{self.name}{{{str(self.min)}}}"
        else :
            return f"{self.name}{{{str(self.min)}..{str(self.max)}}}"        

    #--------------------------------------------------------------
    def toStr(self, view=PRINT_MIX) :
        if view == self.PRINT_VALUE :
            if self.isFailed() :
                return "_"
            elif self.isAssigned() :
                return f"{self.min}"
            else :
                return f"{{{str(self.min)}..{str(self.max)}}}"
            
        elif view == self.PRINT_NAME :
            if self.name == "_" :
                return str(self.min)
            else :
                return str(self.name)

        elif view == self.PRINT_MIX :
            if self.isFailed() :
                return f"{self.name}()"
            elif self.isAssigned() :
                return f"{self.name}{{{str(self.min)}}}"
            else :
                return f"{self.name}{{{str(self.min)}..{str(self.max)}}}"           

    #--------------------------------------------------------------
    def setge(self, val) :
        self.min = max(self.min, val)

    def setle(self, val) :
        self.max = min(self.max, val)

    def isAssigned(self) :
        return (self.min==self.max)
    
    def isFailed(self) :
        return (self.min>self.max)
    
    def card(self) :
        return self.max - self.min + 1
    
    def evaluate(self) :
        return [self.min, self.max]

    def project(self, newmin, newmax) :
        self.setge(newmin)
        self.setle(newmax)
        if newmin > newmax : return False

    def match(self, localvars, globalvars ) :
        for i,v in enumerate(globalvars) :
            if id(v)==id(self) :
                return localvars[i]
        return self

#====================================================================

class Expression (Operable) :
    def __init__(self, exp1, oper, exp2) -> None:
        self.exp1 = exp1
        self.oper = oper
        self.exp2 = exp2

    #--------------------------------------------------------------
    def __str__(self) -> str:
        if self.oper is None :
            return str(self.exp1)
        else :
            return "("+str(self.exp1) + self.oper + str(self.exp2)+")"

    #--------------------------------------------------------------
    def evaluate(self) :
        [lmin,lmax] = self.exp1.evaluate()
        [rmin,rmax] = self.exp2.evaluate()

        match self.oper :

            case "==" :
                if lmin == rmin == lmax == rmax :
                    self.min = self.max = 1
                elif lmin > rmax or rmin > lmax :
                    self.min = self.max = 0
                else :
                    [self.min, self.max] = [0,1]

            case "!=" :
                if lmax<rmin or rmax<lmin :
                    self.min = self.max = 1
                elif lmin == rmin == lmax == rmax :
                    self.min = self.max = 0
                else :
                    [self.min, self.max] = [0,1]

            case "<" :
                if lmax < rmin :
                    self.min = self.max = 1
                elif lmin >= rmax :
                    self.min = self.max = 0
                else :
                    [self.min, self.max] = [0,1]

            case ">" :
                if lmin > rmax :
                    self.min = self.max = 1
                elif lmax <= rmin :
                    self.min = self.max = 0
                else :
                    [self.min, self.max] = [0,1]

            case "<=" :
                if lmax <= rmin :
                    self.min = self.max = 1
                elif lmin > rmax :
                    self.min = self.max = 0
                else :
                    [self.min, self.max] = [0,1]

            case ">=" :
                if lmin >= rmax :
                    self.min = self.max = 1
                elif lmax < rmin :
                    self.min = self.max = 0
                else :
                    [self.min, self.max] = [0,1]

            case "&" :
                if lmin >= 1 and rmin >= 1 :
                    self.min = self.max = 1
                elif lmax <= 0 or rmax <= 0 :
                    self.min = self.max = 0
                else :
                    [self.min, self.max] = [0,1]

            case "|" :
                if lmin >= 1 or rmin >= 1 :
                    self.min = self.max = 1
                elif lmax <= 0 and rmax <= 0 :
                    self.min = self.max = 0
                else :
                    [self.min, self.max] = [0,1]

            case "+" :
                [self.min, self.max] = [lmin+rmin , lmax+rmax]
            case "-" :
                [self.min, self.max] = [lmin-rmax , lmax-rmin]
            case "*" :
                [self.min, self.max] = [
                    min(lmin*rmin, lmin*rmax, lmax*rmin, lmax*rmax),
                    max(lmin*rmin, lmin*rmax, lmax*rmin, lmax*rmax)
                ]

        return [self.min, self.max]

    #--------------------------------------------------------------
    def project(self, nmin, nmax) :
        if nmin > nmax : return False

        [lmin,lmax] = [self.exp1.min, self.exp1.max]
        [rmin,rmax] = [self.exp2.min, self.exp2.max]

        match self.oper :
            case "==" :
                if nmin == nmax == 1 :
                    if self.exp1.project( max(lmin,rmin), min(lmax,rmax) ) is False : return False
                    if self.exp2.project( max(lmin,rmin), min(lmax,rmax) ) is False : return False
                if nmin == nmax == 0 :
                    if rmin == rmax == lmin :
                        if self.exp1.project( lmin+1 , lmax ) is False : return False
                    if rmin == rmax == lmax :
                        if self.exp1.project( lmin , lmax-1 ) is False : return False
                    if lmin == lmax == rmin :
                        if self.exp2.project( rmin+1 , rmax ) is False : return False
                    if lmin == lmax == rmax :
                        if self.exp2.project( rmin , rmax-1 ) is False : return False
            case "!=" : 
                if nmin == nmax == 1 :
                    if rmin == rmax == lmin :
                        if self.exp1.project( lmin+1 , lmax ) is False : return False
                    if rmin == rmax == lmax :
                        if self.exp1.project( lmin , lmax-1 ) is False : return False
                    if lmin == lmax == rmin :
                        if self.exp2.project( rmin+1 , rmax ) is False : return False
                    if lmin == lmax == rmax :
                        if self.exp2.project( rmin , rmax-1 ) is False : return False
                if nmin == nmax == 0 :
                    if self.exp1.project( max(lmin,rmin), min(lmax,rmax) ) is False : return False
                    if self.exp2.project( max(lmin,rmin), min(lmax,rmax) ) is False : return False
            case "<" :
                if nmin == nmax == 1 :
                    if self.exp1.project( lmin  , rmax-1 ) is False : return False
                    if self.exp2.project( lmin+1, rmax   ) is False : return False
                if nmin == nmax == 0 :
                    if self.exp1.project( rmin, lmax ) is False : return False
                    if self.exp2.project( rmin, lmax ) is False : return False
            case ">" :
                if nmin == nmax == 1 :
                    if self.exp1.project( rmin+1, lmax   ) is False : return False
                    if self.exp2.project( rmin  , lmax-1 ) is False : return False
                if nmin == nmax == 0 :
                    if self.exp1.project( lmin, rmax ) is False : return False
                    if self.exp2.project( lmin, rmax ) is False : return False
            case "<=" :
                if nmin == nmax == 1 :
                    if self.exp1.project( lmin, rmax ) is False : return False
                    if self.exp2.project( lmin, rmax ) is False : return False
                if nmin == nmax == 0 :
                    if self.exp1.project( rmin+1, lmax   ) is False : return False
                    if self.exp2.project( rmin  , lmax-1 ) is False : return False
            case ">=" :
                if nmin == nmax == 1 :
                    if self.exp1.project( rmin, lmax ) is False : return False
                    if self.exp2.project( rmin, lmax ) is False : return False
                if nmin == nmax == 0 :
                    if self.exp1.project( lmin  , rmax-1 ) is False : return False
                    if self.exp2.project( lmin+1, rmax   ) is False : return False

            case "&" :
                if nmin == nmax == 1 :
                    if self.exp1.project( 1, lmax ) is False : return False
                    if self.exp2.project( 1, rmax ) is False : return False
                if nmin == nmax == 0 :
                    if rmin == rmax == 1 :
                        if self.exp1.project( lmin, 0 ) is False : return False
                    if lmin == lmax == 1 :
                        if self.exp2.project( rmin, 0 ) is False : return False
            case "|" :
                if nmin == nmax == 1 :
                    if rmin == rmax == 0 :
                        if self.exp1.project( 1, lmax ) is False : return False
                    if lmin == lmax == 0 :
                        if self.exp2.project( 1, rmax ) is False : return False
                if nmin == nmax == 0 :
                    if self.exp1.project( lmin, 0 ) is False : return False
                    if self.exp2.project( rmin, 0 ) is False : return False

            case "+" :
                if self.exp1.project( nmin-rmax , nmax-rmin ) is False : return False
                if self.exp2.project( nmin-lmax , nmax-lmin ) is False : return False
            case "-" :
                if self.exp1.project( nmin+rmin , nmax+rmax ) is False : return False
                if self.exp2.project( lmin-nmax , lmax-nmin ) is False : return False
            case "*" :
                if rmin == 0 : rmin = 1
                if rmax == 0 : rmax = 1
                
                [lmin,lmax] = [
                    min(nmin//rmin, nmin//rmax, nmax//rmin, nmax//rmax),
                    max(math.ceil(nmin/rmin), math.ceil(nmin*rmax), 
                        math.ceil(nmax*rmin), math.ceil(nmax*rmax))
                ]
                if self.exp1.project(lmin, lmax) is False : return False

                if lmin == 0 : lmin = 1
                if lmax == 0 : lmax = 1

                [rmin,rmax] = [
                    min(nmin//lmin, nmin//lmax, nmax//lmin, nmax//lmax),
                    max(math.ceil(nmin/lmin), math.ceil(nmin*lmax), 
                        math.ceil(nmax*lmin), math.ceil(nmax*lmax))
                ]
                if self.exp2.project(rmin, rmax) is False : return False
        return True

    #--------------------------------------------------------------
    def match(self, localvars, globalvars) :
        exp1 = self.exp1.match(localvars, globalvars)
        exp2 = self.exp2.match(localvars, globalvars)

        return Expression(exp1, self.oper, exp2)

#====================================================================

class Constraint :
    def __init__(self, exp) -> None:
        self.exp = exp

    def __str__(self) -> str:
        return str(self.exp)
    
    def prune(self) :
        self.exp.evaluate()
        return self.exp.project(1,1)
    
    def match(self, localvars, globalvars) :
        return Constraint( self.exp.match(localvars, globalvars) )
    
#====================================================================

class Globals :
    def __init__(self, optv, vars, func, sols, tops) -> None:
        self.optv = optv    # Current optimization value
        self.vars = vars    # Original variables
        self.func = func    # Optimization function [type,expression]
        self.optc = None    # Optimization (new) constraint
        self.sols = sols    # Solutions found
        self.tops = tops    # Amount of solutions required
        self.done = False   # Flag to stop searching

#====================================================================

class SearchInstance :
    def __init__(self, vars, cons, func, tops) -> None:
        self.vars = vars
        self.cons = cons
        self.glob = Globals([0], vars, func, [], tops)
    
    def isOptimizing(self) :
        return True if self.glob.func[0] > 0 else False

    def isMinimizing(self) :
        return True if self.glob.func[0] == 1 else False
    
    def isMaximizing(self) :
        return True if self.glob.func[0] == 2 else False

    def getFunValue(self) :
        return self.glob.optv[0]

    def evaluateFun(self) :
        localfun = self.glob.func[1].match(self.vars, self.glob.vars)
        return localfun.evaluate()[0]
    
    def setFunValue(self,v) :
        self.glob.optv[0] = v
    
    def getFun(self) :
        return self.glob.func[1]
    
    def propagate(self) :
        t1 = 0
        for v in self.vars : t1 += v.max - v.min + 1

        self.q = []
        for c in self.cons :
            self.q.append(c)
        
        if not self.glob.optc is None :
            c = self.glob.optc.match(self.vars, self.glob.vars)
            self.q.append(c)

        while self.q != [] :
            c = self.q.pop(0)
            if not c.prune() : return False

        t2 = 0
        for v in self.vars : t2 += v.max - v.min + 1

        if t2 < t1 :
            return self.propagate()
        else :
            return True

    #--------------------------------------------------------------
    def search(self) :
        if not self.propagate() : return []

        allAssigned = True
        for v in self.vars :
            if v.isFailed() :
                return []
            if not v.isAssigned() :
                allAssigned = False
                break

        if allAssigned :
            if self.isOptimizing() : 
                val = self.evaluateFun()
                if self.glob.sols == [] :
                    if self.isMaximizing() :
                        self.glob.optc = Constraint(
                            self.glob.func[1] > IntVar(val, IntVar.INFINITE) )
                    else :
                        self.glob.optc = Constraint(
                            self.glob.func[1] < IntVar(-IntVar.INFINITE, val) )
                else :
                    if self.isMaximizing() :
                        self.glob.optc.exp.exp2.setge( val )
                    else :
                        self.glob.optc.exp.exp2.setle( val )

                self.glob.sols = [ self.vars ]
                self.setFunValue( val )
            else : # Is satisfying
                self.glob.sols.append(self.vars)
                if len(self.glob.sols)==self.glob.tops : self.glob.done = True

        else :
            for i,v in enumerate(self.vars) :
                if self.glob.done : break
                if not v.isAssigned():
                    left    = self.clone()
                    right   = self.clone()

                    left    .vars[i].setle(left .vars[i].min)
                    right   .vars[i].setge(right.vars[i].min+1)
                    
                    left.search()
                    right.search()
                    break

    #--------------------------------------------------------------
    def clone(self) :
        branch = copy.copy(self)
        branch.vars, branch.cons = copy.deepcopy([self.vars, self.cons])
        return branch

#====================================================================

def solveModel(vars, cons, func=[0,None], tops=1) :
    model = copy.deepcopy([vars,cons,func])
    s = SearchInstance(model[0],model[1],model[2],tops)
    s.search()
    return s.glob.sols

#--------------------------------------------------------------

def IntVarArray(n,min,max,prefix='_') :
    vs = []
    for i in range(n) :
        name = prefix+str(i) if prefix != '_' else '_'
        vs.append(IntVar(min,max,name))
    return vs

#--------------------------------------------------------------

def printvars(vars, printview=IntVar.PRINT_MIX) :
    print("[ ",end="")
    for v in vars : 
        print(v.toStr(printview), end=" ")
    print("]")

#--------------------------------------------------------------

def count(vars,cond) :
    exp = vars[0]==cond
    for i in range(1,len(vars)):
        exp = exp + (vars[i]==cond)
    return exp

#--------------------------------------------------------------

def alldifferent(vars) :
    exp = vars[0] if len(vars)==1 else None
    for i in range(len(vars)-1):
        for j in range(i+1,len(vars)):
            if exp is None :
                exp = (vars[i] != vars[j])
            else :
                exp = exp & (vars[i] != vars[j])

    return exp

#--------------------------------------------------------------

def sum(vars) :
    exp = vars[0]
    for i in range(1,len(vars)):
        exp = exp + vars[i]
    return exp

#--------------------------------------------------------------

def minimize(exp) :
    return [1,exp]

#--------------------------------------------------------------

def maximize(exp) :
    return [2,exp]

#====================================================================
