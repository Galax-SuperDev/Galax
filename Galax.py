from tkinter import *
import random
import math

class Etoile:
    def __init__(self,posX,posY,nom,owner):
        self.posX = posX
        self.posY = posY
        self.nom = nom
        self.nbUsine = random.randint(0,6)
        self.listeFlotte = []
        self.spyRank = 0
        self.owner = owner
        self.listeFlotte[0].append(Flotte(self,100))
    
    def AjoutVaisseau(self): 
        self.flotte.nbVaisseaux += self.nbUsine
        
class Flotte:
    def __init__(self,owner,nbVaisseaux):
        self.owner = owner
        self.nbVaisseaux = nbVaisseaux
        self.travelTime = 0
        self.destination = None
        self.isMoving = False

    def calcTravelTime(self):
        distance = abs((self.destination.posX - self.owner.posX)+
                            (self.destination.posY - self.owner.posY))
        if(distance <= 2):
            self.travelTime = distance/2
        else:
            self.travelTime = 1+((distance-2)/3)
    
    def updateTravelTime(self):
        travelTime -= 0.1
    
    def setDestination(etoile):
        self.destination = etoile

class Faction:
    def __init__(self):
        self.etoiles=[]

class Humain(Faction):
    def __init__(self):
        Faction.__init__(self)
        self.nom = 'Humain'
        self.etoiles.append(Etoile(10,10,"Ohm",self))
        self.etoiles[0].nbUsine = 10
        
class Czin(Faction):
    def __init__(self):
        Faction.__init__(self)
        self.nom = 'Czin'
        self.etoiles.append(Etoile(20,30,"Cygnus X-1","Czin"))
        self.etoiles[0].nbUsine = 10
        self.flottes.append(Flotte(self.nom,100))
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
        self.etoiles = self.creeEtoiles(8)
       
    def creeEtoiles(self,nbEtoiles):
        etoilesTemp = []
        for i in range(0,nbEtoiles):
            posX = random.randint(0,100)
            posY = random.randint(0,100)
            posValide = False
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
                    posX = random.randint(0,100)
                    posY = random.randint(0,100)
            etoilesTemp.append(Etoile(posX,posY,"Zimbaboo","Neutral"))
            print(str(posX)+' '+str(posY))
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
    def __init__(self,listeEtoile):
        self.listeEtoiles = listeEtoile
        self.root=Tk()
              
        self.root.title('Galax')
        self.root.iconbitmap(default='galaxIcon.ico')
              
        self.screenWidth = 1280
        self.screenHeight = 768
        self.width = 1024
        self.height = 640
        self.canvas=Canvas(self.root, width=self.screenWidth, height=self.screenHeight, bg='black')  
              
        self.canvas.bind('<Configure>', self.resize)
        self.canvas.bind('<Button-1>', self.click)
    
        self.canvas.pack(expand=True, fill=BOTH)
        
        self.drawMenu()
        '''
        self.canvas.create_rectangle(0,self.screenHeight-128,
                             self.screenWidth,self.screenHeight,
                             fill='gray',tags='menuBar')
        
        self.canvas.create_rectangle(self.screenWidth-256,0,
                                     self.screenWidth,self.screenHeight-256,
                                     fill='gray',tags='menuBar')
        
        self.background = PhotoImage(file="cosmosBG.gif")
        #self.background.zoom(self.width, self.height)
        self.canvas.create_image(0,0,anchor=NW,image=self.background)

        self.drawEtoiles()
        '''
    def click(self,event):
        eventX = event.x
        eventY = event.y
        print(str(eventX)+str(eventY))
    
    def resize(self,event):
        self.screenWidth = event.width
        self.screenHeight = event.height
        self.width = self.screenWidth-256;
        self.height = self.screenHeight-128;
        
        self.drawMenu()
        
        '''
        self.canvas.delete("menuBar")
        self.canvas.create_rectangle(0,self.screenHeight-128,
                                     self.screenWidth,self.screenHeight,
                                     fill='gray',tags="menuBar")
        
        self.canvas.create_rectangle(self.screenWidth-256,0,
                                     self.screenWidth,self.screenHeight-128,
                                     fill='gray',tags="menuBar")
        '''
        
    def drawMenu(self):
        
        self.buttonWidth = 200
        self.buttonHeight = 64
        
        buttonPosX = ((self.screenWidth/2)-self.buttonWidth/2)
        buttonPosY = self.screenHeight/3
        
        self.canvas.delete("menu")
        
        self.canvas.create_rectangle(buttonPosX, buttonPosY,
                                     buttonPosX+self.buttonWidth, buttonPosY+self.buttonHeight, 
                                     fill='gray', activefill='white', tags='menu')
        
        self.canvas.create_rectangle(buttonPosX, buttonPosY+self.buttonHeight+2,
                                     buttonPosX+self.buttonWidth, buttonPosY+(self.buttonHeight*2)+2, 
                                     fill='gray', activefill='white', tags='menu')
        
        self.canvas.create_rectangle(buttonPosX,buttonPosY+(self.buttonHeight*2)+4,
                                     buttonPosX+self.buttonWidth,buttonPosY+(self.buttonHeight*3)+4,
                                     fill='gray',activefill='white',tags='menu')
        
        self.canvas.create_text(buttonPosX+100,buttonPosY+32,
                                text='New game',fill='black',activefill='white',
                                font=('consolas','16'),
                                tags='menu')
        self.canvas.create_text(buttonPosX+100,buttonPosY+96,
                                text='High scores',
                                fill='black',activefill='white',
                                font=('consolas','16'),
                                tags='menu')
        self.canvas.create_text(buttonPosX+100,buttonPosY+160,
                                text='Quit game',
                                fill='black',activefill='white',
                                font=('consolas','16'),
                                tags='menu')
        
    def drawEtoiles(self):
        for e in self.listeEtoiles:
            posX = int((e.posX*self.width-100)/100)
            posY = int((e.posY*self.height-100)/100)
            self.canvas.create_oval(posX,posY,posX+32,posY+32,fill='green')
            print(str(posX)+' '+str(posY))

class Controlleur:
    def __init__(self):
        self.jeu=Jeu(self)
        self.vue=Vue(self.jeu.etoiles)
        self.vue.root.mainloop()
        
if __name__ == '__main__':
    c=Controlleur()