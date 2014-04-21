from tkinter import *
import time

class Vue:
    def __init__(self,controlleur):
        self.controlleur = controlleur
        self.factionVaincue=''
        self.listeEtoile=[]
        
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
        #--------------------------------------------------------
        self.canvas=Canvas(self.root, width=self.screenWidth, height=self.screenHeight, bg='black')  
              
        #self.canvas.bind('<Configure>', self.resize)
        self.canvas.bind('<Button-1>', self.click)
    
        self.canvas.pack()
    
        #image de background
        self.background = PhotoImage(file="cosmosBG.gif")
        #self.canvas.create_image(0,0,anchor=NW,image=self.background)
        
        self.drawMainMenu()
        
    def click(self,event):
        eventX = event.x
        eventY = event.y
        print ('x:'+str(eventX)+' y:'+str(eventY))
        if(eventX >= self.buttonPosX and eventX <= self.buttonPosX+self.buttonWidth):
            if(eventY >= self.buttonPosY1 and eventY <= self.buttonPosY1+self.buttonHeight):
                print("button1")
            elif(eventY >= self.buttonPosY2 and eventY <= self.buttonPosY2+self.buttonHeight):
                print("button2")
            elif(eventY >= self.buttonPosY3 and eventY <= self.buttonPosY3+self.buttonHeight):
                print("button3")
        
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
        self.listeEtoile = listeEtoile
        
    def drawJeu(self):
        self.drawEtoiles(self.listeEtoile)
        self.drawBottomMenu()
        self.drawSideMenu()
        
    def drawSideMenu(self):
        self.canvas.delete("menuBar")
        self.canvas.create_rectangle(self.screenWidth-256,0,
                                     self.screenWidth,self.screenHeight-128,
                                     fill='gray',tags="menuBar")
        
    def drawBottomMenu(self):
        self.canvas.delete("menuBar")
        self.canvas.create_rectangle(0,self.screenHeight-128,
                                     self.screenWidth,self.screenHeight,
                                     fill='gray',tags="menuBar")

    def drawEtoiles(self):
        for e in self.listeEtoiles:
            posX = int((e.posX*self.width-100)/100)
            posY = int((e.posY*self.height-100)/100)
            self.canvas.create_oval(posX,posY,posX+32,posY+32,fill='green',tags='etoiles')
            
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