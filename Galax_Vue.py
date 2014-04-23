from tkinter import *
from tkinter_png import *
import random
import time

class Vue:
    def __init__(self,controlleur):
        self.compteurEtoile = 0
        self.controlleur = controlleur
        self.factionVaincue=''
        self.listeEtoiles=[]
        self.nbrEtoiles = 0
        self.etatVue = 0

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
        
        self.etoileOrigin = None
        self.etoileDestination = None
        #--------------------------------------------------------
        self.clickOnSlider = 0
        #--------------------------------------------------------
        self.canvas=Canvas(self.root, width=self.screenWidth, height=self.screenHeight, bg='black')  
              
        #self.canvas.bind('<Configure>', self.resize)
        self.canvas.bind('<Button-1>', self.leftClick)
        self.canvas.bind('<Button-3>', self.rightClick)
        self.canvas.bind('<B1-Motion>', self.mouseDragged)
    
        self.canvas.pack()
    
        #image de background
        self.background = PhotoImage(file="background.gif")
        self.sideBarLeftImg = PhotoImage(file="sidebarLeft.gif")
        self.sideBarImg = PhotoImage(file="sidebarbot.gif")
        self.endTurnImg = PhotoImage(file="endTurnButton.gif")
        
        self.imagesPlanete = []
        
        '''
        self.planete = PngImageTk("planete0.png")
        self.planete.convert()
        '''
        
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
        
        #self.canvas.create_image(0,0,anchor=NW,image=self.background)
        
        self.drawMainMenu()
        
    def normPosX(self,position): #fuckage ici!
        pos = int((position*self.width)/32)+32
        return pos
    
    def normPosY(self,position):
        pos = int((position*self.height)/20)+32
        return pos
    
    def choixNbrEtoiles(self):
        self.nbrEtoiles = 0
        inputNbrEtoile = Scale(self.root,from_=20, to=80,orient=HORIZONTAL)
        inputNbrEtoile.pack()
        def sendReponse():
            self.nbrEtoiles = inputNbrEtoile.get()
            inputNbrEtoile.destroy()
            b.destroy()
        b = Button(self.root, text="Choisir", width=10, command=sendReponse)
        b.pack()

    def getNbrEtoiles(self):
        return self.nbrEtoiles

    
    def leftClick(self,event):
        eventX = event.x
        eventY = event.y
        print ('x:'+str(eventX)+' y:'+str(eventY),end=' ')
        
        # permet de savoir si la partie de jeu est debutee 0 
        if(self.etatVue == 0):
            if(eventX >= self.buttonPosX and eventX <= self.buttonPosX+self.buttonWidth):
                if(eventY >= self.buttonPosY1 and eventY <= self.buttonPosY1+self.buttonHeight):
                    print("button1")
                    self.controlleur.menuLoop(0)
                    self.etatVue = 1
                elif(eventY >= self.buttonPosY2 and eventY <= self.buttonPosY2+self.buttonHeight):
                    print("button2")
                elif(eventY >= self.buttonPosY3 and eventY <= self.buttonPosY3+self.buttonHeight):
                    print("button3")
                elif(eventY >= self.buttonPosY4 and eventY <= self.buttonPosY4+self.buttonHeight):
                    print("combien d'etoiles")
                    self.choixNbrEtoiles()
        elif(self.etatVue == 1):
            for e in self.listeEtoiles:
        
                posX = self.normPosX(e.posX)
                posY = self.normPosY(e.posY)
                
                if(eventX >= posX and eventX <= posX+32):
                    if(eventY >= posY and eventY <= posY+32):
                        
                        print('click sur etoile')
                        
                        self.etoileOrigin = e
                        
                        cursorX = posX+16
                        cursorY = posY+16
                        
                        self.canvas.delete('cursor')
                        self.canvas.delete('cursorDest')
                        self.canvas.delete('trajet')
                        
                        self.canvas.create_image(cursorX, cursorY, image=self.imageCursor.image, anchor=CENTER,tags='cursor')
                        
                        self.canvas.delete('menu')
                        
                        self.canvas.create_text(self.screenWidth-220,57,anchor=NW,
                                                text="nom de l'etoile",fill='white',
                                                font=('consolas','12'),
                                                tags='menu')
                        self.drawNomEtoile(e)
                        
                        self.canvas.create_rectangle(200,self.screenHeight-115,
                                             220,self.screenHeight-15,
                                             fill='gray20',activefill='gray40',
                                             tags='sliderFlotte')
                
                if(eventX >= 200 and eventX <= 220):
                    if(eventY >= self.screenHeight-115 and eventY <= self.screenHeight-15):
                        self.clickOnSlider = 1
                    else:
                        self.clickOnSlider = 0

                        
    def rightClick(self,event):
        eventX = event.x
        eventY = event.y
        
        for e in self.listeEtoiles:
        
            posX = self.normPosX(e.posX)
            posY = self.normPosY(e.posY)
            
            if(eventX >= posX and eventX <= posX+32):
                if(eventY >= posY and eventY <= posY+32):
                    
                    print('click sur etoile')
                    
                    self.etoileDestination = e
                    
                    oriX = self.normPosX(self.etoileOrigin.posX)+16
                    oriY = self.normPosY(self.etoileOrigin.posY)+16
                    
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
                    
                    self.drawNomEtoile(e)
                    
    def mouseDragged(self,event):
        eventX = event.x
        eventY = event.y
        sliderPosX = 200
        if(eventY >= 640):
            if(self.clickOnSlider == 1):
                sliderPosX = eventX
                if(sliderPosX > 580):
                    sliderPosX = 580
                if(sliderPosX < 200):
                    sliderPosX = 200
                self.canvas.delete('sliderFlotte')
                self.canvas.create_rectangle(sliderPosX,self.screenHeight-115,
                                             sliderPosX+20,self.screenHeight-15,
                                             fill='gray20',activefill='gray40',
                                             tags='sliderFlotte')

        
        
        
                        
    '''
    def resize(self,event):
        self.screenWidth = event.width
        self.screenHeight = event.height
        self.width = self.screenWidth-256;
        self.height = self.screenHeight-128;
        
        self.drawMenu()
    '''
