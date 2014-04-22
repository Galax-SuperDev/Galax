from tkinter import *
from tkinter_png import *
import random
import time

class Vue:
    def __init__(self,controlleur):
        self.controlleur = controlleur
        self.factionVaincue=''
        self.listeEtoiles=[]
        
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
        self.canvas=Canvas(self.root, width=self.screenWidth, height=self.screenHeight, bg='black')  
              
        #self.canvas.bind('<Configure>', self.resize)
        self.canvas.bind('<Button-1>', self.leftClick)
        self.canvas.bind('<Button-3>',self.rightClick)
    
        self.canvas.pack()
    
        #image de background
        self.background = PhotoImage(file="cosmosBG.gif")
        
        
        self.imagesPlanete = []
        
        '''
        self.planete = PngImageTk("planete0.png")
        self.planete.convert()
        '''
        
        for i in range(0,8):
            self.imagesPlanete.append(PngImageTk("planete"+str(i)+".png"))
            self.imagesPlanete[i].convert()
        
        self.imageCursor = PngImageTk("cursor.png")
        self.imageCursor.convert()
        
        self.imageCursorDestination = PngImageTk("cursor_1.png")
        self.imageCursorDestination.convert()
        
        #self.canvas.create_image(0,0,anchor=NW,image=self.background)
        
        self.drawMainMenu()
        
    def normPosX(self,position):
        pos = int((position*self.width)/32)+32
        return pos
    
    def normPosY(self,position):
        pos = int((position*self.height)/20)+32
        return pos
    
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
                        self.canvas.create_text(self.screenWidth-220,25,anchor=NW,
                                                text=e.nom,fill='black',
                                                font=('consolas','12'),
                                                tags='menu')
                        
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
                    self.canvas.create_text(self.screenWidth-220,25,anchor=NW,
                                            text=e.nom,fill='black',
                                            font=('consolas','12'),
                                            tags='menu')
                    
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
        self.canvas.create_rectangle(self.screenWidth-256,0,
                                     self.screenWidth,self.screenHeight-128,
                                     fill='gray',tags="menuBar")
        

        
    def drawBottomMenu(self):
        self.canvas.create_rectangle(0,self.screenHeight-128,
                                     self.screenWidth,self.screenHeight,
                                     fill='gray',tags="menuBar")
        
        # dessin du boutton de fin de tour --------------------------------------------
        self.canvas.create_rectangle(self.screenWidth-241,self.screenHeight-115,
                                     self.screenWidth-15,self.screenHeight-15,
                                     fill='gray50',activefill='gray40',
                                     tags='endTurnButton')
        
        self.canvas.create_text(self.screenWidth-200,self.screenHeight-80,anchor=NW,
                                text='Fin du tour',fill='black',
                                font=('consolas','16'),
                                tags='finTour')
        
        self.canvas.create_rectangle(200,self.screenHeight-115,
                                     600,self.screenHeight-15,
                                     fill='gray50',activefill='gray40',
                                     tags='endTurnButton')
        #-------------------------------------------------------------------------------

    def drawEtoiles(self):
        self.canvas.create_image(0,0,image=self.background,anchor=NW)
        for e in self.listeEtoiles:
            posX = self.normPosX(e.posX)
            posY = self.normPosY(e.posY)
            self.canvas.create_image(posX, posY, image=self.imagesPlanete[random.randint(0,7)].image, anchor=NW,tags="etoile")
        

            
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