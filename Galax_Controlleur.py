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
            self.vue.drawJeu(self.jeu.getMergedListeEtoile())
        elif(vueReturnKey == 1):#High scores
            print("pasEncore implementer")
        elif(vueReturnKey == 2):#Quitter"
            self.vue.root.destroy()
        elif(vueReturnKey == 3): #choix du nombres d'etoiles
            self.vue.choixNbrEtoiles()

    def gameLoop(self):
        self.jeu.gestionTroupes()
        for i in range(10):
            print(i)
            self.jeu.moveFlotteEnMouvement()
        self.jeu.ajoutVaisseau()
        self.jeu.anneePassees +=1
        if(self.jeu.listeFaction[0].isDead()):
            self.vue.drawFinPartie(False)
        if(self.jeu.listeFaction[1].isDead() and self.jeu.listeFaction[1].isDead()):
            self.vue.drawFinPartie(True)
            return self.vue.drawMainMenu()
        if(self.jeu.listeFaction[1].isDead()):
            self.vue.setFactionVaincue(True)
        if(self.jeu.listeFaction[1].isDead()):
            self.vue.setFactionVaincue(False)
        self.vue.drawJeu(self.jeu.getMergedListeEtoile())

    def launchPress(self,etoileDepart,etoileDestination,force):
        if(self.isHumanMovePossible(etoileDepart)):
            self.jeu.lancerFlotteHumain(etoileDepart,etoileDestination,force)

    def isHumanMovePossible(self,etoileDepart):
        if(etoileDepart and isinstance(etoileDepart.owner,Galax_Modele.Humain)):
            return True
        return False

    def setJeu(self,nbEtoile = 50):
        if(not self.jeu):#si la partie n'existe pas
            self.jeu = Galax_Modele.Jeu(nbEtoile)

            

if __name__ == '__main__':
    c=Controlleur()