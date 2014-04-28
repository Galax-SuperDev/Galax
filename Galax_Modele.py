import random
import math



#######################################################
class Jeu:
    def __init__(self,nbEtoilesTotales):
        self.compteurEtoile = 0
        self.listeFaction = []
        print("********** Spawning etoiles ***********************")
        self.humain = Humain(self)
        self.gubru = Gubru(self)
        self.czin = Czin(self)
        self.neutral = Neutral(nbEtoilesTotales-3,self)
        self.listeFaction.append(self.humain)
        self.listeFaction.append(self.gubru)
        self.listeFaction.append(self.czin)
        self.listeFaction.append(self.neutral)
        self.anneePassees = 0
        print("********** Nombre total d'etoile : " + str(self.compteurEtoile)+" *************")
        print("********** Mouvement du joueur ********************")


    def getMergedListeEtoile(self):
        grosseListeEtoile = []
        for faction in self.listeFaction:
            for etoile in faction.listeEtoile:
                grosseListeEtoile.append(etoile)

        return grosseListeEtoile

    def ajoutVaisseau(self):
        for faction in self.listeFaction:
            for etoile in faction.listeEtoile:
                etoile.ajoutVaisseau()

    def gestionTroupes(self):
        for faction in self.listeFaction:
            faction.reorganisationDesFlottes()

    def moveFlotteEnMouvement(self):
        for faction in self.listeFaction:
            for flotte in faction.listeFlotteEnMouvement:
                if(flotte.estRendu()):
                    print("Une flotte de:"+str(flotte.nbVaisseaux)+" appartenant au:"+str(flotte.owner.nom)+" est arrive sur:"+str(flotte.destination.nom))
                    if(flotte.owner.nom == flotte.destination.owner.nom):#si c'est la meme faction
                        flotte.destination.flotteStationnaire.mergeFlotte(flotte)
                        print("Flotte:"+str(flotte.nbVaisseaux)+" merge avec la flotte de l'etoile:"+str(flotte.destination.nom))
                    else:                                                 #Sinon, c'est la bataille!
                        flotte.bataille()
                        if(flotte.flagBataille == True):                    #si c'est l'attaquant qui a gagne la bataille
                            print("Les:"+str(flotte.owner.nom)+" on capturer:"+str(flotte.destination.nom)+" aux mains des:"+str(flotte.destination.owner.nom))
                            flotte.destination.flotteStationnaire = Flotte(flotte.owner,flotte.nbVaisseaux,None,None)
                            flotte.owner.changeEtoileOwner(flotte.destination.owner,flotte.destination)
                        else:                                               #si les defenseurs ont gagne la bataille
                            print("Les:"+str(flotte.destination.owner.nom)+" on defendu la planete:"+str(flotte.destination.nom)+" contre les:"+str(flotte.owner.nom))
                            pass

                    faction.listeFlotteEnMouvement.remove(flotte)#suppression de la flotte.
                else:
                    flotte.updateTravelTime()


    def lancerFlotteHumain(self,etoileDepart,etoileDestination,force):
    	etoileDepart.envoyerNouvelleFlotte(force,etoileDestination)







#######################################################
class Faction:
    def __init__(self,parent):
        self.listeEtoile = []
        self.listeFlotteEnMouvement = []
        self.parent = parent

    def isDead(self):
        if(len(self.listeEtoile) == 0 and len(self.listeFlotteEnMouvement) == 0):
            return True

    def changeEtoileOwner(self,oldOwner,etoileCapturer):
        etoileCapturer.gotTakenBy(self)
        self.listeEtoile.append(oldOwner.listeEtoile.pop(oldOwner.listeEtoile.index(etoileCapturer)))

    def getDistance(self,A,B):
        return math.sqrt((B.posX-A.posX)**2+(B.posY-A.posY)**2)

    def flotteEnRouteVers(self,etoileSujet):
        for flotte in self.listeFlotteEnMouvement:
            if(flotte.destination.nom == etoileSujet.nom):
                return True
        return False

    def trouverEtoilePlusProche(self,etoileSujet):
        listeDeTouteLesEtoile = self.parent.getMergedListeEtoile()
        etoilePlusProche = None
        for etoile in listeDeTouteLesEtoile:
            if(etoile.owner.nom is not self.nom): #si l'etoile n'est pas Czin
                if(not self.flotteEnRouteVers(etoile)): #si il n'y a pas deja une flotte en direction de l'etoile
                    if(etoile.nom is not etoileSujet.nom): 
                        if(not etoilePlusProche): #si il n'y a pas d'etoilePlusProche deja Setter
                            etoilePlusProche = etoile
                        else:
                            distance = self.getDistance(etoile,etoileSujet)
                            distancePlusProche = self.getDistance(etoilePlusProche,etoileSujet)
                            if(distance < distancePlusProche):
                                etoilePlusProche = etoile
        else:
            return etoilePlusProche

    def reorganisationDesFlottes(self):
        pass#fonction abstraite a overrider si necessaire


