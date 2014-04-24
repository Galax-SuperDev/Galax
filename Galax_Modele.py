import random
import math



#######################################################
class Jeu:
    def __init__(self,nbEtoilesTotales=50):
        nbEtoileNeutre = nbEtoilesTotales #Ceci est hardcoder mais on pourait le passer au constructeur a partir du menu principal
        print("Le nombre d'etoile est set a la 9eme ligne du modele a " + str(nbEtoileNeutre))
        self.compteurEtoile = 0
        self.listeFaction = []
        self.listeFaction.append(Humain(self))
        self.listeFaction.append(Gubru(self))
        self.listeFaction.append(Czin(self))
        self.listeFaction.append(Neutral(nbEtoileNeutre,self))
        self.anneePassees = 0
        print(self.compteurEtoile)


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
        self.listeFaction[1].reorganisationDesFlottes() # Gubru
        self.listeFaction[2].reorganisationDesFlottes() #Czin

    def moveFlotteEnMouvement(self):
        aSupprimer = []
        for faction in self.listeFaction:
            for flotte in faction.listeFlotteEnMouvement:
                if(flotte.estRendu()):
                    print("Une flotte de:"+str(flotte.nbVaisseaux)+" appartenant au:"+str(flotte.owner.nom)+" est arrive sur:"+str(flotte.destination.nom))
                    if(flotte.owner.nom == flotte.destination.owner.nom):#si c'est la meme faction
                        flotte.destination.flotteStationnaire.mergeFlotte(flotte)
                        print("Flotte:"+str(flotte.nbVaisseaux)+" merge avec la flotte de l'etoile:"+str(flotte.destination.nom))
                    else:                                                 #Sinon, c'est la bataille!
                        gagnant = flotte.bataille()
                        if(gagnant.nom == faction.nom):                    #si c'est l'attaquant qui a gagne la bataille
                            print("Les:"+str(gagnant.nom)+" on capturer:"+str(flotte.destination.nom)+" aux mains des:"+str(flotte.destination.owner.nom))
                            flotte.destination.flotteStationnaire = Flotte(gagnant,flotte.nbVaisseaux,None)
                            gagnant.changeEtoileOwner(flotte.destination.owner,flotte.destination)
                        else:                                               #si les defenseurs ont gagne la bataille
                            print("Les:"+str(flotte.destination.owner.nom)+" on defendu la planete:"+str(flotte.destination.owner.nom))
                            pass
                        aSupprimer.append(Flotte)
                else:
                    flotte.updateTravelTime()
        if(aSupprimer):
            self.supprimeurDeListe(aSupprimer)

    def supprimeurDeListe(self,uneListeSupprimable):
        for itemSupprimable in uneListeSupprimable:
            del itemSupprimable

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
        self.tempsGrappe = None

        self.distanceGrappe = 4
        self.distance_rassemblement = 6
        self.force_attaque_basique = 20
        self.nbr_vaisseaux_par_attaque = 4

        self.mode_rassemblement_forces = 0
        self.mode_etablir_base = 1
        self.mode_conquerir_grappe = 2
        self.mode = self.mode_rassemblement_forces

    def getForceAttaque(self):
        return self.parent.anneePassees * self.nbr_vaisseaux_par_attaque * self.force_attaque_basique

    def reorganisationDesFlottes(self):
        if(self.mode == self.mode_etablir_base):
            if(self.flotteArrive()):
                if(self.etoileBaseProspective.owner.nom == self.nom):#si la baseProspective est en possession des Czins
                    self.etoileBase = self.etoileBaseProspective
                    self.conquerirGrappe()
                    self.mode = self.mode_conquerir_grappe
                else:                                       #sinon, Ã§a veux dire que les defenceurs ont gagne.
                    self.mode = self.mode_rassemblement_forces
                    self.etoileBase = self.listeEtoile[0]   #on remet l_etoile mere comme base

        if(self.mode == self.mode_conquerir_grappe):
            if(self.listeFlotteEnMouvement[len(self.listeFlotteEnMouvement)-1].estRendu()):
                self.mode = self.mode_rassemblement_forces

        if(self.mode == self.mode_rassemblement_forces):
            if(3*self.getForceAttaque() <= self.etoileBase.flotteStationnaire.nbVaisseaux):
                self.mode = self.mode_etablir_base
                self.etoileBaseProspective = self.choisirBase()
                self.etoileBase.envoyerNouvelleFlotte(self.etoileBase.flotteStationnaire.nbVaisseaux,self.etoileBaseProspective)
            else:
                self.rassemblementForces()

    def flotteArrive(self):
        if(self.listeFlotteEnMouvement[0].estRendu()):
            return True
        else:
            return False

    def rassemblementForces(self): # est-ce la fonction a mettre dans jeu.gestionTroupes?
        for etoile in self.listeEtoile:
            if(self.getDistance(etoile,self.etoileBase) < 6):
                etoile.envoyerNouvelleFlotte(etoile.flotteStationnaire.nbVaisseaux,self.etoileBase)

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

    def conquerirGrappe(self):
        nbEnvoi = self.getForceAttaque()
        listeDeTouteLesEtoile = self.parent.getMergedListeEtoile()
        etoilePlusProche = None
        listeEtoileDejaEnvoi = []

        while(self.etoileBase.flotteStationnaire.nbVaisseaux >= nbEnvoi):
            for etoile in listeDeTouteLesEtoile:
                print(etoile.nom)
                if(not isinstance(etoile.owner,Czin)):
                    if(not etoilePlusProche):
                        etoilePlusProche = etoile
                    else:
                        distance = self.getDistance(etoile,self.etoileBase)
                        distancePlusProche = self.getDistance(etoilePlusProche,self.etoileBase)
                        if(distance < distancePlusProche):
                            for etoileDejaEnvoi in listeEtoileDejaEnvoi:
                                if(etoileDejaEnvoi.nom == etoile.nom):
                                    break
                            else:
                                print(str(etoile.nom)+" est plus proche de la base Czin que:"+etoilePlusProche.nom)
                                etoilePlusProche = etoile

            listeEtoileDejaEnvoi.append(etoilePlusProche)
            self.etoileBase.envoyerNouvelleFlotte(nbEnvoi,etoilePlusProche)

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

    def trouverEtoilePlusPres(self,etoileDeBase):
        self.etoilePlusPres = None
        self.distance = 0
        self.distancePlusPres = 1000
        listeEtoileDejaEnvoi = []

        for faction in self.parent.listeFaction: #pour chaque faction
            if (faction.nom != 'Gubru'): # qui ne sont pas Gubru
                for etoile in faction.listeEtoile: # on regarde a travers toutes les etoiles
                    self.distance = math.sqrt((etoile.posX- self.listeEtoile[0].posX)**2+(etoile.posY- self.listeEtoile[0].posY)**2) #on etabli la distance
                    if(self.distance <= self.distancePlusPres):
                        for etoiles in listeEtoileDejaEnvoi:
                            if(etoiles.nom == self.etoilePlusPres.nom): # regarde la plus proche qui n'est PAS deja une cible
                                print("etoiles deja attaquer")
                                break
                        self.etoilePlusPres = etoile # on a trouver l'etoile la plus pres
                        listeEtoileDejaEnvoi.append(etoile)
                        print("trouver etoile plus proche")
                    else:
                        print("il n'y a plus de cibles potentielles")

        return self.etoilePlusPres

    def formationFlotte(self):
        if (self.parent.anneePassees > 0):
            self.force_attaque = self.parent.anneePassees * (self.nbr_vaisseau_par_attaque + self.force_attaque_basique)
        else:
            self.force_attaque = self.force_attaque_basique * 2

        while(self.listeEtoile[0].flotteStationnaire.nbVaisseaux >= self.force_attaque + self.force_attaque_basique ):
            self.listeEtoile[0].envoyerNouvelleFlotte(self.force_attaque,self.trouverEtoilePlusPres(self.listeEtoile[0]))
