import Galax_Modele
import Galax_Vue

class Controlleur:
    def __init__(self):
        self.jeu = None
        self.vue = Galax_Vue.Vue(self)
        self.vue.root.mainloop()

    def menuLoop(self, vueReturnKey):
        if(vueReturnKey == 0):#NewGame
            if(self.vue.getNbrEtoiles() == 0):
                self.jeu = Galax_Modele.Jeu()
            else:
                self.jeu = Galax_Modele.Jeu(self.vue.getNbrEtoiles())
            self.vue.setListeEtoile(self.jeu.getMergedListeEtoile())
            self.vue.drawJeu()
        elif(vueReturnKey == 1):#High scores
            pass
        elif(vueReturnKey == 2):#Quitter"
            pass
        elif(vueReturnKey ==3): #choix du nombres d'etoiles
            self.vue.choixNbrEtoiles()

    def gameLoop(self):
        jeu.gestionTroupe()
        for i in range(10):
            self.jeu.moveFlotteEnMouvement()
        self.jeu.ajoutVaisseau()
        self.jeu.anneePassees +=1
        if(jeu.faction[0].isDead()):
            vue.drawFinPartie(False)
        if(jeu.faction[1].isDead() and jeu.faction[1].isDead()):
            vue.drawFinPartie(True)
            vue.drawMainMenu()
        if(jeu.faction[1].isDead()):
            vue.setFactionVaincue(True)
        if(jeu.faction[1].isDead()):
            vue.setFactionVaincue(False)
            

if __name__ == '__main__':
    c=Controlleur()