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

# import math

#====================================================================

EAGER       = -1    # Present solutions eagerly (ignored when optimizing)
ALL         = 0     # Store solutions in a list (ignored when optimizing)
LEFT        = 1     # For general purposes
RIGHT       = 2     # For general purposes

MIN         = 0     # Min value of a variable
MAX         = 1     # Max value of a variable

NONEOPTI    = 0     # Without optimization function
MINIMIZE    = 1     # With minimizing function
MAXIMIZE    = 2     # With maximizing function

TYPE        = 0     # Optimization function type
EXPR        = 1     # Optimization fucntion expression 

#====================================================================

class Operable :
    def __add__(self, exp) :
        if isinstance(exp, int) : exp = IntVar(exp,exp)
        return Expression(self,'+',exp)

    def __sub__(self, exp) :
        if isinstance(exp, int) : exp = IntVar(exp,exp)
        return Expression(self,'-',exp)

    def __mul__(self, exp) :
        if isinstance(exp, int) : exp = IntVar(exp,exp)
        return Expression(self,'*',exp)

    def __mul__(self, exp) :
        if isinstance(exp, int) : exp = IntVar(exp,exp)
        return Expression(self,'*',exp)

    def __eq__(self, exp) :
        if isinstance(exp, int) : exp = IntVar(exp,exp)
        return Expression(self,'==',exp)

    def __ne__(self, exp) :
        if isinstance(exp, int) : exp = IntVar(exp,exp)
        return Expression(self,'!=',exp)

    def __lt__(self, exp) :
        if isinstance(exp, int) : exp = IntVar(exp,exp)
        return Expression(self,'<',exp)

    def __le__(self, exp) :
        if isinstance(exp, int) : exp = IntVar(exp,exp)
        return Expression(self,'<=',exp)

    def __gt__(self, exp) :
        if isinstance(exp, int) : exp = IntVar(exp,exp)
        return Expression(self,'>',exp)

    def __ge__(self, exp) :
        if isinstance(exp, int) : exp = IntVar(exp,exp)
        return Expression(self,'>=',exp)

    def __and__(self, exp) :
        if isinstance(exp, int) : exp = IntVar(exp,exp)
        return Expression(self,'&',exp)

    def __or__(self, exp) :
        if isinstance(exp, int) : exp = IntVar(exp,exp)
        return Expression(self,'|',exp)

    def __invert__(self) :
       return Expression(self,'<',IntVar(1,1))

    def __neg__(self) :
        return Expression(IntVar(0,0),'-',self)

    def __pos__(self) :
        return self

#====================================================================

class IntVar (Operable) :
    
    INFINITE                            = 2147483647
    PRINT_NAME, PRINT_VALUE, PRINT_MIX  = 1,2,3

    #--------------------------------------------------------------
    def __init__(self, min=-INFINITE, max=INFINITE, name='_', engine=None) -> None:
        self.min    = min
        self.max    = max
        self.name   = name
        self.engine = engine

    #--------------------------------------------------------------
    def setEngine(self, engine) :
        self.engine = engine

    #--------------------------------------------------------------
    def __str__(self) -> str:
        return self.toStr()

    #--------------------------------------------------------------
    def toStr(self, view=PRINT_MIX) :
        if view == self.PRINT_VALUE :
            if self.isFailed() :
                return '_'
            elif self.isAssigned() :
                return f'{self.min}'
            else :
                return f'{{{str(self.min)}..{str(self.max)}}}'
            
        elif view == self.PRINT_NAME :
            if self.name == '_' :
                return str(self.min)
            else :
                return str(self.name)

        elif view == self.PRINT_MIX :
            if self.isFailed() :
                return f'{self.name}()'
            elif self.isAssigned() :
                return f'{self.name}{{{str(self.min)}}}'
            else :
                return f'{self.name}{{{str(self.min)}..{str(self.max)}}}'           

    #--------------------------------------------------------------
    def setMin(self, nmin) :
        if nmin  > self.max : return False
        if self.min == nmin : return True

        step = [self, LEFT, self.min, False]
        self.engine.trail.append( step )
        self.min = nmin
        return True

    #--------------------------------------------------------------
    def setMax(self, nmax) :
        if nmax  < self.min : return False
        if self.max == nmax : return True

        step = [self, RIGHT, self.max, False]
        self.engine.trail.append( step )
        self.max = nmax
        return True

    #--------------------------------------------------------------
    def setge(self, val) :
        self.min = max(self.min, val)

    def setle(self, val) :
        self.max = min(self.max, val)

    def isAssigned(self) :
        return (self.min==self.max)
    
    def isFailed(self) :
        return (self.min>self.max)
    
    def getVal(self) :
        return self.min
    
    def card(self) :
        return self.max - self.min + 1
    
    def evaluate(self) :
        return [self.min, self.max]

    #--------------------------------------------------------------
    def project(self, nmin, nmax) :
        if nmin > nmax : return False

        if not self.setMin( max(self.min, nmin) ) : return False
        if not self.setMax( min(self.max, nmax) ) : return False

        return True

    def match(self, localvars, globalvars ) :
        for i,v in enumerate(globalvars) :
            if id(v)==id(self) :
                return localvars[i]
        return self

