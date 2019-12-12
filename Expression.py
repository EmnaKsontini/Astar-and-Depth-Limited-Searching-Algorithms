import re

class Expression:
    def __init__(self,chain):
        #si il s sagit d une liste lors de la separation pas besoin de cree une nouvelle expression
        if(isinstance(chain,list)):
            self.expression=chain
            return
        regex = re.sub(r"(\w+)\(", r"[\1,",chain)
        regex = regex.replace(')',']');
        regex = re.sub(r"(\w+)", r"'\1'", regex)
        regex = regex.replace("?'","'?")
        self.expression = eval(regex)
    
    def __str__(self):
        return self.expression.__str__()

    def isAtom(self):
        return (len(self.expression)<=1)

    def isVariable(self):
        return len(self.expression)==1 and '?' in self.expression[0]

    def separate(self):
        if(isinstance(self.expression[0],list)):
            first = self.expression[0]
        else:
            first = [self.expression[0]]
        queue=self.expression[1:]
        #pour ne pas considerer une liste de liste comme un atome
        if(len(queue)==1 and isinstance(queue[0],list)):
            queue=queue[0]
        return Expression(first),Expression(queue)

    def __contains__(self, expr):
        tmp = self.expression.__str__()
        return (expr.expression[0] in tmp)

    def __eq__(self, expr):
        return  len(self.expression) == 1 and len(expr.expression)==1 and self.expression[0]==expr.expression[0]


    def substitute(self,subs:list):
        tmp = self.expression.__str__()
        for sub in subs:    
            tmp=tmp.replace(sub[0], sub[1])
        self.expression = eval(tmp)
        
