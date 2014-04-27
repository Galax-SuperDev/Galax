from tkinter import *
from tkinter_png import *
import random
import time

class Vue:
    def __init__(self,controlleur):
        self.compteurEtoile = 0
        self.controlleur = controlleur
        self.derniereEtoileClick = None
        self.listeEtoiles = []
        self.listeIndexSkinEtoile = []
        self.etatVue = 0
        self.etoileOrigin = []#liste d'etoile d'origine pour pourvoir en sélectionner plusieur a la fois
        self.etoileDestination = None
        self.root=Tk()
        self.root.title('Galax')
        self.root.iconbitmap(default='galaxIcon.ico')
              
        # taille de l'ecran--------------------------------------
        self.screenWidth = 1280
        self.screenHeight = 768
        
        # taille du canva----------------------------------------
        self.width = 1024
        self.height = 640
        
        # taille des bouttons du menus---------------------------
        self.buttonWidth = 200
        self.buttonHeight = 64
        
        self.buttonPosX = 0
        self.buttonPosY1 = 0
        self.buttonPosY2 = 0
        self.buttonPosY3 = 0
        
        self.slider = None
        self.b_launchDansCanvas = None


        self.canvas=Canvas(self.root, width=self.screenWidth, height=self.screenHeight, bg='black')  
              
        #self.canvas.bind('<Configure>', self.resize)
        self.canvas.bind('<Button-1>', self.leftClick)
        self.canvas.bind('<Button-3>', self.rightClick)
        self.canvas.pack()
    ###########################################################
        #image :
        self.background = PhotoImage(file="background.gif")
        self.sideBarLeftImg = PhotoImage(file="sidebarLeft.gif")
        self.sideBarImg = PhotoImage(file="sidebarbot.gif")
        self.endTurnImg = PhotoImage(file="endTurnButton.gif")
        
        self.imagesPlanete = []
        for i in range(0,8):
            self.imagesPlanete.append(PngImageTk("planete"+str(i)+".png"))
            self.imagesPlanete[i].convert()

        self.imagesOmbre = []
        for i in range(3):
            self.imagesOmbre.append(PngImageTk("ombre"+str(i)+".png"))
            self.imagesOmbre[i].convert()
            
        self.imageCursor = PngImageTk("cursor.png")
        self.imageCursor.convert()
        
        self.imageCursorDestination = PngImageTk("cursor_1.png")
        self.imageCursorDestination.convert()
    ###########################################################    
        self.drawMainMenu()
        
    def normPosX(self,position):
        return position*32
        """pos = int((position*self.width)/32)+32
        return pos"""
    
    def normPosY(self,position):
        return position*32
        """pos = int((position*self.height)/20)+32
        return pos"""
    
    def choixNbrEtoiles(self):
        inputNbrEtoile = Scale(self.root,from_=20, to=80,orient=HORIZONTAL)
        inputNbrEtoile_dansCanevas = self.canvas.create_window(self.screenWidth/2,600,
                                                     window=inputNbrEtoile,tags='nbEtoile')
        def sendReponse():
            self.controlleur.setJeu(inputNbrEtoile.get())
            self.canvas.delete('nbEtoile')
        b = Button(self.root, text="Choisir", width=10, command=sendReponse)
        b_dansCanevas = self.canvas.create_window((self.screenWidth/2),650,
                                                     window=b,tags='nbEtoile')


    def leftClick(self,event):
        eventX = event.x
        eventY = event.y
        print ('x:'+str(eventX)+' y:'+str(eventY),end=' ')
        
        # permet de savoir si la partie de jeu est debutee 0 
        if(self.etatVue == 0):
            if(eventX >= self.buttonPosX and eventX <= self.buttonPosX+self.buttonWidth):
                if(eventY >= self.buttonPosY1 and eventY <= self.buttonPosY1+self.buttonHeight):
                    self.controlleur.menuLoop(0)
                elif(eventY >= self.buttonPosY2 and eventY <= self.buttonPosY2+self.buttonHeight):
                    self.controlleur.menuLoop(1)
                elif(eventY >= self.buttonPosY3 and eventY <= self.buttonPosY3+self.buttonHeight):
                    self.controlleur.menuLoop(2)
                elif(eventY >= self.buttonPosY4 and eventY <= self.buttonPosY4+self.buttonHeight):
                    self.controlleur.menuLoop(3)
        elif(self.etatVue == 1):
            self.initSurfaceDessin()
            for e in self.listeEtoiles:
                posX = self.normPosX(e.posX)
                posY = self.normPosY(e.posY)
                if(eventX >= posX and eventX <= posX+32):
                    if(eventY >= posY and eventY <= posY+32):#si click sur etoile
                        self.derniereEtoileClick = e
                        if(e.owner.nom == "Humain"):    #si humain
                            if(not self.etoileOrigin.count(e)): #si l'etoile en question n'est pas deja selectionne
                                self.etoileOrigin.append(e)
                                self.etoileDestination = None
                                self.canvas.delete('menu')
                                self.drawInfosEtoileOrigin(self.derniereEtoileClick)
                                self.drawSurfaceDeJeu()  
                                if(len(self.etoileOrigin) == 1):
                                    self.dessineSliderFlottes()
                                break
                        else:
                            self.etoileOrigin[:] = []  
                            self.etoileDestination = e
                            self.canvas.delete('menu')
                            self.drawInfosEtoileDestination(self.derniereEtoileClick)
                            self.drawSurfaceDeJeu()
                                 
            else:
                self.etoileOrigin[:] = []#sinon vide la selection
                

    def rightClick(self,event):
        eventX = event.x
        eventY = event.y
        
        for e in self.listeEtoiles:
        
            posX = self.normPosX(e.posX)
            posY = self.normPosY(e.posY)
            
            if(eventX >= posX and eventX <= posX+32):
                if(eventY >= posY and eventY <= posY+32):
                    
                    self.etoileDestination = e
                    if(self.etoileOrigin):
                        self.boutonLaunchMAX()
                        if(len(self.etoileOrigin) == 1):
                            self.boutonLaunch()
                            
                    
                    if(self.controlleur.isHumanMovePossible(self.etoileOrigin[0])):
                        oriX = self.normPosX(self.etoileOrigin[0].posX)+16
                        oriY = self.normPosY(self.etoileOrigin[0].posY)+16
                        
                        destX = self.normPosX(self.etoileDestination.posX)+16
                        destY = self.normPosY(self.etoileDestination.posY)+16
                        
                        cursorX = posX+16
                        cursorY = posY+16
                        
                        
                        self.canvas.delete('cursorDest')
                        self.canvas.create_image(cursorX, cursorY, 
                                                 image=self.imageCursorDestination.image, 
                                                 anchor=CENTER,tags='cursorDest')

                        self.canvas.delete('trajet')
                        self.canvas.create_line(oriX,oriY,
                                                destX,destY,fill='white',tags='trajet')
                        
                        self.canvas.delete('menu')
                        
                        self.canvas.create_text(self.screenWidth-220,57,anchor=NW,
                                                text="nom de l'etoile",fill='white',
                                                font=('consolas','12'),
                                                tags='menu')
                        self.canvas.delete('menu')
                        self.drawInfosEtoileOrigin(self.derniereEtoileClick)
                        self.drawInfosEtoileDestination(self.etoileDestination)

                        
    '''
    def resize(self,event):
        self.screenWidth = event.width
        self.screenHeight = event.height
        self.width = self.screenWidth-256;
        self.height = self.screenHeight-128;
        
        self.drawMenu()
    '''
    def effacerFrame(self):

        listeWidgets = self.root.winfo_children()

        for i in listeWidgets:
            i.pack_forget()
            i.place_forget()
