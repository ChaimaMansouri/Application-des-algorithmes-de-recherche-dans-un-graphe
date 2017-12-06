from kivy.app import App
import graphviz
from kivy.uix.button import Button
from kivy.factory import Factory
from kivy.uix.filechooser import FileChooserListView, FileChooser, FileChooserIconView
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from os.path import sep, expanduser, isdir, dirname
import shutil
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.utils import platform
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
import noninforme
import informe
from lxml import etree
import string
import random





class Graph:
    def __init__(self,noeuds=[],heuristique=[],arcs=[],coutArc=[]):
        self.noeuds=noeuds
        self.heuristique=heuristique
        self.arcs=arcs
        self.coutArc=coutArc


class CustomDropDown(DropDown):
    pass


class BtnBrowser(GridLayout):
    pass


class GridLayoutBuild(GridLayout):
    def onButtonPress(self, button):
        return BtnBrowser()

    def oncustomdropdown(self,button):
        drop=CustomDropDown()
        drop.bind(on_select=lambda instance, x: setattr(button, 'text', x))
        return drop.open(button)


class GraphApplicationApp(App):
    file=""
    l=Label(text="")
    image=Image(source="")
    G = graphviz.Digraph(format="png")
    g=Graph()
    list = []
    listchemin=[]
    def build(self):
        return GridLayoutBuild()

    def loader(self,selection):
        s=str(selection[0])
        #because i am on windows
        s=s.replace('\\','/')
        self.file = s
        self.G=None
        self.afficherGraph()

    def afficherGraph(self):
        noeuds=[]
        arcs=[]
        if len(self.g.noeuds)>0:
            print("dd")
            self.g.noeuds.clear()
            self.g.arcs.clear()
            self.g.coutArc.clear()
            self.g.heuristique.clear()
            print(self.g.noeuds)
        if self.file.endswith('.txt'):
            with open(self.file, "r") as out:
                graphe = out.read().split('\n')
            i = graphe.index("noeuds:")
            j = graphe.index("arcs:")
            noeuds = graphe[0:i] + graphe[i + 1:j]
            arcs = graphe[j + 1:]

        elif self.file.endswith('.xml'):
            tree = etree.parse(self.file)
            for n in tree.xpath("/graphe/noeud"):
                noeuds.append(n.text)
            for a in tree.xpath("/graphe/arc"):
                arcs.append(a.text)
        for n in noeuds:
            self.g.noeuds.append(n.split('=')[0])
            self.g.heuristique.append(n.split('=')[1])
        for a in arcs:
            self.g.arcs.append(a.split('=')[0])
            self.g.coutArc.append(a.split('=')[1])
        print(self.g.noeuds,self.g.arcs)
        print(self.file)

        self.G=graphviz.Digraph(format="png",filename="./animation/GrapheImage")
        self.G.attr('node', shape='ellipse')
        for n in range(0,len(self.g.noeuds)):
            self.G.node(name=self.g.noeuds[n],xlabel="<<font color='blue'>"+self.g.heuristique[n]+"</font>>",color="blue")
        for a in range(0,len(self.g.arcs)):
            self.G.edge(self.g.arcs[a].split('=')[0].split(',')[0], self.g.arcs[a].split('=')[0].split(',')[1],label=self.g.coutArc[a])
        self.G.render()
        self.image.source="./animation/GrapheImage.png"
        self.image.reload()


    def getData(self,algo,EI,EF):
        self.image.source = "./animation/GrapheImage.png"
        self.image.reload()
        if algo.text!="Choisir .." and EI.text!="" and EF.text!="" and self.file!="" and EF.text in self.g.noeuds and EI.text in self.g.noeuds:
            if algo.text=="Largeur":
                localPath=[]
                localchemin=[]
                gr={}
                couuut=0
                for i in range(0,len(self.g.arcs)):
                    if gr.keys().__contains__(self.g.arcs[i].split(',')[0]):
                        gr.get(self.g.arcs[i].split(',')[0])
                        gr.get(self.g.arcs[i].split(',')[0]).append(self.g.arcs[i].split(',')[1]+"="+str(self.g.coutArc[i]))
                    else:
                        gr.update({self.g.arcs[i].split(',')[0]: [self.g.arcs[i].split(',')[1]+"="+str(self.g.coutArc[i])]})
                print(gr)
                couuut=noninforme.largeurdabord(gr,EI.text,EF.text,localPath,localchemin)
                print(localPath)
                print(localchemin)
                if EF.text in localPath:
                    self.list=self.getListImage(localPath)
                    print(self.list)
                    self.listchemin=self.getListImage(localchemin)
                    self.l.text = "[b][color=c1b5cc]But atteint \n Cout = " + str(couuut)+"[/color][/b]"
                    self.l.texture_update()
                else:
                    self.list=[]
                    self.listchemin=[]
                    self.l.text = "[b][color=c1b5cc] But Non atteint \n Pas de chemin [/color][/b]"
                    self.l.texture_update()
                print(couuut)
                print(gr)
            elif algo.text=="Profondeur":
                localPath = []
                localchemin = []
                gr = {}
                couuut = 0
                for i in range(0, len(self.g.arcs)):
                    if gr.keys().__contains__(self.g.arcs[i].split(',')[0]):
                        gr.get(self.g.arcs[i].split(',')[0])
                        gr.get(self.g.arcs[i].split(',')[0]).append(
                            self.g.arcs[i].split(',')[1] + "=" + str(self.g.coutArc[i]))
                    else:
                        gr.update({self.g.arcs[i].split(',')[0]: [
                            self.g.arcs[i].split(',')[1] + "=" + str(self.g.coutArc[i])]})
                print(gr)
                couuut = noninforme.profondeurrecherche(gr, EI.text, EF.text, localPath, localchemin)
                print(localPath)
                print(localchemin)
                if EF.text in localPath:
                    self.list=self.getListImage(localPath)
                    print(self.list)
                    self.listchemin=self.getListImage(localchemin)
                    self.l.text = "[b][color=c1b5cc]But atteint \n Cout = " + str(couuut)+"[/color][/b]"
                    self.l.texture_update()
                else:
                    self.list=[]
                    self.listchemin=[]
                    self.l.text = "[b][color=c1b5cc] But Non atteint \n Pas de chemin [/color][/b]"
                    self.l.texture_update()
                print(couuut)
                print(gr)
            elif algo.text=="Cout uniforme":
                localPath = []
                localchemin = []
                gr = {}
                couuut = 0
                for i in range(0, len(self.g.arcs)):
                    if gr.keys().__contains__(self.g.arcs[i].split(',')[0]):
                        gr.get(self.g.arcs[i].split(',')[0])
                        gr.get(self.g.arcs[i].split(',')[0]).append(
                            self.g.arcs[i].split(',')[1] + "=" + str(self.g.coutArc[i]))
                    else:
                        gr.update({self.g.arcs[i].split(',')[0]: [
                            self.g.arcs[i].split(',')[1] + "=" + str(self.g.coutArc[i])]})
                print(gr)
                couuut = noninforme.coutUniforme(gr, EI.text, EF.text, localPath, localchemin)
                print(localPath)
                print(localchemin)
                if EF.text in localPath:
                    self.list=self.getListImage(localPath)
                    print(self.list)
                    self.listchemin=self.getListImage(localchemin)
                    self.l.text = "[b][color=c1b5cc]But atteint \n Cout = " + str(couuut)+"[/color][/b]"
                    self.l.texture_update()
                else:
                    self.list=[]
                    self.listchemin=[]
                    self.l.text = "[b][color=c1b5cc] But Non atteint \n Pas de chemin [/color][/b]"
                    self.l.texture_update()
                print(couuut)
                print(gr)
            elif algo.text=="IDS":
                localPath = []
                localchemin = []
                gr = {}
                couuut = 0
                for i in range(0, len(self.g.arcs)):
                    if gr.keys().__contains__(self.g.arcs[i].split(',')[0]):
                        gr.get(self.g.arcs[i].split(',')[0])
                        gr.get(self.g.arcs[i].split(',')[0]).append(
                            self.g.arcs[i].split(',')[1] + "=" + str(self.g.coutArc[i]))
                    else:
                        gr.update({self.g.arcs[i].split(',')[0]: [
                            self.g.arcs[i].split(',')[1] + "=" + str(self.g.coutArc[i])]})
                print(gr)
                couuut = noninforme.profondeuriteratif(gr, EI.text, EF.text, localPath, localchemin)
                print(localPath)
                print(localchemin)
                if EF.text in localPath:
                    self.list=self.getListImage(localPath)
                    print(self.list)
                    self.listchemin=self.getListImage(localchemin)
                    self.l.text = "[b][color=c1b5cc]But atteint \n Cout = " + str(couuut)+"[/color][/b]"
                    self.l.texture_update()
                else:
                    self.list=[]
                    self.listchemin=[]
                    self.l.text = "[b][color=c1b5cc] But Non atteint \n Pas de chemin [/color][/b]"
                    self.l.texture_update()
                print(couuut)
                print(gr)
            elif algo.text=="A*":
                localPath = []
                localchemin = []
                gr = {}
                ch=""
                couuut=0
                for i in range(0,len(self.g.noeuds)):
                    for j in range(0,len(self.g.arcs)):
                        ch=self.g.noeuds[i]+"="+str(self.g.heuristique[i])
                        if self.g.arcs[j].split(',')[0]==self.g.noeuds[i]:
                            s=""
                            for p in range(0,len(self.g.noeuds)):
                                if self.g.noeuds[p]==self.g.arcs[j].split(',')[1]:
                                    s=self.g.noeuds[p]+"="+str(self.g.heuristique[p])
                                    print(ch)
                                    print(s)
                            if ch in gr.keys():
                                gr[ch].append([s,int(self.g.coutArc[j])])
                            else:
                                gr[ch]=[[s,int(self.g.coutArc[j])]]
                print(gr)
                couuut=informe.algoa(gr, EI.text, EF.text, localPath, localchemin)
                print(localPath)
                if EF.text in localPath:
                    self.list=self.getListImage(localPath)
                    print(self.list)
                    self.listchemin=self.getListImage(localchemin)
                    self.l.text = "[b][color=c1b5cc]But atteint \n Cout = " + str(couuut)+"[/color][/b]"
                    self.l.texture_update()
                else:
                    self.list=[]
                    self.listchemin=[]
                    self.l.text = "[b][color=c1b5cc] But Non atteint \n Pas de chemin [/color][/b]"
                    self.l.texture_update()
                print(couuut)

            elif algo.text=="BFS":
                localPath = []
                localchemin = []
                gr = {}
                ch=""
                couuut=0
                for i in range(0,len(self.g.noeuds)):
                    for j in range(0,len(self.g.arcs)):
                        ch=self.g.noeuds[i]+"="+str(self.g.heuristique[i])
                        if self.g.arcs[j].split(',')[0]==self.g.noeuds[i]:
                            s=""
                            for p in range(0,len(self.g.noeuds)):
                                if self.g.noeuds[p]==self.g.arcs[j].split(',')[1]:
                                    s=self.g.noeuds[p]+"="+str(self.g.heuristique[p])
                            if ch in gr.keys():
                                gr[ch].append(s)
                            else:
                                gr[ch] = [s]
                print(gr)
                couuut=informe.gloutn(gr,EI.text, EF.text, localPath,localchemin)
                if EF.text in localPath:
                    self.list=self.getListImage(localPath)
                    print(self.list)
                    self.listchemin=self.getListImage(localchemin)
                    self.l.text = "[b][color=c1b5cc]But atteint \n Cout = " + str(couuut)+"[/color][/b]"
                    self.l.texture_update()
                else:
                    self.list=[]
                    self.listchemin=[]
                    self.l.text = "[b][color=c1b5cc] But Non atteint \n Pas de chemin [/color][/b]"
                    self.l.texture_update()
    def aniamationset(self,list):
        if list!=[]:
            self.image.source = list[0]
            self.image.reload()
            list.remove(list[0])

    def getListImage(self,l):
        parcours=[]
        for i in range(0, len(l)):
            self.G = graphviz.Digraph(format="png")
            self.G.attr('node', shape='ellipse')
            for n in range(0, len(self.g.noeuds)):
                if self.g.noeuds[n] == l[i]:
                    self.G.node(name=self.g.noeuds[n],
                                xlabel="<<font color='blue'>" + self.g.heuristique[n] + "</font>>",
                                color="blue", style='filled', fillcolor="green")
                else:
                    self.G.node(name=self.g.noeuds[n],
                                xlabel="<<font color='blue'>" + self.g.heuristique[n] + "</font>>", color="blue")
            for a in range(0, len(self.g.arcs)):
                self.G.edge(self.g.arcs[a].split('=')[0].split(',')[0],
                            self.g.arcs[a].split('=')[0].split(',')[1], label=self.g.coutArc[a])
            parcours.append(self.G.render(filename="./animation/"+''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(7))))
        return parcours

if __name__ == '__main__':
    GraphApplicationApp().run()