#====================================================================

class Expression (Operable) :
    def __init__(self, exp1, oper, exp2) -> None:
        self.exp1 = exp1    # LEFT expression
        self.oper = oper    # Operator expression
        self.exp2 = exp2    # RIGHT expression

    #--------------------------------------------------------------
    def __str__(self) -> str:
        return self.toStr()

    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        if self.oper is None :
            return self.exp1.toStr(printview)
        else :
            text  = self.exp1.toStr(printview) 
            text += self.oper 
            text += self.exp2.toStr(printview)

            return '(' + text + ')'

    #--------------------------------------------------------------
    def evaluate(self) :
        [lmin,lmax] = self.exp1.evaluate()
        [rmin,rmax] = self.exp2.evaluate()

        match self.oper :

            case '==' :
                if lmin == rmin == lmax == rmax :
                    self.min = self.max = 1
                elif lmin > rmax or rmin > lmax :
                    self.min = self.max = 0
                else :
                    [self.min, self.max] = [0,1]

            case '!=' :
                if lmax<rmin or rmax<lmin :
                    self.min = self.max = 1
                elif lmin == rmin == lmax == rmax :
                    self.min = self.max = 0
                else :
                    [self.min, self.max] = [0,1]

            case '<' :
                if lmax < rmin :
                    self.min = self.max = 1
                elif lmin >= rmax :
                    self.min = self.max = 0
                else :
                    [self.min, self.max] = [0,1]

            case '>' :
                if lmin > rmax :
                    self.min = self.max = 1
                elif lmax <= rmin :
                    self.min = self.max = 0
                else :
                    [self.min, self.max] = [0,1]

            case '<=' :
                if lmax <= rmin :
                    self.min = self.max = 1
                elif lmin > rmax :
                    self.min = self.max = 0
                else :
                    [self.min, self.max] = [0,1]

            case '>=' :
                if lmin >= rmax :
                    self.min = self.max = 1
                elif lmax < rmin :
                    self.min = self.max = 0
                else :
                    [self.min, self.max] = [0,1]

            case '&' :
                if lmin >= 1 and rmin >= 1 :
                    self.min = self.max = 1
                elif lmax <= 0 or rmax <= 0 :
                    self.min = self.max = 0
                else :
                    [self.min, self.max] = [0,1]

            case '|' :
                if lmin >= 1 or rmin >= 1 :
                    self.min = self.max = 1
                elif lmax <= 0 and rmax <= 0 :
                    self.min = self.max = 0
                else :
                    [self.min, self.max] = [0,1]

            case '+' :
                [self.min, self.max] = [lmin+rmin , lmax+rmax]
            case '-' :
                [self.min, self.max] = [lmin-rmax , lmax-rmin]
            case '*' :
                [self.min, self.max] = [
                    min(lmin*rmin, lmin*rmax, lmax*rmin, lmax*rmax),
                    max(lmin*rmin, lmin*rmax, lmax*rmin, lmax*rmax)
                ]

        return [self.min, self.max]

    #--------------------------------------------------------------
    def evaluateSAT(self) -> bool :
        [min,max] = self.evaluate()
        if min>0 : return True
        if max<1 : return False
        return None    

    #--------------------------------------------------------------
    def project(self, nmin, nmax) :
        if nmin > nmax : return False

        [lmin,lmax] = [self.exp1.min, self.exp1.max]
        [rmin,rmax] = [self.exp2.min, self.exp2.max]

        match self.oper :
            case '==' :
                if nmin == nmax == 1 :
                    if not self.exp1.project( max(lmin,rmin), min(lmax,rmax) ) : return False
                    if not self.exp2.project( max(lmin,rmin), min(lmax,rmax) ) : return False
                if nmin == nmax == 0 :
                    if rmin == rmax == lmin :
                        if not self.exp1.project( lmin+1 , lmax ) : return False
                    if rmin == rmax == lmax :
                        if not self.exp1.project( lmin , lmax-1 ) : return False
                    if lmin == lmax == rmin :
                        if not self.exp2.project( rmin+1 , rmax ) : return False
                    if lmin == lmax == rmax :
                        if not self.exp2.project( rmin , rmax-1 ) : return False
            case '!=' : 
                if nmin == nmax == 1 :
                    if rmin == rmax == lmin :
                        if not self.exp1.project( lmin+1 , lmax ) : return False
                    if rmin == rmax == lmax :
                        if not self.exp1.project( lmin , lmax-1 ) : return False
                    if lmin == lmax == rmin :
                        if not self.exp2.project( rmin+1 , rmax ) : return False
                    if lmin == lmax == rmax :
                        if not self.exp2.project( rmin , rmax-1 ) : return False
                if nmin == nmax == 0 :
                    if not self.exp1.project( max(lmin,rmin), min(lmax,rmax) ) : return False
                    if not self.exp2.project( max(lmin,rmin), min(lmax,rmax) ) : return False
            case '<' :
                if nmin == nmax == 1 :
                    if not self.exp1.project( lmin  , rmax-1 ) : return False
                    if not self.exp2.project( lmin+1, rmax   ) : return False
                if nmin == nmax == 0 :
                    if not self.exp1.project( rmin, lmax ) : return False
                    if not self.exp2.project( rmin, lmax ) : return False
            case '>' :
                if nmin == nmax == 1 :
                    if not self.exp1.project( rmin+1, lmax   ) : return False
                    if not self.exp2.project( rmin  , lmax-1 ) : return False
                if nmin == nmax == 0 :
                    if not self.exp1.project( lmin, rmax ) : return False
                    if not self.exp2.project( lmin, rmax ) : return False
            case '<=' :
                if nmin == nmax == 1 :
                    if not self.exp1.project( lmin, rmax ) : return False
                    if not self.exp2.project( lmin, rmax ) : return False
                if nmin == nmax == 0 :
                    if not self.exp1.project( rmin+1, lmax   ) : return False
                    if not self.exp2.project( rmin  , lmax-1 ) : return False
            case '>=' :
                if nmin == nmax == 1 :
                    if not self.exp1.project( rmin, lmax ) : return False
                    if not self.exp2.project( rmin, lmax ) : return False
                if nmin == nmax == 0 :
                    if not self.exp1.project( lmin  , rmax-1 ) : return False
                    if not self.exp2.project( lmin+1, rmax   ) : return False

            case '&' :
                if nmin == nmax == 1 :
                    if not self.exp1.project( 1, lmax ) : return False
                    if not self.exp2.project( 1, rmax ) : return False
                if nmin == nmax == 0 :
                    if rmin == rmax == 1 :
                        if not self.exp1.project( lmin, 0 ) : return False
                    if lmin == lmax == 1 :
                        if not self.exp2.project( rmin, 0 ) : return False
            case '|' :
                if nmin == nmax == 1 :
                    if rmin == rmax == 0 :
                        if not self.exp1.project( 1, lmax ) : return False
                    if lmin == lmax == 0 :
                        if not self.exp2.project( 1, rmax ) : return False
                if nmin == nmax == 0 :
                    if not self.exp1.project( lmin, 0 ) : return False
                    if not self.exp2.project( rmin, 0 ) : return False

            case '+' :
                if not self.exp1.project( nmin-rmax , nmax-rmin ) : return False
                if not self.exp2.project( nmin-lmax , nmax-lmin ) : return False
            case '-' :
                if not self.exp1.project( nmin+rmin , nmax+rmax ) : return False
                if not self.exp2.project( lmin-nmax , lmax-nmin ) : return False
            case '*' :
                # if rmin == 0 : rmin = 1
                # if rmax == 0 : rmax = 1
                
                # [lmin,lmax] = [
                #     min(nmin//rmin, nmin//rmax, nmax//rmin, nmax//rmax),
                #     max(math.ceil(nmin/rmin), math.ceil(nmin/rmax), 
                #         math.ceil(nmax/rmin), math.ceil(nmax/rmax))
                # ]
                # if not self.exp1.project(lmin, lmax) : return False

                # if lmin == 0 : lmin = 1
                # if lmax == 0 : lmax = 1

                # [rmin,rmax] = [
                #     min(nmin//lmin, nmin//lmax, nmax//lmin, nmax//lmax),
                #     max(math.ceil(nmin/lmin), math.ceil(nmin/lmax), 
                #         math.ceil(nmax/lmin), math.ceil(nmax/lmax))
                # ]
                # if not self.exp2.project(rmin, rmax) : return False
                pass
        return True

    #--------------------------------------------------------------
    def match(self, localvars, globalvars) :
        exp1 = self.exp1.match(localvars, globalvars)
        exp2 = self.exp2.match(localvars, globalvars)

        return Expression(exp1, self.oper, exp2)

    #--------------------------------------------------------------
    def setEngine(self, engine) :
        self.exp1.setEngine(engine)
        self.exp2.setEngine(engine)

#====================================================================

def minimize(exp) -> list:
    return [MINIMIZE,exp]

#--------------------------------------------------------------

def maximize(exp) -> list:
    return [MAXIMIZE,exp]

#--------------------------------------------------------------

def unoptimize() -> list:
    return [NONEOPTI,None]

#====================================================================

def IntVarArray(n,min=-IntVar.INFINITE,max=IntVar.INFINITE,prefix='_') -> list:
    vs = []
    for i in range(n) :
        name = prefix+str(i) if prefix != '_' else '_'
        vs.append(IntVar(min,max,name))
    return vs

#--------------------------------------------------------------

def toStrs(vars, printview=IntVar.PRINT_VALUE) -> str:
    text = ''
    for v in vars : 
        text += v.toStr(printview) + ' '

    return '[' + text + ']'

#--------------------------------------------------------------

def toInts(vars, len=0) -> list:
    intArray = []
    for i,v in enumerate(vars) : 
        if len>0 and i == len : break
        intArray.append( v.getVal() )

    return intArray
