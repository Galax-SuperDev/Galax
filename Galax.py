from tkinter import *
import random
import math

class Etoile:
    def __init__(self,posX,posY,nom,owner):
        self.posX = posX
        self.posY = posY
        self.nom = nom
        self.nbUsine = random.randint(0,6)
        self.flotte = Flotte("neutral",0)
        self.spyRank = 0
        self.owner = owner
        #self.type = random(0 .... n)
        
class Flotte:
    def __init__(self,owner,nbVaisseaux):
        self.owner = owner
        self.nbVaisseaux = nbVaisseaux
        self.travelTime = 0
        self.positionCourante = None
        self.desitnation = None

    def calcTravelTime(self):
        distance = abs((self.destination.posX - self.positionCourante.posX)+
                            (self.desitnation.posY - self.positionCourante.posY))
        if(distance <= 2):
            self.travelTime = distance/2
        else:
            self.travelTime = 1+((distance-2)/3)

class Faction:
    def __init__(self):
        self.etoiles=[]
        self.flottes=[]

class Humain(Faction):
    def __init__(self):
        Faction.__init__(self)
        self.nom = 'Humain'
        self.etoiles.append(Etoile(10,10,"Ohm","Humain"))
        self.etoiles[0].nbUsine = 10
        self.flottes.append(Flotte("Humain",100))
        self.flottes[0].positionCourante = self.etoiles[0]
        
class Czin(Faction):
    def __init__(self):
        Faction.__init__(self)
        self.nom = 'Czin'
        self.etoiles.append(Etoile(20,30,"Cygnus X-1","Czin"))
        self.etoiles[0].nbUsine = 10
        self.flottes.append(Flotte("Czin",100))
        self.flottes[0].positionCourante = self.etoiles[0]
                
class Gubru(Faction):
    def __init__(self):
        Faction.__init__(self)
        self.nom = 'Gubru'
        self.etoiles.append(Etoile(20,30,"Granatovaya","Gubru"))
        self.etoiles[0].nbUsine = 10
        self.flottes.append(Flotte("Gubru",100))
        self.flottes[0].positionCourante = self.etoiles[0]

class Jeu:
    def __init__(self,parent):
        self.parent = parent
        self.humain = Humain()
        self.czin = Czin()
        self.gubru = Gubru()
        self.sizeCase = 16
        self.etoiles = self.creeEtoiles(16)
        
       
    def creeEtoiles(self,nbEtoiles):
        etoilesTemp = []
        posX = random.randint(0,100)
        posY = random.randint(0,100)
        posValide = False
        for i in range(0,nbEtoiles):
            while posValide == False:
                    # si la position de l'etoile est egale a la position d'une etoile mere
                    if( posX==self.humain.etoiles[0].posX and posY==self.humain.etoiles[0].posY):
                        posValide = False
                    elif( posX==self.gubru.etoiles[0].posX and posY==self.gubru.etoiles[0].posY):
                        posValide = False
                    elif( posX==self.czin.etoiles[0].posX and posY==self.czin.etoiles[0].posY):
                        posValide = False
                    else:
                        posValide = True
                        
                    # si la position de l'etoile est egale a la position d'une autre etoile   
                    for e in etoilesTemp:
                        if(posX == e.posX and posY == e.posY):
                            posValide = False
                        else:
                            posValide = True
                    # si la position n'est pas valide on donne une nouvelle position a l'etoile et on recommence la boucle
                    if(posValide == False):
                        posX = random.randint(0,(parent.width-1)/self.sizeCase)
                        posY = random.randint(0,(parent.height-1)/self.sizeCase)
            etoilesTemp.append(Etoile(posX,posY,"Zimbaboo","Neutral"))
        return etoilesTemp
    
    def AjoutVaisseau(self):
        # ajout dans toutes les etoiles sauf etoiles mere
        for e in self.etoiles:
            e.flotte.nbVaisseaux += e.nbUsine
        #ajout dans les etoiles mere
        self.czin.flottes[0].nbVaisseaux += self.czin.etoiles[0].nbUsine
        self.gubru.flottes[0].nbVaisseaux += self.gubru.etoiles[0].nbUsine
        self.humain.flottes[0].nbVaisseaux += self.humain.etoiles[0].nbUsine
            
        
        
class Vue:
    def __init__(self,parent):
        self.parent=parent
        self.root=Tk()
              
        self.root.title('Galax')
        self.root.iconbitmap(default='galaxIcon.ico')
              
        self.screenWidth = 1280
        self.screenHeight = 768
        self.width = 1024
        self.height = 640
        self.canvas=Canvas(self.root, width=self.screenWidth, height=self.screenHeight, bg='black')  
              
        self.canvas.bind('<Configure>', self.resize)
        
        self.canvas.create_rectangle(0,self.screenHeight-128,
                                     self.screenWidth,self.screenHeight,
                                     fill='gray',tags='menuBar')
        
        self.canvas.create_rectangle(self.screenWidth-256,0,
                                     self.screenWidth,self.screenHeight-256,
                                     fill='gray',tags='menuBar')
          
        self.canvas.pack(expand=True, fill=BOTH)
        self.drawEtoiles()
        
    def drawEtoiles(self):
        self.canvas.create_oval(10,10,20,20,fill='green')

    def resize(self,event):
        self.screenWidth = event.width
        self.screenHeight = event.height
        self.width = self.screenWidth-256;
        self.height = self.screenHeight-128;

        self.canvas.delete("menuBar")
        self.canvas.create_rectangle(0,self.screenHeight-128,
                                     self.screenWidth,self.screenHeight,
                                     fill='gray',tags="menuBar")
        
        self.canvas.create_rectangle(self.screenWidth-256,0,
                                     self.screenWidth,self.screenHeight-128,
                                     fill='gray',tags="menuBar")

class Controlleur:
    def __init__(self):
        self.jeu=Jeu(self)
        self.vue=Vue(self)
        self.vue.root.mainloop() 
        
if __name__ == '__main__':
    c=Controlleur()