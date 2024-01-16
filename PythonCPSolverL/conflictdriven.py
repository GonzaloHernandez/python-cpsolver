#====================================================================
# Simple Constraint (Satisfaction/Optimization) Programming Solver 
# Current version 1.3
#
# Gonzalo Hernandez
# gonzalohernandez@hotmail.com
# 2024
#
# Modules:
#   PythonCPSolver
#       engine.py
#       propagators.py
#       variables.py
#       brancer.py
#       conflictdriven.py
#====================================================================

from PythonCPSolverL.propagators import *

#====================================================================

class ConflictDriven :
    def __init__(self,vars, engine) -> None:
        self.vars   = vars  # Real variables
        self.bvars  = []    # Boolean variables linking each value
        self.claus  = []    # New constraints ( Clauses ) 
        self.delta  = []    # Matching to min value of real variable

        for v in self.vars :
            bvar = IntVarArray( v.card(), 0,1, '#'+v.name )
            lits = []
            for i,vi in enumerate(bvar) :
                engine.cons.append( Equation(vi == (v == i+v.min)) )
                vi.setEngine( engine )
                lits.append( Literal(vi) )

            self.bvars.append( bvar )
            self.delta.append( v.min )
            self.claus.append( Clause(lits) )
        pass

    def __str__(self) -> str:
        return "Confict driven"

    def prune(self) :
        for c in self.claus :
            if c.prune() is False : self.learn()

        return True

    def learn(self) :
        pass

    def createClause(self, vars, alts) :
        lits = []
        for i,v in enumerate(vars) :
            var = self.bvars[i][v.getVal() - self.delta[i]]
            lits.append( Literal(var, alts[i] ) )

        self.claus.append( Clause(lits) )

#====================================================================
