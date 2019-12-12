from Expression import Expression
import Unifcation
import re
class Premisses :
     def __init__(self,expressions,conditions):
        self.expressions = expressions
        self.conditions = conditions
class Regle:
    def __init__(self,expressions,conditions,conclusion):
        self.presmisses = Premisses(expressions,conditions)
        self.conclusion = conclusion
    def __str__(self):
        e=''
        for exp in self.presmisses.expressions:
            e = e + ' ' + exp.__str__() + ','
        return e + ' ' + self.presmisses.conditions.__str__() + ' => ' + self.conclusion.__str__()

class Fait:
    def __init__(self,exp):
        self.exp = exp
    def __str__(self):
        return self.exp.__str__()
    __repr__ = __str__

def parse_file(file_name,base_des_regles,base_des_faits):
    file = open(file_name, "r")
    input = file.read()
    input = input.split('\n')
    
    for line in input:
        if len(line):
            if not('si ' in line or 'Si ' in line)  :
                base_des_faits.append(Fait(Expression(line)))
            else :
                regle = line[3:]
                regle = regle.split(' alors ')
                conditions = []
                expressions= []
                tableau = regle[0].split(' et ')
                for premisse in tableau:
                    if bool(re.compile(r".*(=|<|>|<=|>=|!=|==).*").match(premisse)):
                        conditions.append(premisse)
                    else: 
                        expressions.append(Expression(premisse))  
                        regle1 = regle[1][:len(regle[1])-1]
                        regex = re.sub(r"(\w+)\(", r"['\1,",regle1)
                        regex = regex.replace(",","','")
                        regex=regex+']'
                        regex = regex.replace("]","']")
                        conclusion = Expression(eval(regex))
                    
                base_des_regles.append(Regle(expressions,conditions,conclusion))

    
        
def ChercherUnificationPourRegle(base_des_faits,regle,i ,Result,Unif):
    Test = False
    if i == len(regle.presmisses.expressions) :
        conditionsValid= True
        for c in regle.presmisses.conditions :
            if eval(c) == False :
                conditionsValid=False
                return False
                break;
        if conditionsValid == True :           
            Result.append(regle)
            Result.append(Unif)
            Result=[]
            Unif=[]
            return True
    for f in base_des_faits:
        Uni=Unifcation.unifier(f.exp,regle.presmisses.expressions[i])
        if(Uni!= None):
            Test = True 
            premisses=[]
            conds=[]
            for e in regle.presmisses.expressions :
                premisses.append(Expression(e.expression))
            for e in regle.presmisses.conditions :
                conds.append(e)
            regleCopie = Regle(premisses,conds,Expression(regle.conclusion.expression));
            for j in range(0, len(regleCopie.presmisses.expressions)):   
                regleCopie.presmisses.expressions[j].substitute(Uni)
            for k in range(0, len(regleCopie.presmisses.conditions)):   
                for sub in Uni:
                    regleCopie.presmisses.conditions[k]=regleCopie.presmisses.conditions[k].replace(sub[0], sub[1])
            for j in range(0, len(regleCopie.conclusion.expression)):   
                regleCopie.conclusion.substitute(Uni)
            test=ChercherUnificationPourRegle(base_des_faits,regleCopie,i+1,Result,Unif)
            if test == True:
               Uni = Uni[::-1]
               Unif.append(Uni)
      
    return Test
    
    
        
def genereOperateursApplicables(base_des_regles,base_des_faits):
   
    Resultat=[]
    Unif=[]
    LogFile=[]
    conclusions=[]
    i=0
    for regle in base_des_regles :
        ChercherUnificationPourRegle(base_des_faits,regle,0,Resultat,Unif)
        if Resultat != [] :
            LogFile.append(str("Instanciations possibles pour la Regle "+ str(i)))
            #print("Instanciations possibles pour la Regle",i)
            for j in range(0, len(Resultat)-1):
                LogFile.append(str(Resultat[j]))
                #print(Resultat[j])
                if j%2 == 0 :
                    conclusions.append(Resultat[j].conclusion)
            LogFile.append(str("Substitution \n"+str(Resultat[j+1])))
            #print("avec la substitution suivante \n",Resultat[j+1])
            
        Resultat=[]
        Unif=[]
        i=i+1
    return LogFile,conclusions

