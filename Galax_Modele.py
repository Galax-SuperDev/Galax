import random
import math



#######################################################
class Jeu:
    def __init__(self):
        nbEtoileNeutre = 10 #Ceci est hardcoder mais on pourait le passer au constructeur a partir du menu principal
        self.listeFaction = []
        self.listeFaction.append(Humain(self))
        self.listeFaction.append(Czin(self))
        self.listeFaction.append(Gubru(self))
        self.listeFaction.append(Neutral(nbEtoileNeutre,self))
       
    def getMergedListeEtoile(self):
        grosseListeEtoile = []
        for faction in self.listeFaction:
                for etoile in faction.listeEtoile:
                    grosseListeEtoile.append(etoile)
        return grosseListeEtoile
    
    def ajoutVaisseau(self):
        # ajout dans toutes les etoiles sauf etoiles mere
        for e in self.etoiles:
            e.flotte.nbVaisseaux += e.nbUsine
        #ajout dans les etoiles mere
        self.czin.flottes[0].nbVaisseaux += self.czin.etoiles[0].nbUsine
        self.gubru.flottes[0].nbVaisseaux += self.gubru.etoiles[0].nbUsine
        self.humain.flottes[0].nbVaisseaux += self.humain.etoiles[0].nbUsine

    def updateFlotte(self):
        for i in range(11):
            for faction in self.listeFaction:
                for etoile in faction.listeEtoiles:
                    if(i == 0)
                        etoile.ajouterVaisseau()
                    for flotte in etoile.listeFlotte:
                        if(i==0):
                            if(flotte.destination != None and not flotte.travelTime > 0 ): #Verif si il y a une destination, et si le temps de voyage n'est pas deja calculer
                                flotte.calcTravelTime()
                                flotte.isMoving = True
                        if(flotte.isMoving):
                            flotte.updateTravelTime()
                            if(travelTime == 0):
                                flotte.isMoving=False
                                if(isinstance(flotte.owner.parent,flotte.destination.parent)):#si c'est la meme faction
                                    flotte.destination.listeFlotte[0].nbVaisseaux += flotte.nbVaisseaux
                                else:
                                    flotte.bataille()







#######################################################
class Faction:
    def __init__(self,parent):
        self.listeEtoile=[]
        self.parent = parent

class Humain(Faction):
    def __init__(self, parent):
        Faction.__init__(self, parent)
        self.nom = 'Humain'
        self.listeEtoile.append(Etoile("Ohm",self))
        self.listeEtoile[0].nbUsine = 10
        
class Czin(Faction):
    def __init__(self, parent):
        Faction.__init__(self, parent)
        self.nom = 'Czin'
        self.listeEtoile.append(Etoile("Cygnus X-1",self))
        self.listeEtoile[0].nbUsine = 10
                
class Gubru(Faction):
    def __init__(self, parent):
        Faction.__init__(self, parent)
        self.nom = 'Gubru'
        self.listeEtoile.append(Etoile("Granatovaya",self))
        self.listeEtoile[0].nbUsine = 10

class Neutral(Faction):
    def __init__(self, nbEtoileNeutre, parent):
        Faction.__init__(self, parent)
        self.nbEtoileNeutre = nbEtoileNeutre
        self.nom = 'Neutral'
        self.listeEtoile = []
        self.setListeEtoileNeutre()

    def setListeEtoileNeutre(self):
        for i in range(self.nbEtoileNeutre):
            self.listeEtoile.append(Etoile(("Neutral "+str(i)), self))
            








#######################################################
class Etoile:
    def __init__(self,nom,owner):
        self.owner = owner
        self.posX = None
        self.posY = None
        self.setPosition()#afin d'attribuer une valeur a posX et posY
        self.nom = nom
        self.nbUsine = 0
        self.listeFlotte = []
        self.spyRank = 0
        if(not isinstance(owner, Neutral)):# lorsque le proprio de l'etoile n'est pas un neutral
            self.listeFlotte.append(Flotte(self,100))
            self.nbUsine = 10
            print(self.owner.nom)
        else:#cas neutral
            self.listeFlotte.append(Flotte(self,0))
            self.nbUsine = random.randint(0,6)
            print(self.nom)
    
    def ajoutVaisseau(self): 
        self.flotte.nbVaisseaux += self.nbUsine


#CALIS QU'IL Y A DU COMMENTAIRE DANS LA PROCHAINE FONCTION!!!
    def setPosition(self):  #attribut une position au hasare a l'etoile en verifiant de ne pas la mettre sur une etoile existante
        while(True):        #boucle infini qui s'arrete lorsque le dernier else est executer et arrive au return
            posX = random.randint(0,100)
            posY = random.randint(0,100)  
            for faction in self.owner.parent.listeFaction:          #pour chaque faction dans la liste de faction
                for etoile in faction.listeEtoile:                  #pour chaque etoile dans la liste d'etoile contenue dans chaque faction
                    if( posX==etoile.posX and posY==etoile.posY):   #si la position de l'etoile courante est egale a la position d'une autre etoile
                        break       #fait sortir du 2e "for", qui nous ammene au second break
                else:               #si la 2e boucle finis sans heurt
                    continue        #retourne et continue l'iteration dans le 1er "for"
                break               #fait sortir du 1er "for", qui nous ammène au "while" au dessus
            else:                   #si les deux boucles ont finis sans rencontrer une seule fois une etoile a la meme position que l'etoile courante
                self.posX = posX    #attribution de la position en x
                self.posY = posY    #attribution de la position en y
                print(str(posX)+' '+str(posY))#print la position de l'etoile
                return              #quitte la fonction










        


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

    def bataille(self):
        nbVaisseauDefence = self.destination.listeFlotte[0].nbVaisseaux
        tourDefence = True
        if(nbVaisseauDefence > self.nbVaisseaux)
            if(attaqueSurprise(nbVaisseauDefence)):
                tourDefence = False

        
        while(nbVaisseauDefence != 0 or self.nbVaisseaux != 0):
            if(random.randint(0,10) > 6):
                turnValue = -1
            else:
                turnValue = 0
            if(tourDefence):
                self.nbVaisseaux += turnValue
                tourDefence = False
            else:
                nbVaisseauDefence += turnValue



    def attaqueSurprise(self,nbVaisseauDefence):
        ratio = nbVaisseauDefence/self.nbVaisseaux
        if(ratio < 5): 
            P = ratio / 10
        elif(ratio < 20):
            P = (3 * ratio + 35) /100
        else:
            P = 0.95

        if(random.randint(0,100) < P*100):
            return True
        else:
            return False


