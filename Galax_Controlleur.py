import Galax_Modele
import Galax_Vue

class Controlleur:
    def __init__(self):
        self.jeu = None
        self.vue = Galax_Vue.Vue(self)
        self.vue.root.mainloop()

    def menuLoop(self, vueReturnKey):
        if(vueReturnKey == 0):#NewGame
            self.setJeu()
            self.vue.etatVue = 1
            self.vue.drawJeu(self.jeu.getMergedListeEtoile())
        elif(vueReturnKey == 1):#High scores
            print("pasEncore implementer")
        elif(vueReturnKey == 2):#Quitter
            self.vue.root.destroy()
        elif(vueReturnKey == 3): #choix du nombres d'etoiles
            self.vue.choixNbrEtoiles()

    def gameLoop(self):
        print("********** Movement IA ****************************")
        self.jeu.gestionTroupes()
        print("********** Gestion de l'annee "+str(self.jeu.anneePassees)+" ******************")
        for i in range(10):
            print("********** "+str(i)+"/10 ***********************************")
            self.jeu.moveFlotteEnMouvement()
        self.jeu.ajoutVaisseau()
        self.jeu.anneePassees +=1
        
        if(self.checkEndGame()):
            return
        self.vue.listeEtoiles = self.jeu.getMergedListeEtoile()
        self.checkSiToutesLesEtoilesSelectionneesSontEncoreA_Moi()
        
        print("********** Mouvement du joueur ********************")
        self.vue.drawJeu(self.jeu.getMergedListeEtoile())

    def launchPress(self,listeEtoileDepart,etoileDestination,force):
        if(len(listeEtoileDepart)==1):
            self.jeu.lancerFlotteHumain(listeEtoileDepart[0], etoileDestination, force)
        else:
            for etoileDepart in listeEtoileDepart:
                self.jeu.lancerFlotteHumain(etoileDepart, etoileDestination, etoileDepart.flotteStationnaire.nbVaisseaux)

    def isHumanMovePossible(self,etoileDepart):
        if(etoileDepart and self.isStillHumain(etoileDepart)):
            return True
        return False

    def isStillHumain(self,etoile):
        if(isinstance(etoile.owner,Galax_Modele.Humain)):
            return True
        return False

    def setJeu(self,nbEtoile = 40):
        if(not self.jeu):#si la partie n'existe pas
            self.jeu = Galax_Modele.Jeu(nbEtoile)

    def checkEndGame(self):
        while True:
            unMort = self.jeu.getSomeDead()

            if(unMort):
                message = "Les " + str(unMort.nom) + " sont vaincus"
                self.vue.splashMessage(message, 2)
                self.jeu.listeFaction.remove(unMort)

                if(unMort.nom == "Humain"):
                    self.vue.splashMessage("Vous avez perdu!", 5)
                    self.vue.drawMainMenu()
                    self.vue.etatVue = 0
                    self.jeu = None
                    return True
                elif(len(self.jeu.listeFaction) == 1):
                    self.vue.splashMessage("Vous avez gagnez!", 5)
                    self.vue.drawMainMenu()
                    self.vue.etatVue = 0
                    self.jeu = None
                    return True

            else:
                return None
            

    def checkSiToutesLesEtoilesSelectionneesSontEncoreA_Moi(self):
        for etoile in self.vue.etoileOrigin:
            if(self.isStillHumain(etoile)):
                pass #good, cette etoile t'appartient encore!
            else: #ohoh...
                self.vue.etoileOrigin.remove(etoile)
            if(len(self.vue.etoileOrigin) == 0):
                self.vue.etoileOrigin = None

            

if __name__ == '__main__':
    c=Controlleur()