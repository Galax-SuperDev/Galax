import Galax_Modele
import Galax_Vue

class Controlleur:
    def __init__(self):
        self.jeu=Galax_Modele.Jeu(self)
        self.vue=Galax_Vue.Vue(self.jeu.etoiles)
        self.vue.root.mainloop()
		
    def gameLoop(self):
        for i in range(self.tic):
            for faction in jeu.listeFaction:
                for etoile in faction.listeEtoiles:
                    for flotte in etoile.listeFlotte:
                        if(i==0):
                            if(flotte.destination != None and not flotte.travelTime > 0 ): #Verif si il y a une destination, et si le temps de voyage n'est pas deja calculer
                                flotte.calcTravelTime()
                        if(flotte.isMoving):
                            flotte.updateTravelTime()
                        if(travelTime == 0):
                            flotte.isMoving=False
        
if __name__ == '__main__':
    c=Controlleur()