def getNewFactsForAppliedRules(base_des_regles,base_des_faits) :
    LogFile,conclusions=genereOperateursApplicables(base_des_regles,base_des_faits)
    for i in range(0,len(conclusions)):
        for j in range(0, len(conclusions[i].expression)):
            if "+" in str(conclusions[i].expression[j]) or "-" in str(conclusions[i].expression[j])  or "*" in str(conclusions[i].expression[j])  or "/" in str(conclusions[i].expression[j])   :
                conclusions[i].expression[j]=str(eval(conclusions[i].expression[j]))
        regex = re.sub(r"\s*(\d+)", r"\1",str(conclusions[i].expression))
        conclusions[i]=Expression(eval(regex))

    return conclusions

def depthSearch(depth,base_des_regles,base_des_faits,but):
    liste=[]
    if depth == 0 :
        return False
    print ("******************")
    print(base_des_faits[0])
    print ("******************")
    conclusions=getNewFactsForAppliedRules(base_des_regles,base_des_faits)
    for e in conclusions :
        print(e)
    for i in range(0,len(conclusions)):
        if Unifcation.unifier(conclusions[i],but) is not None :
            print("But Atteint",conclusions[i])
            return True
        liste=[Fait(conclusions[i])] 
        result = depthSearch(depth - 1 ,base_des_regles,liste,but)
        if result == True :
            return result
def iterativeLimitedDepthSearch(base_des_regles,base_des_faits,but,limit):
    print("Lancer recherche profondeur Limité")  
    while not(depthSearch(limit,base_des_regles,base_des_faits,but)):
        limit=limit+1
    print("resultat trouvé dans la profondeur" , limit)
    return limit
             


class Node():
    def __init__(self, parent, position:Expression):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        for i in range(0,len(self.position.expression)):
            if self.position.expression[i] != other.position.expression[i] :
                return False
        return True


def astar(base_des_regles, start, end , heristic):
    start_node = Node(None, start.exp)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = []

    open_list.append(start_node)

    while len(open_list) > 0:

        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        if Unifcation.unifier(current_node.position,end_node.position) != None:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] 

        children= []
        liste = [Fait(current_node.position)]
        childrens = getNewFactsForAppliedRules(base_des_regles,liste)
        for e in childrens :
            children.append(Node(current_node,e))
            
        for child in children:
            child.g = current_node.g + 1
            if heristic == 1 :
                child.h = abs(int(child.position.expression[1])-2)
            else :
                if int(child.position.expression[1]) == 2 :
                    child.h =0
                if int(child.position.expression[1]+ child.position.expression[2]) < 2 :
                    child.h =7
                if int(child.position.expression[2]) > 2 : 
                    child.h =3
                else :
                    child.h =1

            child.f = child.g + child.h
            current_index=0;
            for  item in closed_list:
                if child == item  and child.f < item.f:
                    closed_list.pop(current_index)
                    open_list.append(child)
                    break;
                current_index=current_index+1
            
            current_index=0;
            for item in open_list:
                if child == item  and child.f < item.f:
                    open_list.pop(current_index)
                    break;
                current_index=current_index+1
         
            open_list.append(child)



                        
from tkinter import * 
from tkinter import filedialog
import os

class FileImport:
    def __init__(self,parent,title):
        self.parent = parent
        self.title= title
        self.filePath = StringVar() 
        self.filePathInput = Entry(self.parent, textvariable=self.filePath, width=30, state="readonly")
        self.filePathInput.pack()
        self.browseBtn = Button(self.parent, text="open", command=self.browseFile)
        self.browseBtn.pack()
        self.path = ""

    def getParent(self):
        return self.parent

    def getFilePathString(self):
        return self.filePath.get()
    
    def browseFile(self):
        my_filetypes = [('all files', '.*'), ('text files', '.txt')]
        self.filePath.set(
            filedialog.askopenfilenames(parent=self.parent,
                                            initialdir=os.getcwd(),
                                            title=self.title,
                                            filetypes=my_filetypes)
                                            )
        self.path=self.getFilePathString().split('(')[1].split(',')[0];
        
       

class Frame:
    def __init__(self,parent,title,rowV,columnV):
        self.parent = parent
        self.title = title
        self.frame = LabelFrame(self.parent, text=self.title, padx=10, pady=10)
        self.frame.grid(row = rowV, column = columnV, pady = 2,columnspan = 2) 
    
    def getElement(self):
        return self.frame

