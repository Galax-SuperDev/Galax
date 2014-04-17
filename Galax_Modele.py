import random
import math



#######################################################
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



#######################################################
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
        self.etoiles.append(Etoile(20,30,"Cygnus X-1",self))
        self.etoiles[0].nbUsine = 10
                
class Gubru(Faction):
    def __init__(self):
        Faction.__init__(self)
        self.nom = 'Gubru'
        self.etoiles.append(Etoile(20,30,"Granatovaya",self))
        self.etoiles[0].nbUsine = 10

class Neutral(Faction):
    def __init__(self):
        self.nom = 'Neutral'
        self.setListEtoile()

    def setListEtoile(self):


#######################################################
class Etoile:
    def __init__(self,posX,posY,nom,owner):
        self.posX = posX
        self.posY = posY
        self.nom = nom
        self.nbUsine = random.randint(0,6)
        self.listeFlotte = []
        self.spyRank = 0
        self.owner = owner
        if(not isinstance(owner, Neutral)):# lorsque le proprio de l'etoile n'est pas un neutral
            self.listeFlotte.append(Flotte(self,100))
        else:
    
    def AjoutVaisseau(self): 
        self.flotte.nbVaisseaux += self.nbUsine
        


#######################################################
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
    
    def setDestination(self,etoile):
        self.destination = etoile
        