class Humain(Faction):
    def __init__(self, parent):
        Faction.__init__(self, parent)
        self.nom = 'Humain'
        self.listeEtoile.append(Etoile("Soleil",self))
        self.listeEtoile[0].nbUsine = 10
        self.listeEtoile[0].flotteStationnaire = Flotte(self,100,None,None)


class Czin(Faction):
    def __init__(self, parent):
        Faction.__init__(self, parent)
        self.nom = 'Czin'
        self.listeEtoile.append(Etoile("Etoile Czin",self))
        self.listeEtoile[0].nbUsine = 10
        self.listeEtoile[0].flotteStationnaire = Flotte(self,100,None,None)
        self.etoileBase = self.listeEtoile[0]
        self.etoileBaseProspective = self.listeEtoile[0]
        self.armada = None
        self.armadaPasEnvoyer = True

        self.distanceGrappe = 4
        self.distance_rassemblement = 6
        self.force_attaque_basique = 20
        self.nbr_vaisseaux_par_attaque = 4

        self.mode_rassemblement_forces = 0
        self.mode_etablir_base = 1
        self.mode_conquerir_grappe = 2
        self.mode = self.mode_rassemblement_forces

    def getForceAttaque(self):
        return self.parent.anneePassees+1 * self.nbr_vaisseaux_par_attaque * self.force_attaque_basique

    def reorganisationDesFlottes(self):
        if(self.etoileBase.owner.nom is not "Czin"): #si les Czin perdent leur base, ils se replient vers leur etoile en position listeEtoile[0]
            self.etoileBase = self.listeEtoile[0]
            self.mode = mode_rassemblement_forces
        ceci = True
        while ceci is True:
            if(self.mode == self.mode_etablir_base):
                print("modeEtablirBase")
                ceci = self.etablirBase()
            if(self.mode == self.mode_conquerir_grappe):
                print("mode_conquerir_grappe")
                ceci = self.conquerirGrappe()
            if(self.mode == self.mode_rassemblement_forces):
                print("mode_rassemblement_forces")
                self.rassemblementForces()
                ceci = self.changementModRassemblementForce()

    def etablirBase(self):
        if(self.armadaPasEnvoyer):
            self.armadaPasEnvoyer = False
            self.etoileBaseProspective = self.choisirBase()
            self.etoileBase.envoyerNouvelleFlotte(self.etoileBase.flotteStationnaire.nbVaisseaux, self.etoileBaseProspective)
            self.armada = self.listeFlotteEnMouvement[len(self.listeFlotteEnMouvement)-1]
            return False
        elif(not self.listeFlotteEnMouvement or not (self.listeFlotteEnMouvement and self.listeFlotteEnMouvement.count(self.armada))):#si l'armada est arrive a destination et c'est battu
            self.armadaPasEnvoyer = True
            if(self.etoileBaseProspective.owner.nom == self.nom):#si la baseProspective est en possession des Czins
                self.etoileBase = self.etoileBaseProspective
                self.mode = self.mode_conquerir_grappe
            else:                                       #sinon, ca veux dire que les defenseurs ont gagne.
                self.mode = self.mode_rassemblement_forces
            return True
        else:
            return False
    def conquerirGrappe(self):
        nbEnvoi = self.getForceAttaque()
        while(self.etoileBase.flotteStationnaire.nbVaisseaux >= nbEnvoi):
            self.etoileBase.envoyerNouvelleFlotte(nbEnvoi,self.trouverEtoilePlusProche(self.etoileBase))
        else:
            self.mode = self.mode_rassemblement_forces
            return True

    def rassemblementForces(self):
        for etoile in self.listeEtoile:
            if(self.etoileBase.nom is not etoile.nom):
                if(self.getDistance(etoile,self.etoileBase) < 6):
                    etoile.envoyerNouvelleFlotte(etoile.flotteStationnaire.nbVaisseaux,self.etoileBase)
    def changementModRassemblementForce(self):
        print(3*self.getForceAttaque())
        print(self.etoileBase.flotteStationnaire.nbVaisseaux)
        if(3*self.getForceAttaque() <= self.etoileBase.flotteStationnaire.nbVaisseaux):
            self.mode = self.mode_etablir_base
            return True
        else:
            return False

    def choisirBase(self):
        self.initialiserValeurGrappe()
        self.determinerGrappe()
        etoileRetour = None
        grosseListeEtoile = self.parent.getMergedListeEtoile()
        for etoile in grosseListeEtoile:
            if(not isinstance(etoile.owner,Czin)):
                if(etoileRetour == None):
                    etoileRetour = etoile
                if(etoile.valeurGrappe == 0):
                    etoile.valeurBase = 0
                else:
                    etoile.valeurBase = etoile.valeurGrappe-3*self.getDistance(self.etoileBase,etoile)
                    if(etoile.valeurBase > etoileRetour.valeurBase):
                        etoileRetour = etoile
        return etoileRetour

    def initialiserValeurGrappe(self):
        for faction in self.parent.listeFaction:
            for etoile in faction.listeEtoile:
                etoile.valeurGrappe = 0

    def determinerGrappe(self):
        for faction in self.parent.listeFaction:
            for A in faction.listeEtoile:
                for faction in self.parent.listeFaction:
                    for B in faction.listeEtoile:
                        distance = self.getDistance(A,B)
                        if(distance <= self.distanceGrappe):
                            s = self.distanceGrappe - distance + 1
                            A.valeurGrappe = s*s