class Input:
    def __init__(self,parent,initValue,state):
        self.state = state
        self.parent = parent
        self.content = StringVar()
        self.content.set(initValue)
        self.input = Entry(self.parent, textvariable=self.content, width=30, state=self.state)
        self.input.pack()
    
    def setState(self,state):
        self.input.config(state = state)
        return
    def getElement(self):
        return self.input

class RadioList:
    def __init__(self,parent,initValue,modes,inputElement1,inputElement2,inputElement3):
        self.MODES = modes
        self.parent = parent
        self.choice = StringVar()
        self.choice.set(initValue)
        self.inputElement1 = inputElement1
        self.inputElement2 = inputElement2
        self.inputElement3 = inputElement3

        self.randerRadioMenu()

    def showChoice(self):
        choice = int(self.choice.get())
        if(choice==1):
            self.inputElement1.getElement().config(state=NORMAL)
            self.inputElement2.getElement().config(state=NORMAL)
            self.inputElement3.getElement().config(state=DISABLED)
        else:
            self.inputElement1.getElement().config(state=DISABLED)
            self.inputElement2.getElement().config(state=DISABLED)
            self.inputElement3.getElement().config(state=NORMAL)



    def randerRadioMenu(self):
        for text, mode in self.MODES:
            r = Radiobutton(self.parent, text=text,
                            variable=self.choice, value=mode, command=self.showChoice)
            r.pack(anchor=W)

window = Tk()
fileImport1 = FileImport(Frame(window,"Bases des connaissance",0,0).getElement(),"Select file")
Expression1 = Input(Frame(window,"Expression 1",1,0).getElement(),'',DISABLED) 
Expression2 = Input(Frame(window,"Expression 2",2,0).getElement(),'',DISABLED)
BUT= Input(Frame(window,"BUT",4,0).getElement(),'',DISABLED)


radioList = RadioList(
    Frame(window,"Mode",3,0).getElement(),
    "2",
    [
        ("Unifier 2 Expression", "1"),
        ("Chercher Les Jeux d 'instantiations possibles ", "2"),
        ("Appliquer Algorithme de Profondeur Limité", "3"),
        ("Appliquer Algorithme A* avec la premiere heuristique", "4"),
        ("Appliquer Algorithme A* avec la deuxième heuristique", "5"),
    ],
     Expression1,
     Expression2,
     BUT
     
     
)


tlog = Text(window,wrap = "word")
tlog.grid(row = 0, column = 2, columnspan = 3, rowspan = 4, padx = 5, pady = 5)
               

    
    
def Execution():
    if int(radioList.choice.get()) == 1 :
        resultat = Unifcation.unifier(Expression(Expression1.content.get()),Expression(Expression2.content.get()));
        if resultat == None :
            tlog.insert(END,"Pas d'unifciation Possible"+"\n")
        else :
            tlog.insert(END,"La substitution géneralle pour ces deux expressions est :"+"\n")
            tlog.insert(END,str(resultat)+"\n")

    if int(radioList.choice.get()) == 2 :
        FileHandler = fileImport1.path.replace("'",'')
        base_des_regles = []
        base_des_faits = []
        parse_file(FileHandler,base_des_regles,base_des_faits)
        LogFile,conclusions=genereOperateursApplicables(base_des_regles,base_des_faits)
        for e in LogFile :
            tlog.insert(END,e+"\n")
    if int(radioList.choice.get()) == 3 :
         FileHandler = fileImport1.path.replace("'",'')
         base_des_regles = []
         base_des_faits = []
         parse_file(FileHandler,base_des_regles,base_des_faits)
         limit=iterativeLimitedDepthSearch(base_des_regles,base_des_faits,Expression(BUT.content.get()),0)
         tlog.insert(END,"Le but se trouve a la profondeur :"+str(limit)+"\n")
    if int(radioList.choice.get()) == 4 :
           FileHandler = fileImport1.path.replace("'",'')
           base_des_regles = []
           base_des_faits = []
           parse_file(FileHandler,base_des_regles,base_des_faits)
           path = astar(base_des_regles,base_des_faits[0], Expression(BUT.content.get()),1)
           tlog.insert(END,"Solution Path according to the first heuristic is :"+"\n")
           print("Solution Path according to the first heuristic is :"+"\n")
           for e in path :
               print(e)
               tlog.insert(END,str(e)+"\n")
    if int(radioList.choice.get()) == 5 :
           FileHandler = fileImport1.path.replace("'",'')
           base_des_regles = []
           base_des_faits = []
           parse_file(FileHandler,base_des_regles,base_des_faits)
           path = astar(base_des_regles,base_des_faits[0], Expression(BUT.content.get()),2)
           tlog.insert(END,"Solution Path according to the first heuristic is :"+"\n")
           print("Solution Path according to the second heuristic is :"+"\n")           
           for e in path :
               print(e)
               tlog.insert(END,str(e)+"\n")



    
   