########voir les explications dans le commit nomme "Changement majeur dans la gestion des platetes - ajout fn"

    def reorganisationDesFlottes(self): #cela doit etre fait a chaque tour
        for etoile in self.listeEtoile:
            if(etoile.nom != self.listeEtoile[0].nom): # on ne veux pas envoyer de flottes de l'etoile mere vers l'etoile mere
                if (etoile.flotteStationnaire.nbVaisseaux > 25):
                    self.etoile.envoyerNouvelleFlotte(etoile.flotteStationnaire - 15,self.listeEtoile[0])
                else:
                    self.etoile.envoyerNouvelleFlotte(etoile.flotteStationnaire,self.listeEtoile[0])
        self.formationFlotte()



class Neutral(Faction):
    def __init__(self, nbEtoileNeutre, parent):
        Faction.__init__(self, parent)
        self.nbEtoileNeutre = nbEtoileNeutre
        self.nom = 'Neutral'
        self.tabNomPossible = []
        self.setupListes()


    def donnerNomEtoile(self):
        fileHandle = open('listeNomEtoile.txt','r')
        if(not self.tabNomPossible):#si le fichier n'est pas encore parser...
            for ligne in fileHandle.readlines():
                self.tabNomPossible.append(str(ligne).rstrip())
            else:
                fileHandle.close()
        return self.tabNomPossible.pop(random.randint(0,len(self.tabNomPossible)-1))

    def setupListes(self):
        for i in range(self.nbEtoileNeutre):
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
            print(str(self.owner.nom) + " --> Flotte:" + str(nbVaisseaux) + ", Depart:" + str(self.nom) + ", Destination:" + str(etoileDestination.nom))
        else:
            print("flotte nulle")

    def ajoutVaisseau(self):
        self.flotteStationnaire.nbVaisseaux += self.nbUsine*random.randint(1,12)

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
        self.flotteAuDernierPassage = 0