#----------------------------------------------------------------------------------------
#---------------------   JEU  -----------------------------------------------------------  
#----------------------------------------------------------------------------------------

    #bool 0 = czin 1= gubru
    def setFactionVaincue(self,factionVaincue):
        self.factionVaincue = factionVaincue
        
    #la liste de toutes les etoiles de la partie
    def setListeEtoile(self,listeEtoile):
        self.listeEtoiles = listeEtoile
        
    def drawJeu(self):
        self.canvas.delete('all')
        self.drawEtoiles()
        self.drawBottomMenu()
        self.drawSideMenu()
        
    def drawSideMenu(self):
        self.canvas.create_image(self.screenWidth-256,0,image=self.sideBarLeftImg,anchor=NW,tags='menuBar')

        
    def drawBottomMenu(self):
        self.canvas.create_image(0,self.screenHeight-128,image=self.sideBarImg,anchor=NW)
        
        # dessin du boutton de fin de tour --------------------------------------------
        self.canvas.create_image(self.screenWidth-256,self.screenHeight-128,image=self.endTurnImg,anchor=NW,tags='endTurnButton')

        self.canvas.create_text(self.screenWidth-200,self.screenHeight-90,anchor=NW,
                                text='Fin du tour',fill='white',
                                font=('consolas','16'),
                                tags='endTurnButton')
        #-------------------------------------------------------------------------------
        
        # dessin du slider de gestion des flottes --------------------------------------
        self.canvas.create_rectangle(200,self.screenHeight-115,
                                     600,self.screenHeight-15,
                                     fill='gray50',
                                     tags='sliderBackground')
        
        self.canvas.create_rectangle(200,self.screenHeight-115,
                             220,self.screenHeight-15,
                             fill='gray20',activefill='gray40',
                             tags='sliderFlotte')
        
        self.canvas.create_rectangle(620,self.screenHeight-113,
                                     660,self.screenHeight-68,fill='gray40',activefill='gray',
                                     tags='addFlotteButton')
        
        self.canvas.create_rectangle(670,self.screenHeight-113,
                                     710,self.screenHeight-68,fill='gray40',activefill='gray',
                                     tags='addFlotteButton')
        
        self.canvas.create_rectangle(620,self.screenHeight-61,
                                     660,self.screenHeight-18,fill='gray40',activefill='gray',
                                     tags='addFlotteButton')
        
        self.canvas.create_rectangle(670,self.screenHeight-61,
                                     710,self.screenHeight-18,fill='gray40',activefill='gray',
                                     tags='addFlotteButton')
        

    def drawEtoiles(self):
        self.canvas.create_image(0,0,image=self.background,anchor=NW)
        for e in self.listeEtoiles:
            posX = self.normPosX(e.posX)
            posY = self.normPosY(e.posY)
            if(e.nom == "Czin"):
                self.canvas.create_image(posX-16, posY-16, image=self.imagesOmbre[0].image, anchor=NW,tags="etoile")
            if(e.nom == "Gubru"):
                self.canvas.create_image(posX-16, posY-16, image=self.imagesOmbre[1].image, anchor=NW,tags="etoile")
            if(e.nom == "Humain"):
                self.canvas.create_image(posX-16, posY-16, image=self.imagesOmbre[2].image, anchor=NW,tags="etoile")

            self.canvas.create_image(posX, posY, image=self.imagesPlanete[random.randint(0,7)].image, anchor=NW,tags="etoile")
            self.compteurEtoile += 1
        print(self.compteurEtoile)


            
    def drawNomEtoile(self,etoile):
        self.canvas.create_text(self.screenWidth-220,74,anchor=NW,
                        text=etoile.nom,fill='white',
                        font=('consolas','12'),
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
                                font=('consolas','16'),
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