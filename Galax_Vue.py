from tkinter import *

class Vue:
    def __init__(self,listeEtoile):
        self.listeEtoiles = listeEtoile
        self.root=Tk()
              
        self.root.title('Galax')
        self.root.iconbitmap(default='galaxIcon.ico')
              
        self.screenWidth = 1280
        self.screenHeight = 768
        self.width = 1024
        self.height = 640
        self.canvas=Canvas(self.root, width=self.screenWidth, height=self.screenHeight, bg='black')  
              
        self.canvas.bind('<Configure>', self.resize)
        self.canvas.bind('<Button-1>', self.click)
    
        self.canvas.pack(expand=True, fill=BOTH)
        
        self.drawMenu()
        '''
        self.canvas.create_rectangle(0,self.screenHeight-128,
                             self.screenWidth,self.screenHeight,
                             fill='gray',tags='menuBar')
        
        self.canvas.create_rectangle(self.screenWidth-256,0,
                                     self.screenWidth,self.screenHeight-256,
                                     fill='gray',tags='menuBar')
        
        self.background = PhotoImage(file="cosmosBG.gif")
        #self.background.zoom(self.width, self.height)
        self.canvas.create_image(0,0,anchor=NW,image=self.background)

        self.drawEtoiles()
        '''
    def click(self,event):
        eventX = event.x
        eventY = event.y
        print(str(eventX)+str(eventY))
    
    def resize(self,event):
        self.screenWidth = event.width
        self.screenHeight = event.height
        self.width = self.screenWidth-256;
        self.height = self.screenHeight-128;
        
        self.drawMenu()
        
        '''
        self.canvas.delete("menuBar")
        self.canvas.create_rectangle(0,self.screenHeight-128,
                                     self.screenWidth,self.screenHeight,
                                     fill='gray',tags="menuBar")
        
        self.canvas.create_rectangle(self.screenWidth-256,0,
                                     self.screenWidth,self.screenHeight-128,
                                     fill='gray',tags="menuBar")
        '''
        
    def drawMenu(self):
        
        self.buttonWidth = 200
        self.buttonHeight = 64
        
        buttonPosX = ((self.screenWidth/2)-self.buttonWidth/2)
        buttonPosY = self.screenHeight/3
        
        self.canvas.delete("menu")
        
        self.canvas.create_rectangle(buttonPosX, buttonPosY,
                                     buttonPosX+self.buttonWidth, buttonPosY+self.buttonHeight, 
                                     fill='gray', activefill='white', tags='menu')
        
        self.canvas.create_rectangle(buttonPosX, buttonPosY+self.buttonHeight+2,
                                     buttonPosX+self.buttonWidth, buttonPosY+(self.buttonHeight*2)+2, 
                                     fill='gray', activefill='white', tags='menu')
        
        self.canvas.create_rectangle(buttonPosX,buttonPosY+(self.buttonHeight*2)+4,
                                     buttonPosX+self.buttonWidth,buttonPosY+(self.buttonHeight*3)+4,
                                     fill='gray',activefill='white',tags='menu')
        
        self.canvas.create_text(buttonPosX+100,buttonPosY+32,
                                text='New game',fill='black',activefill='white',
                                font=('consolas','16'),
                                tags='menu')
        self.canvas.create_text(buttonPosX+100,buttonPosY+96,
                                text='High scores',
                                fill='black',activefill='white',
                                font=('consolas','16'),
                                tags='menu')
        self.canvas.create_text(buttonPosX+100,buttonPosY+160,
                                text='Quit game',
                                fill='black',activefill='white',
                                font=('consolas','16'),
                                tags='menu')
        
    def drawEtoiles(self):
        for e in self.listeEtoiles:
            posX = int((e.posX*self.width-100)/100)
            posY = int((e.posY*self.height-100)/100)
            self.canvas.create_oval(posX,posY,posX+32,posY+32,fill='green')
            print(str(posX)+' '+str(posY))