####dans setPosition ajouter un intervalle pour ne pas que les etoiles ce chevauche ( puisqu'elle on un certain rayon)
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
                break               #fait sortir du 1er "for", qui nous ammÃ¨ne au "while" au dessus
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

    def mergeFlotte(self,laFlotteAnnexe):
        self.nbVaisseaux += laFlotteAnnexe.nbVaisseaux

    def calcTravelTime(self):
        distance = math.sqrt((self.destination.posX-self.depart.posX)**2+(self.destination.posY-self.depart.posY)**2)
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
        self.travelTime -= 0.1

    def setDestination(self,etoile):
        self.destination = etoile

    def bataille(self):
        nbVaisseauDefence = self.destination.flotteStationnaire.nbVaisseaux
        tourDefence = True
        if(nbVaisseauDefence > self.nbVaisseaux):
            print("Possibilite d'attaque surprise...")
            if(self.attaqueSurprise(nbVaisseauDefence)):
                tourDefence = False
                print("Ahaha! Attaque surprise!!!")
        while(nbVaisseauDefence > 0 and self.nbVaisseaux > 0):
            if(random.randint(0,10) > 6):
                turnValue = -1
                print("Perte d'un vaisseau pour les",end=' ')
            else:
                turnValue = 0
                print("Aucune perte pour les",end=' ')
            if(tourDefence):
                self.nbVaisseaux += turnValue
                tourDefence = False
                print("attaquant")
            else:
                nbVaisseauDefence += turnValue
                tourDefence = True
                print("defenseur")
        else:
            if(nbVaisseauDefence == 0):
                return self.owner
            else:
                return self.destination.owner



    def attaqueSurprise(self,nbVaisseauDefence):
        print("attaqueSurprise avant ratio")
        ratio = nbVaisseauDefence/self.nbVaisseaux
        print("dans fonct Attaque")
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