#----------------------------------------------------------------------------------------
#---------------------   JEU  -----------------------------------------------------------  
#----------------------------------------------------------------------------------------
        
    def splashMessage(self,message):
        splashBox = Text(width=self.root.winfo_width(), bg='black', fg='white', font=('Arial', 40),tags='splashBox')
        splashBox.delete(1.0, END)
        splashBox.place(height=100, x=0, y=self.root.winfo_height()/2)
        splashBox.insert(INSERT,message)
        self.root.update()
        time.sleep(1)
        self.root.delete('splashBox')

        
    def drawJeu(self,listeEtoiles):
        self.listeEtoiles = listeEtoiles
        self.canvas.delete('all')
        self.drawSurfaceDeJeu()
        self.drawBottomMenu()
        self.drawSideMenu()
        
    def drawSideMenu(self):
        self.canvas.create_image(self.screenWidth-256,0,image=self.sideBarLeftImg,anchor=NW,tags='menuBar')

        
    def drawBottomMenu(self):
        self.canvas.create_image(0,self.screenHeight-128,image=self.sideBarImg,anchor=NW)#sidebarImage
        self.canvas.create_image(self.screenWidth-256,self.screenHeight-128,image=self.endTurnImg,anchor=NW,tags='endTurnButton')# dessin du boutton de fin de tour
        self.boutonFinDeTour()


    def initSurfaceDessin(self):
        self.etoileDestination = None
        self.canvas.delete('cursorDest')
        self.canvas.delete('trajet')
        self.canvas.delete('cursor')
        if(self.b_launchDansCanvas):
            self.canvas.delete('slider')
            self.canvas.delete('launcher')

    def resetSlider(self):
        self.canvas.delete('slider')
        self.dessineSliderFlottes()

    
    def actionBoutonLaunch(self,maximum):
        if(maximum):
            self.controlleur.launchPress(self.etoileOrigin,self.etoileDestination,self.etoileOrigin[0].flotteStationnaire.nbVaisseaux)
        else:
            self.controlleur.launchPress(self.etoileOrigin,self.etoileDestination,self.slider.get())
        if(len(self.etoileOrigin) == 1):
            self.resetSlider()

    def boutonLaunch(self):
        if(self.etoileOrigin):
            if(self.controlleur.isHumanMovePossible(self.etoileOrigin[0]) and self.etoileDestination):
                boutonLaunch = Button(self.root,text="LAUNCH!", command= lambda: self.actionBoutonLaunch(False))
                self.b_launchDansCanvas = self.canvas.create_window(650,680,window=boutonLaunch,tags='launcher')

    def boutonLaunchMAX(self):
        if(self.etoileOrigin):
            if(self.controlleur.isHumanMovePossible(self.etoileOrigin[0]) and self.etoileDestination):
                boutonLaunchMax = Button(self.root,text="Launch MAX", command= lambda: self.actionBoutonLaunch(True))
                self.b_launchDansCanvas = self.canvas.create_window(650,715,window=boutonLaunchMax,tags='launcher')


    def boutonFinDeTour(self):
        boutonFinTour = Button(self.root,width=20,height=1,text="Fin du tour",command=self.controlleur.gameLoop,bg='black',fg='red')
        self.b_EndTurn = self.canvas.create_window(self.screenWidth-160,self.screenHeight-90,window=boutonFinTour)


        #-------------------------------------------------------------------------------
        

        # dessin du slider de gestion des flottes --------------------------------------
    def dessineSliderFlottes(self): 
        if(self.etoileOrigin):
            if(self.controlleur.isHumanMovePossible(self.etoileOrigin[0])):
                self.slider = Scale(self.root,from_=0,to=int(self.etoileOrigin[0].flotteStationnaire.nbVaisseaux),
                                orient=HORIZONTAL,label="Nombres de vaisseaux a envoyer",
                                bg='gray40',length=300)
            slider_dansCanvas = self.canvas.create_window(200,715,window=self.slider,tags='slider')



    def drawSurfaceDeJeu(self):
        self.canvas.create_image(0,0,image=self.background,anchor=NW)
        if(self.etoileDestination):
            self.drawCurseurDestination()
        if(self.etoileOrigin):
            for etoile in self.etoileOrigin:
                self.drawCurseur(etoile)
        self.drawEtoiles()

    def drawCurseur(self,etoile):
        self.canvas.create_image(self.normPosX(etoile.posX)+16, self.normPosY(etoile.posY)+16, image=self.imageCursor.image, anchor=CENTER,tags='cursor')

    def drawCurseurDestination(self):
        self.canvas.create_image(self.normPosX(self.etoileDestination.posX)+16, self.normPosY(self.etoileDestination.posY)+16, image=self.imageCursorDestination.image, anchor=CENTER,tags='cursor')

    def drawEtoiles(self):
        i = -1
        for e in self.listeEtoiles:
            i+=1
            posX = self.normPosX(e.posX)
            posY = self.normPosY(e.posY)
            if(e.owner.nom == "Czin"):
                self.canvas.create_image(posX-16, posY-16, image=self.imagesOmbre[0].image, anchor=NW,tags=("etoile","surfaceDejeu"))
            if(e.owner.nom == "Gubru"):
                self.canvas.create_image(posX-16, posY-16, image=self.imagesOmbre[1].image, anchor=NW,tags="etoile")
            if(e.owner.nom == "Humain"):
                self.canvas.create_image(posX-16, posY-16, image=self.imagesOmbre[2].image, anchor=NW,tags="etoile")
            if(len(self.listeEtoiles) >= len(self.listeIndexSkinEtoile)):
                self.listeIndexSkinEtoile.append(random.randint(0,7))
            self.canvas.create_image(posX, posY, image=self.imagesPlanete[self.listeIndexSkinEtoile[i]].image, anchor=NW,tags="etoile")


            
    def drawInfosEtoileOrigin(self,etoile):  
             
        self.canvas.create_text(self.screenWidth-220,58,anchor=NW,
                text="Owner:"+str(etoile.owner.nom),fill='white',
                font=('consolas','10'),
                tags='menu')
        
        self.canvas.create_text(self.screenWidth-220,74,anchor=NW,
                text="Nom de l'etoile:",fill='white',
                font=('consolas','10'),
                tags='menu')
        
        self.canvas.create_text(self.screenWidth-220,90,anchor=NW,
                text=etoile.nom,fill='white',
                font=('consolas','10'),
                tags='menu')

        self.canvas.create_text(self.screenWidth-220,106,anchor=NW,
                text="x:"+str(etoile.posX)+" y:"+str(etoile.posY),fill='white',
                font=('consolas','10'),
                tags='menu')
        
        self.canvas.create_text(self.screenWidth-220,122,anchor=NW,
                text="Spy rank:"+str(etoile.spyRank),fill='white',
                font=('consolas','10'),
                tags='menu')

        if(etoile.getNbUsine() == -1):
            texte = "Nombre d'usines: - ? ? ? -"
        else:
            texte = "Nombre d'usines:"+str(etoile.getNbUsine())
        self.canvas.create_text(self.screenWidth-220,138,anchor=NW,
                text=texte,fill='white',
                font=('consolas','10'),
                tags='menu')

        if(etoile.getNbVaisseau() == -1):
            texte = "Nb Vaisseaux: - ? ? ? -"
        else:
            texte = "Vaisseaux:"+str(etoile.getNbVaisseau())
        self.canvas.create_text(self.screenWidth-220,154,anchor=NW,
                text=texte,fill='white',
                font=('consolas','10'),
                tags='menu')
        
    def drawInfosEtoileDestination(self,etoile): 
             
        self.canvas.create_text(self.screenWidth-220,202,anchor=NW,
                text="Owner:"+str(etoile.owner.nom),fill='white',
                font=('consolas','10'),
                tags='menu')
        
        self.canvas.create_text(self.screenWidth-220,218,anchor=NW,
                text="Nom de l'etoile:",fill='white',
                font=('consolas','10'),
                tags='menu')
        
        self.canvas.create_text(self.screenWidth-220,234,anchor=NW,
                text=etoile.nom,fill='white',
                font=('consolas','10'),
                tags='menu')

        self.canvas.create_text(self.screenWidth-220,250,anchor=NW,
                text="x:"+str(etoile.posX)+" y:"+str(etoile.posY),fill='white',
                font=('consolas','10'),
                tags='menu')
        
        self.canvas.create_text(self.screenWidth-220,266,anchor=NW,
                text="Spy rank:"+str(etoile.spyRank),fill='white',
                font=('consolas','10'),
                tags='menu')

        if(etoile.getNbUsine() == -1):
            texte = "Nombre d'usines: - ? ? ? -"
        else:
            texte = "Nombre d'usines:"+str(etoile.getNbUsine())
        self.canvas.create_text(self.screenWidth-220,282,anchor=NW,
                text=texte,fill='white',
                font=('consolas','10'),
                tags='menu')
        
        if(etoile.getNbVaisseau() == -1):
            texte = "Nb Vaisseaux: - ? ? ? -"
        else:
            texte = "Vaisseaux:"+str(etoile.getNbVaisseau())
        self.canvas.create_text(self.screenWidth-220,298,anchor=NW,
                text=texte,fill='white',
                font=('consolas','10'),
                tags='menu')             
