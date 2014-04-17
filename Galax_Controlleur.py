import Galax_Modele
import Galax_Vue

class Controlleur:
    def __init__(self):
        self.debugMod = True#ce mod sera a enlever lorsqu'il sera possible de ne pas passer en parametre dès le init du controleur un self.jeu.getMergedListeEtoile à la vue
        if(self.debugMod):
            self.jeu = Galax_Modele.Jeu()
        else:
            self.jeu
        self.vue = Galax_Vue.Vue(self.jeu.getMergedListeEtoile())
        self.vue.root.mainloop()

    def menuLoop(self, vueReturnKey):
        if(vueReturnKey == 0):#NewGame
            self.jeu = Galax_Modele.Jeu()
            #call de la fonction dans la vue qui va afficher le jeux
        elif(vueReturnKey == 1):#High scores
            pass
        elif(vueReturnKey == 2):#Quitter
            pass

		
    def gameLoop(self):
        self.jeu.updateFlotte()
        
if __name__ == '__main__':
    c=Controlleur()