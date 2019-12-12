from Expression import Expression


def unifier_atom(expr1:Expression,expr2:Expression):
    if(expr2.isAtom()):
        expr1,expr2=expr2,expr1

    if(expr1==expr2):
        return []

    if(expr2.isVariable()):
        expr1,expr2 = expr2,expr1

    if(expr1.isVariable()):
        if(expr1 in expr2):
            return None
        if (expr2.isAtom()):
           return [[expr1.expression[0],expr2.expression[0]]]
        else:
            return [[expr1.expression[0],expr2.expression.__str__()]]

    return None

def unifier(terms1:Expression,terms2:Expression):
    if(terms1.isAtom() or terms2.isAtom()):
        return unifier_atom(terms1,terms2)
    F1,T1=terms1.separate()
    F2,T2=terms2.separate()

    Z1=unifier(F1,F2)
    if(Z1==None):
        return None

    T1.substitute(Z1)
    T2.substitute(Z1)


    Z2=unifier(T1,T2)

    if(Z2==None):
        return None
    Z2+=Z1
    return Z2


