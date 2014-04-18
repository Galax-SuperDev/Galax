import random
import math



#######################################################
class Jeu:
	#on doit ajouter une valeur du temps qui passe a utiliser dans la creation de flottes des AI
    def __init__(self):
        nbEtoileNeutre = 50 #Ceci est hardcoder mais on pourait le passer au constructeur a partir du menu principal
        print("Le nombre d'etoile est set a la 9eme ligne du modele a " + str(nbEtoileNeutre))
        self.listeFaction = []
        self.listeFaction.append(Humain(self))
        self.listeFaction.append(Czin(self))
        self.listeFaction.append(Gubru(self))
        self.listeFaction.append(Neutral(nbEtoileNeutre,self))
        self.anneePassees = 0
       
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
        for faction in self.listeFaction:
            for flotte in faction.listeFlotteEnMouvement:
                if(flotte.estRendu()):
                    flotte.isMoving=False
                    if(isinstance(flotte.owner,flotte.destination)):#si c'est la meme faction
                        flotte.destination.mergeFlotte(flotte)
                    else:
                        flotte.bataille()
                else:
                    flotte.updateTravelTime()

    def initialiserValeurGrappe():
        for faction in self.listeFaction:
            for etoile in faction.listeEtoile:
                etoile.valeurGrappe = 0







#######################################################
class Faction:
    def __init__(self,parent):
        self.listeEtoile = []
        self.listeFlotteEnMouvement = []
        self.parent = parent

class Humain(Faction):
    def __init__(self, parent):
        Faction.__init__(self, parent)
        self.nom = 'Humain'
        self.listeEtoile.append(Etoile("Soleil",self))
        self.listeEtoile[0].nbUsine = 10

    def isDead():
        if(self.listeEtoile.size() == 0 and self.listeFlotteEnMouvement == 0):
            return True
        
class Czin(Faction):
    def __init__(self, parent):
        Faction.__init__(self, parent)
        self.nom = 'Czin'
        self.listeEtoile.append(Etoile("Etoile Czin",self))
        self.etoileCourante = self.listeEtoile[0]
        self.listeEtoile[0].nbUsine = 10
        self.listeEtoile[0].flotteStationnaire = Flotte(self,100)
        self.distanceGrappe = 4

    def formationFlotte():
        pass
    def determinerGrappe():
        self.parent.initialiserValeurGrappe()
        for faction in self.listeFaction:
            for A in faction.listeEtoile:
                for faction in self.listeFaction:
                    for B in faction.listeEtoile:
                        distance = getDistance(A,B)
                        if(distance <= self.distanceGrappe):
                            s = self.distanceGrappe - distance + 1
                            A.valeurGrappe = s*s

    def getDistance(self,A,B):
        return math.sqrt((B.posX-A.posX)**2+(B.posY-A.posY)**2)



                
class Gubru(Faction):
    def __init__(self, parent):
        Faction.__init__(self, parent)
        self.nom = 'Gubru'
        self.listeEtoile.append(Etoile("Etoile Gubru",self))
        self.listeEtoile[0].nbUsine = 10
        self.listeEtoile[0].flotteStationnaire = Flotte(self,100)
        self.nbr_vaisseau_par_attaque = 5
        self.force_attaque_basique = 10

    def formationFlotte():
    	if (Jeu.anneesPassees > 0):
    		self.force_attaque = Jeu.anneesPassees * (self.nbr_vaisseau_par_attaque + self.force_attaque_basique)
    	else:
    		self.force_attaque = force_attaque_basique * 2
    	
    	while(self.listeEtoile[0].nbVaisseaux >= force_attaque+force_attaque_basique ):
    		self.listeEtoile[0].nouvelleFlotte = Flotte(self,force_attaque)
    		
    def trouverEtoilePlusPres(self,etoileDeBase):
    	self.etoilePlusPres = None
        self.distance = 0
        self.distancePlusPres = 0


        for faction in self.listeFaction: #pour chaque faction
            if (faction.nom != "Gubru"): # qui ne sont pas Gubru
                for etoile in faction.listeEtoile: # on regarde a travers toutes les etoiles
                   distance = abs((etoile.posX - self.listeEtoile[0].posX)+ (etoile.posY - self.listeEtoile[0].posY)) #on etabli la distance
                   if(distance <= distancePlusPres): # on regarde si la distance est plus petite que la plus petite distance trouver a date
                        self.etoilePlusPres = etoile # on a trouver l'etoile la plus pres

        return self.etoilePlusPres


    	
    		
        