class Gubru(Faction):
    def __init__(self, parent):
        Faction.__init__(self, parent)
        self.nom = 'Gubru'
        self.listeEtoile.append(Etoile("Etoile Gubru",self))
        self.listeEtoile[0].nbUsine = 10
        self.listeEtoile[0].flotteStationnaire = Flotte(self,100,None,None)
        self.nbr_vaisseau_par_attaque = 5
        self.force_attaque_basique = 10
        self.force_attaque = 0


    def formationFlotte(self):
        if (self.parent.anneePassees > 0):
            self.force_attaque = self.parent.anneePassees * (self.nbr_vaisseau_par_attaque + self.force_attaque_basique)
        else:
            self.force_attaque = self.force_attaque_basique * 2

        if(self.listeEtoile):
            while(self.listeEtoile[0].flotteStationnaire.nbVaisseaux >= self.force_attaque + self.force_attaque_basique ):
                self.listeEtoile[0].envoyerNouvelleFlotte(self.force_attaque,self.trouverEtoilePlusProche(self.listeEtoile[0]))

    def reorganisationDesFlottes(self): #cela doit etre fait a chaque tour
        for etoile in self.listeEtoile:
            if(etoile.nom != self.listeEtoile[0].nom): # on ne veux pas envoyer de flottes de l'etoile mere vers l'etoile mere
                if (etoile.flotteStationnaire.nbVaisseaux > 25):
                    etoile.envoyerNouvelleFlotte(etoile.flotteStationnaire.nbVaisseaux - 15,self.listeEtoile[0])
                elif(etoile.flotteStationnaire.nbVaisseaux > 0):
                    etoile.envoyerNouvelleFlotte(etoile.flotteStationnaire.nbVaisseaux,self.listeEtoile[0])
        self.formationFlotte()



class Neutral(Faction):
    def __init__(self, nbEtoileNeutre, parent):
        Faction.__init__(self, parent)
        self.nom = 'Neutral'
        self.tabNomPossible = []
        self.setupListes(nbEtoileNeutre)


    def donnerNomEtoile(self):
        if(not self.tabNomPossible):#si le fichier n'est pas encore parser...
            fileHandle = open('listeNomEtoile.txt','r')
            for ligne in fileHandle.readlines():
                self.tabNomPossible.append(str(ligne).rstrip())
            else:
                fileHandle.close()
        return self.tabNomPossible.pop(random.randint(0,len(self.tabNomPossible)-1))

    def setupListes(self,nbEtoileNeutre):
        for i in range(nbEtoileNeutre):
            self.listeEtoile.append(Etoile(Neutral.donnerNomEtoile(self), self))