#----------------------------------------------------------------------------------------
#---------------------   JEU  -----------------------------------------------------------  
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
#---------------------   MAIN MENU ------------------------------------------------------  
#----------------------------------------------------------------------------------------
    def drawMainMenu(self):
        
        self.buttonWidth = 200
        self.buttonHeight = 64
        
        self.buttonPosX = (self.screenWidth/2)-self.buttonWidth/2
        
        self.buttonPosY1 = self.screenHeight/3 
        self.buttonPosY2 = self.screenHeight/3 + self.buttonHeight + 2
        self.buttonPosY3 = self.screenHeight/3 + (self.buttonHeight*2) + 4
        self.buttonPosY4 = self.screenHeight/3 + (self.buttonHeight*3) + 6
        
        self.canvas.delete("menu")
        
        self.canvas.create_rectangle(self.buttonPosX, self.buttonPosY1,
                                     self.buttonPosX+self.buttonWidth, self.buttonPosY1+self.buttonHeight, 
                                     fill='gray', activefill='white', tags='menu')
        
        self.canvas.create_rectangle(self.buttonPosX, self.buttonPosY2,
                                     self.buttonPosX+self.buttonWidth, self.buttonPosY1+(self.buttonHeight*2)+2, 
                                     fill='gray', activefill='white', tags='menu')
        
        self.canvas.create_rectangle(self.buttonPosX, self.buttonPosY3,
                                     self.buttonPosX+self.buttonWidth, self.buttonPosY1+(self.buttonHeight*3)+4,
                                     fill='gray',activefill='white',tags='menu')
        
        self.canvas.create_rectangle(self.buttonPosX,self.buttonPosY4,
                                     self.buttonPosX+self.buttonWidth,self.buttonPosY1+(self.buttonHeight*4)+6,
                                     fill='gray',activefill='white',tags='menu')

        self.canvas.create_text(self.buttonPosX+100,self.buttonPosY1+32,
                                text='New game',fill='black',activefill='white',
                                font=('consolas','16'),
                                tags='menu')
        self.canvas.create_text(self.buttonPosX+100,self.buttonPosY1+96,
                                text='High scores',
                                fill='black',activefill='white',
                                font=('consolas','16'),
                                tags='menu')
        self.canvas.create_text(self.buttonPosX+100,self.buttonPosY1+160,
                                text='Quit game',
                                fill='black',activefill='white',
                                font=('consolas','16'),
                                tags='menu')
        self.canvas.create_text(self.buttonPosX+100,self.buttonPosY1+226,
                                text='choix # Etoiles',
                                fill='black',activefill='white',
                                font=('consolas','14'),
                                tags='menu')

#----------------------------------------------------------------------------------------
#---------------------   MAIN MENU ------------------------------------------------------  
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
#---------------------   END GAME ------------------------------------------------------- 
#----------------------------------------------------------------------------------------
    # bool 1 = win 0 = lose
    def drawFinPartie(self,etatFinale):
        self.canvas.delete('all')
        
        if(etatFinale == 0):
            self.canvas.create_text(100,100,text='vous avez perdu la partie')
        elif(etatFinale == 1):
            self.canvas.create_text(100,100,text='vous avez gagne la partie')
        time.sleep(5)
        
#----------------------------------------------------------------------------------------
#---------------------   END GAME ------------------------------------------------------- 
#----------------------------------------------------------------------------------------