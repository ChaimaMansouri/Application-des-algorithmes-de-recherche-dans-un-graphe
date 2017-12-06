import time
graphe={'S=21': [['A=18',4], ['B=15',10]], 'A=18': [['B=15',3]],'B=15': [['D=4',6],['C=5',10]],'D=4':[['D=4',10]],'C=5':[['G1=0',6],['G2=0',5]]}

graphe1={'S=21':['A=18','B=15'],'A=18':['B=15'],'B=15':['D=4','C=5'],'D=4':['D=4'],'C=5':['G1=0','G2=0']}


def gloutn(graphe={},EI="",EF="",path=[],chemin=[]):
    start_time = time.time()
    cout=0
    f=open("./Logfile/GloutonLog.txt","w")
    etatInitial = finditem(graphe, EI)
    visited=[EI]
    path.append(EI)
    chemin.append(EI)
    if etatInitial!=None:
        cout=int(etatInitial.split('=')[1])
    else:
        return 0
    etatdebut=etatInitial
    tab = []
    while EI!=EF:
        if etatInitial in graphe.keys():
            for i in graphe[etatInitial]:
                if i.split('=')[0] not in visited:
                    tab.append(i)
        etatInitial=getMin(tab)
        if tab!=[]:
            if etatInitial.split('=')[0] not in visited:
                EI=etatInitial.split('=')[0]
                cout=cout+int(etatInitial.split('=')[1])
                visited.append(EI)
                chemin.append(EI)
            else:
                tab=returntableau(tab,etatInitial)
                if len(tab)>0:
                    etatInitial=getMin(tab)
                    EI = etatInitial.split('=')[0]
                    cout = cout + int(etatInitial.split('=')[1])
                else:
                    EI = path[len(path)-2]
                    etatInitial= finditem(graphe, EI)
        else:
            return cout
        path.append(EI)
    chemin.append(EF)
    print(path)
    print(chemin)
    f.write("\n path: ")
    for i in path:
        f.write(i + " , ")
    f.write(" \n chemin: ")
    for i in chemin:
        f.write(i + " , ")
    f.write("\n cout: "+ str(cout))
    f.write("\n temps exec :"+str(time.time()-start_time))
    return cout

def getMin(tab=[]):
    l=[]
    for i in tab:
        l.append(int(i.split("=")[1]))
    for i in tab:
        if sorted(l)[0]==int(i.split("=")[1]):
            return i

def returntableau(tab,etatInitial):
    for i in range(0, len(tab)):
        if tab[i] == etatInitial:
            tab.pop(i)
            return tab


def finditem(graphe,EI):
    for i in graphe.keys():
        if i.split('=')[0]==EI:
            return i
    for i in graphe.values():
        for j in i:
            if j[0].split('=')[0]==EI:
                return j[0]


def algoa(graphe={},EI="",EF="",path=[],chemin=[]):
    start_time = time.time()
    f = open("./Logfile/ALog.txt", "w")
    cout=0
    dicopen={}
    dicclose={}
    etatInitial=finditem(graphe,EI)
    dicopen[EI]=[int(etatInitial.split('=')[1]),0]
    f.write("noeuds     ouvert       ferme \n")
    while dicopen!={}:
        f.write(EI+"     "+ str(dicopen)+"     "+str(dicclose)+"\n")
        dicclose[EI] = dicopen[EI]
        if EI==EF:
            path.append(EF)
            cout = sum(dicopen[EF])
            f.write("path:  " + str(path) + "\n")
            f.write("chemin:  " + str(path) + "\n")
            f.write("cout: " + str(cout) + "\n")
            f.write("temps exec :"+ str(time.time()-start_time))
            for i in path:
                chemin.append(i)
            return cout
        if etatInitial in graphe.keys():
            for i in graphe[etatInitial]:
                if i[0].split('=')[0] not in list(dicopen.keys()) or i[0].split('=')[0] not in list(dicclose.keys()):
                    dicopen[i[0].split('=')[0]]=[int(i[0].split('=')[1]),i[1]+dicopen[EI][1]]
                elif i[0].split('=')[0] in list(dicopen.keys()) or i[0].split('=')[0] in list(dicclose.keys()):
                    g=0
                    if i[0].split('=')[0] in dicopen.keys():
                        g=sum(dicopen[i[0].split('=')[0]])
                    else:
                        g = sum(dicclose[i[0].split('=')[0]])
                    if list(dicopen[EI])[1]+i[1]+int(i[0].split('=')[1]) <g:
                        dicopen[i[0].split('=')[0]]=i[1]+int(i[0].split('=')[1])
        path.append(EI)
        del dicopen[EI]
        sorted(list(dicopen.values()))
        if len(list(dicopen.keys()))>0:
            EI=list(dicopen.keys())[0]
            etatInitial = finditem(graphe, EI)
        else:
            return cout

path=[]
chemin=[]
#print(algoa(graphe,'S','G2',path,chemin))
print(gloutn(graphe1,'G1','G2',path,chemin))