class Neutral(Faction):
    def __init__(self, nbEtoileNeutre, parent):
        Faction.__init__(self, parent)
        self.nbEtoileNeutre = nbEtoileNeutre
        self.nom = 'Neutral'
        self.setupListes()

    def setupListes(self):
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
        self.flotteStationnaire = Flotte(self,0)
        self.flotteAuDernierPassage = -1
        self.spyRank = 0
        self.nbUsine = random.randint(0,6)
        self.valeurGrappe = 0
        print(self.nom,end=' -> ')
        print(str(self.posX)+' '+str(self.posY))#print la position de l'etoile
    
    def ajoutVaisseau(self): 
        self.flotteStationnaire.nbVaisseaux += self.nbUsine

    def updateSpyRank(self):
        if(self.spyRank < 3):
            self.spyRank += 1
        self.flotteAuDernierPassage = self.flotteStationnaire.nbVaisseaux


    def getNbVaisseau(self):
        if(self.spyRank == 0 or self.spyRank == 1 or self.spyRank == 2):
            return self.flotteAuDernierPassage
        elif(isinstance(owner,Humain) or self.spyRank == 3):
            return self.flotteStationnaire.nbVaisseaux

    def getNbUsine(self):
        if(self.spyRank == 0 or self.spyRank == 1):
            return -1       #afin de pouvoir donner la liberter de choisir le message aproprie a�afficher
        elif(self.spyRank == 2 or self.spyRank == 3 or isinstance(owner,Humain)):
            return self.nbUsine

    def gotTakenBy(self,newOwner):
        self.owner = newOwner
        self.flotteAuDernierPassage = 0

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
                return              #quitte la fonction








#######################################################
class Flotte:
    def __init__(self,owner,nbVaisseaux):
        self.owner = owner
        self.nbVaisseaux = nbVaisseaux
        self.travelTime = 0
        self.destination = None

    def mergeFlotte(laFlotteAnnexe):
        self.nbVaisseaux += laFlotteAnnexe.nbVaisseaux
		if(self.nbVaisseaux - laFlotteAnnexe.nbVaisseaux >= 0 ) # il y a un if puisqu'il se peut que la flotte annexe arrive sur une etoile sans flotte donc il ne faut pas supprimer laFlotteAnnexe
			del laFlotteAnnexe # on delete la flotte annexe puisque elle donne tout ses vaisseaux a la flotte sur l'etoile

    def calcTravelTime(self):
        distance = abs((self.destination.posX - self.owner.posX)+
                            (self.destination.posY - self.owner.posY))
        if(distance <= 2):
            self.travelTime = distance/2
        else:
            self.travelTime = 1+((distance-2)/3)

    def estRendu(self):
        if(self.travelTime == 0):
            return True
        else:
            return False
    
    def updateTravelTime(self):
        travelTime -= 0.1
    
    def setDestination(self,etoile):
        self.destination = etoile

    def bataille(self):
        nbVaisseauDefence = self.destination.listeFlotte[0].nbVaisseaux
        tourDefence = True
        if(nbVaisseauDefence > self.nbVaisseaux):
            print("Possibilité d'attaque surprise...")
            if(attaqueSurprise(nbVaisseauDefence)):
                tourDefence = False
                print("Ahaha! Attaque surprise!!!")        
        while(nbVaisseauDefence != 0 or self.nbVaisseaux != 0):
            if(random.randint(0,10) > 6):
                turnValue = -1
                print("Perte d'un vaisseau pour les",end=' ')
            else:
                turnValue = 0
            if(tourDefence):
                self.nbVaisseaux += turnValue
                tourDefence = False
                print("attaquant")
            else:
                nbVaisseauDefence += turnValue
                print("defenseur")
        else:
            if(nbVaisseauDefence == 0):
                return self.owner
            else:
                return self.destination.owner



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