def RuleFunc():
   FileHandler = fileImport1.path.replace("'",'')
   base_des_regles = []
   base_des_faits = []
   parse_file(FileHandler,base_des_regles,base_des_faits)
   for e in base_des_regles :
       tlog.insert(END,str(e)+"\n")

def FactFunc():
   FileHandler = fileImport1.path.replace("'",'')
   base_des_regles = []
   base_des_faits = []
   parse_file(FileHandler,base_des_regles,base_des_faits)
   for e in base_des_faits :
       tlog.insert(END,str(e)+"\n")   

def ClearTolg():
    tlog.delete('1.0', END)
    

save = Button(window, text="Delete", command=ClearTolg)
save.grid(row = 5, column = 0, pady = 2) 
save = Button(window, text="Execute", command=Execution)
save.grid(row = 5, column = 2, pady = 2) 
save = Button(window, text="Facts", command=FactFunc)
save.grid(row = 5, column = 3, pady = 1) 
save = Button(window, text="Rules", command=RuleFunc)
save.grid(row = 5, column = 4, pady = 1) 


7
window.mainloop()                    
                
def main():
     base_des_regles = []
     base_des_faits = []
    
     print("Veuillez Saisir Le nom du fichier:")
     File= input()
     if File != "" :
         print("Veuillez choisir un Mode:")
         print("1-Chercher Les Jeux d 'instantiations possibles")
         print("2- Appliquer Algorithme de Profondeur Limité" )
         print("3- Appliquer Algorithme A* avec la premiere heuristique" )
         print("4- Appliquer Algorithme A* avec la deuxième heuristique ")
         print("5-Appliquer Algorithme de Profondeur Limité paramétré" )
    
         mode= input()
         if int(mode) == 1:
             parse_file(File,base_des_regles,base_des_faits)
             LogFile,conclusions=genereOperateursApplicables(base_des_regles,base_des_faits)
             for e in LogFile :
                 print(e)     
         if int(mode) == 2:
             print("Veuillez Saisir Un But:")
             but= input()
             base_des_regles = []
             base_des_faits = []
             parse_file(File,base_des_regles,base_des_faits)
             limit=iterativeLimitedDepthSearch(base_des_regles,base_des_faits,Expression(but),0)   
         if int(mode) == 3:
             print("Veuillez Saisir Un But:")
             but= input()
             base_des_regles = []
             base_des_faits = []
             parse_file(File,base_des_regles,base_des_faits)
             path = astar(base_des_regles,base_des_faits[0], Expression(but),1)
             print("Solution Path according to the first heuristic is :"+"\n")
             for e in path :
                 print(e) 
         if int(mode) == 4:
             print("Veuillez Saisir Un But:")
             but= input()
             base_des_regles = []
             base_des_faits = []
             parse_file(File,base_des_regles,base_des_faits)
             path = astar(base_des_regles,base_des_faits[0], Expression(but),2)
             print("Solution Path according to the first heuristic is :"+"\n")
             for e in path :
                 print(e)   
         if int(mode) == 5:
             print("Veuillez Saisir Un But:")
             but= input()
             print("Veuillez Specifier une profondeur:")
             limit= input()
             base_des_regles = []
             base_des_faits = []
             parse_file(File,base_des_regles,base_des_faits)
             boolean=depthSearch(int(limit),base_des_regles,base_des_faits,Expression(but))  
             if boolean :
                 print("resultat trouvé dans la profondeur" , limit)
             else:
                 print("resultat non trouvé dans la profondeur" , limit)
                 


        

if __name__ == "__main__":
    main()
