
graphe={'S': ['A=4', 'B=10'], 'A': ['B=3'], 'B': ['D=6', 'C=10'], 'D': ['D=10'], 'C': ['G1=6', 'G2=5']}


def coutUniforme(graphe={},EI="",EF="",path=[],chemin=[]):
    f=open("./Logfile/coutuniformealgo.txt","w")
    path.append(EI)
    tmplist=[]
    etatinitial=EI
    cu=0
    visited=[]
    while EI!=EF:
        if graphe.keys().__contains__(EI):
            for j in list(graphe.get(EI)):
                tmplist.append([int(j.split('=')[1])+cu,j.split('=')[0]])
        visited.append(EI)
        if tmplist!=[]:
            while tmplist!=[]:
                if sorted(tmplist)[0][1] not in visited:
                    EI = sorted(tmplist)[0][1]
                    path.append(EI)
                    cu = int(sorted(tmplist)[0][0])
                    deletecout(tmplist)
                    break
                else:
                    deletecout(tmplist)
            if tmplist==[]:
                return cu
        else:
            return cu
        if len(tmplist)>10:
            return 0

    chemin.append(EF)
    while EF!=etatinitial:
        l = []
        for i in list(graphe.values()):
            l.insert(0,i)
        for i in l:
            for j in i:
                if j.split('=')[0]==EF:
                    for s in path:
                        if graphe.keys().__contains__(s):
                            if graphe[s]==i:
                                EF=s
                                chemin.insert(0,s)
                                break
    f.write("path: "+str(path)+"\n")
    f.write("chemin: " + str(chemin) + "\n")
    f.write("cout: " + str(cu) + "\n")
    print(path,chemin)
    return cu



def deletecout(tmplist):
    i=0
    while len(tmplist) > i:
        if tmplist[i] == sorted(tmplist)[0]:
            tmplist.pop(i)
            return True
        i = i + 1


def largeurdabord(graphe={},etatInitial="",etatFinal="",path=[],chemin=[]):
    f=open("./Logfile/largeurLog.txt","w")
    path.append(etatInitial)
    item=[]
    EI=etatInitial
    couuut=0
    visited=[etatInitial]
    if etatInitial!=etatFinal:
        for s in graphe.__getitem__(etatInitial):
            item.append(s.split('=')[0])
        for i in item:
            if i not in visited:
                if graphe.keys().__contains__(i):
                    for j in graphe.__getitem__(i):
                        item.append(j.split('=')[0])
            path.append(i)
            visited.append(i)
            print(path)
            if i==etatFinal:
                it=etatFinal
                while it!=EI:
                    for mm in graphe.values():
                        m=[]
                        for k in mm:
                            m.append(k.split('=')[0])
                        if it in m:
                            for i in path:
                                if graphe.keys().__contains__(i) and graphe.__getitem__(i)==mm:
                                    chemin.insert(0,i)
                                    it=i
                                    break
                chemin.append(etatFinal)
                print(path)
                print(chemin)
                f.write("parcours: "+str(path)+"\n")
                f.write("chemin: " + str(chemin)+"\n")

                for i in range(1, len(chemin)):
                    st = graphe.get(chemin[i - 1])
                    for j in st:
                        if j.split('=')[0] == chemin[i]:
                            couuut = couuut + int(j.split('=')[1])
                f.write("cout: "+str(couuut)+"\n")
                return couuut
    return couuut


def profondeurrecherche(graphe={},EI="",EF="",path=[],chemin=[],file=""):
    f=""
    if file=="":
        f=open("./Logfile/profondeurLog.txt","w")
    path.append(EI)
    etatinitial=EI
    etatfin=EF
    cc=0
    if EI==EF:
        return True
    else:
        item=[]
        visited=[]
        if graphe.keys().__contains__(EI):
            for i in graphe.get(EI):
                item.append(i.split("=")[0])
            while EI!=EF and len(item)>0:
                EI=item[0]
                visited.append(item[0])
                path.append(EI)
                item.pop(0)
                if graphe.keys().__contains__(EI):
                    for j in range(0,len(graphe.get(EI))):
                        if graphe.get(EI)[j].split("=")[0] not in visited:
                            item.insert(j,graphe.get(EI)[j].split("=")[0])
            if EI == EF:
                chemin.append(EF)
                while EF != etatinitial:
                    l = []
                    for i in list(graphe.values()):
                        l.insert(0, i)
                        #print(l)
                    for i in l:
                        for j in i:
                            if j.split('=')[0] == EF:
                                for s in path:
                                    if graphe.keys().__contains__(s):
                                        if graphe[s] == i:
                                            if s!=etatfin:
                                                EF = s
                                                chemin.insert(0, s)
                                                print(s)
                                                break
                for i in range(1, len(chemin)):
                    st = graphe.get(chemin[i - 1])
                    for j in st:
                        if j.split('=')[0] == chemin[i]:
                            cc = cc + int(j.split('=')[1])
            else:
                for i in path:
                    chemin.append(i)
        else:
            chemin.append(etatinitial)
            cout=0

        if file=="":
            f.write("path: " + str(path) + "\n")
            f.write("chemin: " + str(chemin) + "\n")
            f.write("cout: " + str(cc) + "\n")
        return cc



def profondeuriteratif(graphe={},etatInitial="", etatFinal="",path=[],chemin=[]):
    graphe1=list(graphe.keys())
    niveau = 1
    cout=0
    f=open("./Logfile/profondeurIteratifLog.txt","w")
    f.write("niveau 0: \n path: "+etatInitial+"\n chemin: "+etatInitial+"\n")
    grav={}
    for i in graphe1:
        grav.update({i:graphe.get(i)})
    for i in graphe1:
        if i==etatInitial:
            break
        else:
            grav.pop(i)
    cheminLocal = []
    if etatInitial!=etatFinal:
        while not path.__contains__(etatFinal):
            g = {}
            cheminLocal=[]
            pathLocal=[]
            if len(grav.keys())>0:
                for i in range(0,niveau):
                    if len(grav.keys()) >i:
                        g.update({list(grav.keys())[i]:graphe.get(list(grav.keys())[i])})
                    else:
                        return cout
                if len(g.keys())>0:
                    cout=profondeurrecherche(g,etatInitial,etatFinal,pathLocal,cheminLocal,"./Logfile/profondeurIteratifLog.txt")
                    f.write("niveau " + str(niveau)+" : \n path: "+str(pathLocal)+"\n chemin: "+str(cheminLocal)+"\n cout: "+str(cout)+"\n")
                    for p in pathLocal:
                        path.append(p)
                    niveau=niveau+1
                else:
                    return cout
            else:
                return cout
        for i in cheminLocal:
            chemin.append(i)
        print(chemin)
        print(path)
    else:
        path.append(etatFinal)
        chemin.append(etatInitial)
    return cout



path=[]
chemin=[]
#print(largeurdabord(graphe,'B','A'))
print(profondeuriteratif(graphe,'S','G2',[],[]))

#print(profondeurrecherche(graphe,'G1','S',[],[]))

#print(coutUniforme(graphe,'S','G2',path,chemin))