#######################################################
class Etoile:
    def __init__(self,nom,owner):
        self.nom = nom
        self.owner = owner
        self.posX = None
        self.posY = None
        self.setPosition()#afin d'attribuer une valeur a posX et posY
        self.flotteStationnaire = Flotte(self.owner, 0, None, None)
        self.flotteAuDernierPassage = -1
        self.spyRank = 0
        self.nbUsine = random.randint(0,6)
        self.valeurGrappe = 0
        self.valeurBase = 0
        print(self.nom,end=' -> ')
        print(str(self.posX)+' '+str(self.posY))#print la position de l'etoile
        self.owner.parent.compteurEtoile += 1

    def envoyerNouvelleFlotte(self,nbVaisseaux,etoileDestination):
        if(nbVaisseaux > 0):
            nouvelleFlotte = Flotte(self.owner, nbVaisseaux, self, etoileDestination)
            nouvelleFlotte.calcTravelTime()
            self.owner.listeFlotteEnMouvement.append(nouvelleFlotte)
            self.flotteStationnaire.nbVaisseaux -= nbVaisseaux
            print(str(self.owner.nom) + " -> Flotte:" + str(nbVaisseaux) + ", Depart:" + str(self.nom) + ", Destination:" + str(etoileDestination.nom))
        else:
            print("flotte nulle")

    def ajoutVaisseau(self):
        self.flotteStationnaire.nbVaisseaux += self.nbUsine*random.randint(10,20)

    def updateSpyRank(self):
        if(self.spyRank < 3):
            self.spyRank += 1
        self.flotteAuDernierPassage = self.flotteStationnaire.nbVaisseaux

    def getNbVaisseau(self):
        if(isinstance(self.owner,Humain) or self.spyRank == 3):
            return self.flotteStationnaire.nbVaisseaux
        elif(self.spyRank == 0 or self.spyRank == 1 or self.spyRank == 2):
            return self.flotteAuDernierPassage


    def getNbUsine(self):
        if(isinstance(self.owner,Humain) or self.spyRank == 2 or self.spyRank == 3):
            return self.nbUsine
        if(self.spyRank == 0 or self.spyRank == 1):
            return -1


    def gotTakenBy(self,newOwner):
        self.owner = newOwner
        self.flotteAuDernierPassage = -1

    def setPosition(self):  #attribut une position au hasare a l'etoile en verifiant de ne pas la mettre sur une etoile existante
        while(True):        #boucle infini qui s'arrete lorsque le dernier else est executer et arrive au return
            posX = random.randint(0,31)
            posY = random.randint(0,19)
            for faction in self.owner.parent.listeFaction:          #pour chaque faction dans la liste de faction
                for etoile in faction.listeEtoile:                  #pour chaque etoile dans la liste d'etoile contenue dans chaque faction
                    if( posX==etoile.posX and posY==etoile.posY):   #si la position de l'etoile courante est egale a la position d'une autre etoile
                        break       #fait sortir du 2e "for", qui nous ammene au second break
                else:               #si la 2e boucle finis sans heurt
                    continue        #retourne et continue l'iteration dans le 1er "for"
                break               #fait sortir du 1er "for", qui nous ammÃƒÂ¨ne au "while" au dessus
            else:                   #si les deux boucles ont finis sans rencontrer une seule fois une etoile a la meme position que l'etoile courante
                self.posX = posX    #attribution de la position en x
                self.posY = posY    #attribution de la position en y
                return              #quitte la fonction








#######################################################
class Flotte:
    def __init__(self,owner,nbVaisseaux,etoileDepart,etoileDestination):
        self.owner = owner
        self.nbVaisseaux = nbVaisseaux
        self.travelTime = 0
        self.depart = etoileDepart
        self.destination = etoileDestination
        self.flagBataille = None

    def mergeFlotte(self,laFlotteAnnexe):
        self.nbVaisseaux += laFlotteAnnexe.nbVaisseaux

    def calcTravelTime(self):
        distance = math.sqrt((self.depart.posX-self.destination.posX)**2+(self.depart.posY-self.destination.posY)**2)
        if(distance <= 2):
            self.travelTime = distance/2
        else:
            self.travelTime = 1+((distance-2)/3)

    def estRendu(self):
        if(self.travelTime <= 0):
            return True
        else:
            return False

    def updateTravelTime(self):
        self.travelTime -= 0.1

    def setDestination(self,etoile):
        self.destination = etoile

    def bataille(self):
        if(isinstance(self.owner,Humain)):
            self.destination.updateSpyRank()
        tourDefence = True
        if(self.destination.flotteStationnaire.nbVaisseaux > self.nbVaisseaux):
            print("Possibilite d'attaque surprise...")
            if(self.attaqueSurprise(self.destination.flotteStationnaire.nbVaisseaux)):
                tourDefence = False
                print("Ahaha! Attaque surprise!!!")
        while(self.destination.flotteStationnaire.nbVaisseaux > 0 and self.nbVaisseaux > 0):
            if(random.randint(0,10) > 6):
                turnValue = -1
            else:
                turnValue = 0
            if(tourDefence):
                self.nbVaisseaux += turnValue
                tourDefence = False
            else:
                self.destination.flotteStationnaire.nbVaisseaux += turnValue
                tourDefence = True
        else:
            if(self.destination.flotteStationnaire.nbVaisseaux == 0):
                self.flagBataille = True
            else:
                self.flagBataille = False



    def attaqueSurprise(self,nbVaisseauDefence):
        ratio = nbVaisseauDefence/self.nbVaisseaux
        if(ratio < 5):
            P = ratio / 10
        elif(ratio < 20):
            P = (3 * ratio + 35) /100
        else:
            P = 0.95

        if(random.randint(1,100) < P*100):
            return True
        else:
            return False


