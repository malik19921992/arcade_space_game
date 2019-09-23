#!/usr/bin/env python3
########################################################
## Star Wars Arcade Game
########################################################
## code under GPL licence , you can copy change and use 
########################################################
## Author: malek esmail alfutaisy
## Copyright: Copyright 2019, STAR_WARS_ARCADE
## License: GPL
## Version: 0.0.1
## Email: mathjon@gmail.com
## Status: active
########################################################
import tkinter
import re
import time
import threading
import random
from PIL import Image, ImageTk
import math

class main_class:

    _default = ""

    def __init__(self,master):
        #main variables:
        self.DICT_VARS     =    {}                                                                                                                                        
        self.z             =    self.DICT_VARS
        self.SURE          =    False
        self.score         =    0
        self.LIVESONGUI    =    3
        self.off           =    0
        #functions:
        self.Shape()
        self.TraficText(3)
        self.lab()
        self.Button2Close()
        self.bindings()
        self.setter([0],[0],0)
        self.Levels()

    def IfTouchBang(self,arg,arg2=None,NUM=None):
        if arg == 'bullet':
            self.BulletTouch()
        elif arg == "bomb":
            self.BombTouch("ALIAN",NUM)
        elif arg == "alian_ship":
            self.AlianShipTouch()
        elif arg == "MISSILE":
            self.MissileTouch(NUM)

    def BulletTouch(self):
        for TYPE in ["MISSILE","ALIAN","LORDALIAN","CRAFTALIAN"]:
                if TYPE in self.z:
                    for NUM in self.z[TYPE]["ALIVE"].keys():
                        if self.z[TYPE]["ALIVE"][NUM] == 1:
                            #print(self.z["pos"][TYPE][NUM])
                            #if self.z["pos"][TYPE][NUM]:
                            if NUM in self.z["pos"][TYPE]:
                                if self.z["pos"][TYPE][NUM]['y']-30 <= self.z["pos"]["BULIT"][0]['y'] <= (self.z["pos"][TYPE][NUM]['y']+25):
                                    if self.z["pos"]["BULIT"][0]['x']-25 <= self.z["pos"][TYPE][NUM]['x'] <= (self.z["pos"]["BULIT"][0]['x']+25):
                                        self.z[TYPE]["MOVE"][NUM] = 0
                                        self.z[TYPE]["ALIVE"][NUM] = 0
                                        self.z["BulletMove"] = 0
                                        self.SURE = False
                                        self.Drawparticle('',0,0,0,"BULIT")
                                        self.Drawparticle('',0,0,NUM,"BOMB")
                                        self.can.update()
                                        if TYPE != "MISSILE" and TYPE != "CRAFTALIAN":
                                            self.Drawparticle('fire2.png',self.z["pos"][TYPE][NUM]['x'],self.z["pos"][TYPE][NUM]['y'],NUM,TYPE)
                                            self.can.update()
                                            self.Drawparticle('',self.z["pos"][TYPE][NUM]['x'],self.z["pos"][TYPE][NUM]['y'],NUM,TYPE)
                                            self.UpdateAfter(15)
                                        elif TYPE == "MISSILE" or TYPE == "CRAFTALIAN":
                                            self.z['img'][TYPE][NUM]  = tkinter.PhotoImage(file = 'fire2.png')
                                            self.can.itemconfig(self.z['item'][TYPE][NUM], image = self.z['img'][TYPE][NUM])
                                            self.can.update()
                                            self.z['img'][TYPE][NUM]  = tkinter.PhotoImage(file = '')
                                            self.can.itemconfig(self.z['item'][TYPE][NUM], image = self.z['img'][TYPE][NUM])
                                            self.UpdateAfter(15)
                                        self.CountAlians()
                                        self.DefAlianScore(TYPE)
                                        self.can.itemconfigure(self.SCORE_NUM,text=str(self.txt5).zfill(5)) # update score
                                        if self.LIVESONGUI > 0:
                                            self.can.itemconfigure(self.LIVENUM,text=self.LIVESONGUI) # update lives
                                        elif self.LIVESONGUI <= 0:
                                            self.can.itemconfigure(self.LIVENUM,text=0)
                                            self.loop1 = 0
                                            self.lives = 0
                                        if self.Alians <= 0:
                                            self.loop1 = 0
                                            self.lives = 0
                                        self.NEXT_LEVEL = True # you win next level is true , now after finish loop , do if next level true , then...
                                        self.LEVEL1= False # finiesh level 1 , you need this to define if you finiesh win or finiesh lose
                                        self.GAMEOVER = False # you not lose

    def MissileTouch(self,MISSILE_NUM):
        if self.z["MISSILE"]["ALIVE"][MISSILE_NUM] == 1:
            for TYPE in ["LORDALIAN","SPACESHIP"]:
                if TYPE == "LORDALIAN":
                    for NUM in self.z["pos"]["LORDALIAN"].keys():
                        if self.z["LORDALIAN"]["ALIVE"][NUM] == 1:
                            if self.z["pos"][TYPE][NUM]['y']+40 >= self.z["pos"]["MISSILE"][MISSILE_NUM]['y'] >= self.z["pos"][TYPE][NUM]['y']-40:
                                if self.z["pos"][TYPE][NUM]['x']+40 >= self.z["pos"]["MISSILE"][MISSILE_NUM]['x'] >= self.z["pos"][TYPE][NUM]['x']-40:
                                    self.Drawparticle('fire2.png',self.z["pos"][TYPE][NUM]['x']+20,self.z["pos"][TYPE][NUM]['y']-20,NUM,TYPE) # draw spaceship
                                    #self.Bang(MISSILE_NUM,"MISSILE")
                                    self.z['img']["MISSILE"][MISSILE_NUM]  = tkinter.PhotoImage(file = '')
                                    self.can.itemconfig(self.z['item']["MISSILE"][MISSILE_NUM], image = self.z['img']["MISSILE"][MISSILE_NUM])
                                    self.can.update()
                                    self.z["MISSILE"]["ALIVE"][MISSILE_NUM]  =     0
                                    self.z["LORDALIAN"]["ALIVE"][NUM]        =     0
                                    self.z["LORDALIAN"]["MOVE"][NUM]         =     0       
                                    self.Drawparticle('fire2.png',self.z["pos"][TYPE][NUM]['x']+20,self.z["pos"][TYPE][NUM]['y']-20,NUM,TYPE)
                                    self.can.update()
                                    self.Drawparticle('',self.z["pos"][TYPE][NUM]['x']+20,self.z["pos"][TYPE][NUM]['y']-20,NUM,TYPE)
                                    self.MineAfter(0.2)
                                    self.Alians -= 1
                                    self.DefAlianScore(TYPE)
                                    self.can.itemconfigure(self.SCORE_NUM,text=str(self.txt5).zfill(5)) # update score
                                    self.NEXT_LEVEL = True # you win next level is true , now after finish loop , do if next level true , then...
                                    self.LEVEL1= False # finiesh level 1 , you need this to define if you finiesh win or finiesh lose
                                    self.GAMEOVER = False # you not lose
                                    if self.Alians <= 0:
                                        self.loop1 = 0
                                        self.lives = 0
                elif TYPE == "SPACESHIP":
                    if self.z["pos"]["SPACESHIP"][0]['y']+25 >= self.z["pos"]["MISSILE"][MISSILE_NUM]['y'] >= self.z["pos"]["SPACESHIP"][0]['y']-25:
                        if self.z["pos"]["SPACESHIP"][0]['x']+25 >= self.z["pos"]["MISSILE"][MISSILE_NUM]['x'] >= self.z["pos"]["SPACESHIP"][0]['x']-25:
                            self.Drawparticle('fire2.png',self.z["pos"]["SPACESHIP"][0]['x']+20,self.z["pos"]["SPACESHIP"][0]['y']-20,0,"SPACESHIP") # draw spaceship
                            #self.Bang(MISSILE_NUM,"MISSILE")
                            self.z['img']["MISSILE"][MISSILE_NUM]  = tkinter.PhotoImage(file = '')
                            self.can.itemconfig(self.z['item']["MISSILE"][MISSILE_NUM], image = self.z['img']["MISSILE"][MISSILE_NUM])
                            self.can.update()
                            self.z["MISSILE"]["ALIVE"][MISSILE_NUM] = 0
                            self.can.update()    
                            self.can.after(70,lambda:self.Drawparticle(self.z["IMAGES"]["SPACESHIP"],self.z["pos"]["SPACESHIP"][0]['x']+20,self.z["pos"]["SPACESHIP"][0]['y']-20,0,"SPACESHIP"))
                            self.lives -= 1 # lose one of three lives 
                            self.LIVESONGUI -= 1  # variable we use to update lives on gui
                            self.NEXT_LEVEL = False # you not win now , so no next level
                            self.GAMEOVER = True # if your lives is 0 , then it gaves you gameover for sure
                            self.DefAlianScore(TYPE)
                            self.can.itemconfigure(self.SCORE_NUM,text=str(self.txt5).zfill(5)) # update score
                            if self.LIVESONGUI > 0:
                                self.can.itemconfigure(self.LIVENUM,text=self.LIVESONGUI) # update lives
                            elif self.LIVESONGUI <= 0:
                                self.can.itemconfigure(self.LIVENUM,text=0)
                                self.loop1 = 0

    def BombTouch(self,TYPE,NUM):
        if self.z["pos"][TYPE][NUM]['x'] != 0:
            if self.z["pos"]["BOMB"][NUM]['y'] != 0:
                if self.z[TYPE]["ALIVE"][NUM]:
                    if self.z[TYPE]["ALIVE"][NUM] == 1:
                        if self.z["pos"]["SPACESHIP"][0]['y']+25 >= self.z["pos"]["BOMB"][NUM]['y'] >= self.z["pos"]["SPACESHIP"][0]['y']-25: # if BOMB_Y == SPACESHIP_Y and :
                            if self.z["pos"]["SPACESHIP"][0]['x']+50 >= self.z["pos"]["BOMB"][NUM]['x'] >= self.z["pos"]["SPACESHIP"][0]['x']-25:# if BOMB_X == SPACESHIP_X                        
                                self.Drawparticle('fire2.png',self.z["pos"]["SPACESHIP"][0]['x']+20,self.z["pos"]["SPACESHIP"][0]['y']-20,0,"SPACESHIP") # draw spaceshi
                                self.Drawparticle('',0,0,NUM,"BOMB")
                                self.can.update()
                                self.can.after(250,lambda:self.Drawparticle('sp3.png',self.z["pos"]["SPACESHIP"][0]['x']+20,self.z["pos"]["SPACESHIP"][0]['y']-20,0,"SPACESHIP"))
                                self.can.update()
                                self.lives -= 1 # lose one of three lives 
                                self.LIVESONGUI -= 1  # variable we use to update lives on gui
                                self.NEXT_LEVEL = False # you not win now , so no next level
                                self.GAMEOVER = True # if your lives is 0 , then it gaves you gameover for sure
                                self.LEVEL1 = False #
                                if self.LIVESONGUI > 0:
                                    self.can.itemconfigure(self.LIVENUM,text=self.LIVESONGUI) # update lives
                                elif self.LIVESONGUI <= 0:
                                    self.can.itemconfigure(self.LIVENUM,text=0)
                                    self.loop1 = 0

    def AlianShipTouch(self):
        for TYPE in ["LORDALIAN","ALIAN"]:
             if TYPE in self.z:
                for NUM in self.z[TYPE]["ALIVE"].keys():
                    if self.z[TYPE]["ALIVE"][NUM] == 1:
                        if self.z["pos"][TYPE][NUM]:
                            if self.z[TYPE]["ALIVE"][NUM] == 1:
                                if (self.z["pos"][TYPE][NUM]['y']-47) <= self.z["pos"]["SPACESHIP"][0]['y'] <= (self.z["pos"][TYPE][NUM]['y']+47):
                                    if (self.z["pos"]["SPACESHIP"][0]['x']-47) <= self.z["pos"][TYPE][NUM]['x'] <= (self.z["pos"]["SPACESHIP"][0]['x']+47):
                                        self.Drawparticle('fire2.png',self.z["pos"]["SPACESHIP"][0]['x']+20,self.z["pos"]["SPACESHIP"][0]['y']-20,0,'SPACESHIP') #fireup spaceship
                                        #self.Bang(NUM,TYPE)
                                        self.Drawparticle('fire2.png',self.z["pos"][TYPE][NUM]['x'],self.z["pos"][TYPE][NUM]['y'],NUM,TYPE)# fireup alian
                                        self.can.update()
                                        self.DefAlianScore(TYPE)
                                        self.can.itemconfigure(self.SCORE_NUM,text=str(self.txt5).zfill(5)) # update score
                                        self.Drawparticle('',0,0,NUM,'BOMB')
                                        self.Drawparticle('',0,0,0,'SPACESHIP')
                                        self.Drawparticle('',self.z["pos"][TYPE][NUM]['x'],self.z["pos"][TYPE][NUM]['y'],NUM,TYPE)# fireup alian
                                        self.Drawparticle('sp3.png',self.z["pos"]["SPACESHIP"][0]['x']+20,self.z["pos"]["SPACESHIP"][0]['y']-20,0,'SPACESHIP') #delete spaceship
                                        self.MineAfter(0.3)
                                        self.Bang = 0
                                        self.z["BulletMove"] = 0
                                        self.z[TYPE]["MOVE"][NUM] = 0
                                        self.z[TYPE]["ALIVE"][NUM] = 0
                                        self.SURE = False
                                        self.Alians -= 1
                                        self.lives -= 1 # lose one of three lives 
                                        self.LIVESONGUI -= 1  # variable we use to update lives on gui      
                                        if self.LIVESONGUI <= 0:
                                            self.can.itemconfigure(self.LIVENUM,text=0)
                                            self.NEXT_LEVEL = False # you not win now , so no next level
                                            self.GAMEOVER = True # if your lives is 0 , then it gaves you gameover for sure
                                            self.loop1 = 0
                                            self.lives = 0
                                            self.BREAK = 1
                                        elif self.LIVESONGUI > 0:
                                            if self.Alians <= 0:
                                                self.can.itemconfigure(self.LIVENUM,text=self.LIVESONGUI) # update lives
                                                self.NEXT_LEVEL = True # you not win now , so no next level
                                                self.GAMEOVER = False # if your lives is 0 , th
                                                self.loop1 = 0
                                                self.lives = 0
                                                self.BREAK = 1
                                            elif self.Alians != 0:
                                                self.can.itemconfigure(self.LIVENUM,text=self.LIVESONGUI) # update lives
                                        self.MineAfter(0.3)

    def CountAlians(self):
        Alians = 0
        for TYPE in ["ALIAN","LORDALIAN","CRAFTALIAN"]:
            if self.z[TYPE]["ALIVE"]:
                for NUM in self.z[TYPE]["ALIVE"].keys():
                    if  self.z[TYPE]["ALIVE"][NUM] == 1:
                        Alians += 1
                    else:
                        pass
        self.Alians = Alians

    def MineAfter(self,int):
        #stop every thing and wait int secounds
        #self.can.after() ---> wait only this function but others are still works
        #self.MineAfter() ---> stop all program and wait int  time then continue execution and update
        time.sleep(int)
        self.can.update()

    def SpaceStars(self):                                                                                                                                     
        colors = ["blue","red","green","white"]                                                                                                  
        for i in range(200):                                                                                                                              
            rand1 = random.randint(1,500)                                                                                                                 
            rand2 = random.randint(1,500)                                                                                                                 
            rand3 = random.uniform(0.3,1.6)                                                                                                               
            rand4 = random.choice(colors)                                                                                                                 
            self.can.create_oval(rand1-rand3,rand2-rand3,rand1+rand3,rand2+rand3,fill=rand4)

    def FlipAgainAlianPos(self):
        for NUM in self.z["pos"]["ALIAN"].keys():
            if self.z["ALIAN"]["ALIVE"][NUM] == 1:
                self.Drawparticle('alian102.png',self.X[NUM],self.Y[NUM],NUM,"ALIAN")# draw alian

    def Bang(self,NUM,TYPE):
            self.z['img'][TYPE][NUM]  = tkinter.PhotoImage(file = 'fire2.png')
            self.can.itemconfig(self.z['item'][TYPE][NUM], image = self.z['img'][TYPE][NUM])
            self.can.update()
            self.z['img'][TYPE][NUM]  = tkinter.PhotoImage(file = '')
            self.can.itemconfig(self.z['item'][TYPE][NUM], image = self.z['img'][TYPE][NUM])
            self.UpdateAfter(15)

    def AsignAlianGuide(self):
        if 'LIVETOPS' in self.z['ALIAN']:
            if self.z['ALIAN']['LIVETOPS'] != {}:
                for NUM in self.z['ALIAN']['LIVETOPS'].keys():
                    if self.z['ALIAN']['LIVETOPS'][NUM] == 1:
                        self.guide = NUM
                        break
            elif self.z['ALIAN']['LIVEBUTS'] != {}: 
                for NUM in self.z['ALIAN']['LIVEBUTS'].keys():
                    if self.z['ALIAN']['LIVEBUTS'][NUM] == 1:
                        self.guide = NUM
                        break
            else:
                pass
        else:
            pass

    def DefAlianScore(self,TYPE):
        if TYPE == "ALIAN":
            self.txt5 += 120
        elif TYPE == "LORDALIAN":
            self.txt5 += 1200
        elif "BULIT":
            self.txt5 += 100
        elif "SPACESHIP":
            self.txt5 += 1200

    def motion(self,event):
        a = event.x - self.z["pos"]["SPACESHIP"][0]['x']
        b = event.y - self.z["pos"]["SPACESHIP"][0]['y']
        self.can.move(self.z['item']['SPACESHIP'][0],a,b)
        self.z["pos"]["SPACESHIP"][0]['x'] = event.x
        self.z["pos"]["SPACESHIP"][0]['y'] = event.y
        self.chine.configure(text='x={}  y={} '.format(self.z["pos"]["SPACESHIP"][0]['x'],self.z["pos"]["SPACESHIP"][0]['y']))

    def Shape(self):
        global can
        self.can = tkinter.Canvas(fen,width=500,height=500,bg='black')
        self.SpaceStars()        
        self.can.pack()
        self.can.config(cursor='none') # hide cursor

    def Button2Close(self):
        self.bou1 = tkinter.Button(fen,text='close',command=fen.quit)
        self.bou1.pack(side=tkinter.RIGHT)

    def lab(self):
        global chine
        self.chine = tkinter.Label(fen)
        self.chine.pack(side=tkinter.LEFT)

    def bindings(self):
        self.can.bind('<Motion>',self.motion)
        self.can.bind('<Button-1>',self.BulletObject2)

    def Drawparticle(self,IMAGE,X,Y,NUM,TYPE):
        global image                                                                                                                                                                                                                                                        
        if "item" not in self.z:                                                                                                                               
            self.z["item"] = {}                                                                                                                                
        if "img" not  in self.z:                                                                                                                               
            self.z["img"] = {}                                                                                                                                 
        if TYPE not in self.z["item"]:                                                                                                                         
            self.z["item"][TYPE] = {}                                                                                                                          
        if TYPE not in self.z["img"]:                                                                                                                          
            self.z["img"][TYPE]   = {}
        #if TYPE not in self.z["pos"]:
        #    self.z["pos"][TYPE] = {}
        #    self.z["pos"][TYPE][NUM]  =  {'x':X ,'y':Y}
        if 'image' not in self.z:
            self.z["image"] = {}
        if TYPE not in self.z["image"]:
            self.z["image"][TYPE] = {}        
        self.z["pos"][TYPE][NUM] = {}
        self.z["pos"][TYPE][NUM]['x'] =  X 
        self.z["pos"][TYPE][NUM]['y'] =  Y                                                                                                                     
        self.z['img'][TYPE][NUM]      =   tkinter.PhotoImage(file=IMAGE)                                                                                            
        self.z['item'][TYPE][NUM]     =   self.can.create_image(X,Y, anchor=tkinter.NE, image=self.z['img'][TYPE][NUM])

    def Drawparticletwoflip(self,IMAGE,X,Y,NUM,TYPE):
        global image                                                                                                                                                                                                                                                        
        if "item" not in self.z:                                                                                                                               
            self.z["item"]             =   {}                                                                                                                                
        if "img" not  in self.z:                                                                                                                               
            self.z["img"]              =   {}                                                                                                                                 
        if TYPE not in self.z["item"]:                                                                                                                         
            self.z["item"][TYPE]       =   {}                                                                                                                          
        if TYPE not in self.z["img"]:                                                                                                                          
            self.z["img"][TYPE]        =   {}
        if TYPE not in self.z["pos"]:
            self.z["pos"][TYPE]        =   {}
            self.z["pos"][TYPE][NUM]   =   {'x':X ,'y':Y}
        if 'image' not in self.z:
            self.z["image"]            =   {}
        if TYPE not in self.z["image"]:
            self.z["image"][TYPE]      =   {}        
        self.z["pos"][TYPE][NUM]       =   {}
        self.z["pos"][TYPE][NUM]['x']  =   X 
        self.z["pos"][TYPE][NUM]['y']  =   Y
        self.z['img'][TYPE][NUM]       =   Image.open(IMAGE)
        self.z['image'][TYPE][NUM]     =   ImageTk.PhotoImage(self.z['img'][TYPE][NUM])                                                                         
        self.z['item'][TYPE][NUM]      =   self.can.create_image(X,Y,image=self.z['image'][TYPE][NUM])

    def Deleteparticletwoflip(self,NUM,TYPE):
        global img4
        img4  = tkinter.PhotoImage(file = '')
        self.can.after(5000,lambda:self.can.itemconfig(self.z['item'][TYPE][NUM], image = img4))

    def CheckSameAltitude(self):
        for NUM in self.Y:
            if self.Y[0] != NUM:
                self.SAMEALTITUDE = False
                break
            else:
                self.SAMEALTITUDE = True

    def RandGen(self,min=6,max=480):
        x = 0
        for i in range(self.Alians):
            self.z["RAND"][x] = random.randint(min,max)
            x += 1
        if "MISSILE" in self.z:
            self.z["MISSILE"]["RAND"] = {}
            for NUM in self.z["MISSILE"]["TRIGGER"].keys():
                self.z["MISSILE"]["RAND"][NUM] = random.randint(1,1500)

    def bombing(self,RANGE,NUM):
        if self.z["RAND"][NUM] == RANGE:  
            self.Drawparticle('bomb6.png',(self.z["pos"]["ALIAN"][NUM]['x']-15),(self.z["pos"]["ALIAN"][NUM]['y']+30),NUM,'BOMB')   
            self.z["TRIGGER"][NUM] = 1                                                                                                                                                                                                                   
        if self.z["TRIGGER"][NUM] == 1:                                                                                                                             
            self.can.move(self.z['item']['BOMB'][NUM],0,1)
            #print(self.can.coords(self.z['item']['BOMB'][NUM]))
            self.z["pos"]["BOMB"][NUM]['x']  =  int((self.can.coords(self.z['item']['BOMB'][NUM]))[0])
            self.z["pos"]["BOMB"][NUM]['y']  =  int((self.can.coords(self.z['item']['BOMB'][NUM]))[1])                                                                                                                                                                                                             
        self.IfTouchBang("bomb",NUM=NUM)

    def MissileLunch(self,SPEED,RANGE,NUM):
        #speeds:
        if SPEED == 1:
            speed = 0.001
        elif SPEED == 2:
            speed = 0.002
        elif SPEED == 3:
            speed = 0.003
        elif SPEED == 4:
            speed = 0.004
        elif SPEED == 5:
            speed = 0.005
        else:
            speed = 0.003
        if self.z["MISSILE"]["RAND"][NUM] == RANGE:
            if self.z["MISSILE"]["ALIVE"][NUM] == 0:
                self.z["MISSILE"]["ALIVE"][NUM]   = 1
                self.z["MISSILE"]["TRIGGER"][NUM] = 1
                self.MissileDraw("missile7.png",self.z["pos"]["LORDALIAN"][NUM]['x'],(self.z["pos"]["LORDALIAN"][NUM]['y']+50),NUM,"MISSILE")
        if self.z["MISSILE"]["TRIGGER"][NUM] == 1:
            if self.z["MISSILE"]["ALIVE"][NUM] == 1:
                X = round((((self.z["pos"]["SPACESHIP"][0]['x']-70) - self.z["pos"]["MISSILE"][NUM]['x'])*speed)+0.1,3)
                Y = round(((self.z["pos"]["SPACESHIP"][0]['y'] - self.z["pos"]["MISSILE"][NUM]['y'])*speed),3)
                x = float(re.sub(r'([0-9]+\.)0+([1-9]+)',r'\1\2',str(X))) # increase speed when getting closer 
                y = float(re.sub(r'([0-9]+\.)0+([1-9]+)',r'\1\2',str(Y))) # increase speed when getting closer
                self.AlianMoveOneStep(x+0.1,y+0.1,NUM,"MISSILE")
                self.MissileTracker(NUM,"MISSILE")
                self.IfTouchBang("MISSILE",NUM=NUM)

    def MissileDraw(self,IMAGE,X,Y,NUM,TYPE):
        #if "image" not in self.z:
        #    self.z["image"] = {}
        #if TYPE not in self.z["image"]:
        #    self.z["image"][TYPE] = {}
        if "item" not in self.z:                                                                                                                               
            self.z["item"] = {}                                                                                                                                
        if "img" not  in self.z:                                                                                                                               
            self.z["img"] = {}                                                                                                                                 
        if TYPE not in self.z["item"]:                                                                                                                         
            self.z["item"][TYPE] = {}                                                                                                                          
        if TYPE not in self.z["img"]:                                                                                                                          
            self.z["img"][TYPE]   = {}
        if "pos" not in self.z:
            self.z["pos"] = {}
        if "MISSILE" not  in self.z["pos"]:
            self.z["pos"]["MISSILE"] = {}
        if NUM not in self.z["pos"]["MISSILE"]:
            self.z["pos"]["MISSILE"][NUM] = {'x': X , 'y': Y}
        self.z['img']["MISSILE"][NUM]    =   Image.open(IMAGE)                                                                                      
        self.z['item']["MISSILE"][NUM]  =    self.can.create_image(X,Y,image=ImageTk.PhotoImage(Image.open(IMAGE)))

    def MissileTracker(self,NUM,TYPE):
        tracker_Pos_x = self.z["pos"]["SPACESHIP"][0]['x'] - self.z["pos"]["MISSILE"][NUM]['x']
        tracker_Pos_y = self.z["pos"]["SPACESHIP"][0]['y'] - self.z["pos"]["MISSILE"][NUM]['y']
        fd = math.atan2(tracker_Pos_x , tracker_Pos_y)/math.pi*180
        self.MissileUpdateMotionFlip(fd,NUM,TYPE)

    def MissileUpdateMotionFlip(self,deg,NUM,TYPE):
        image = ImageTk.PhotoImage(self.z['img'][TYPE][NUM].rotate(deg))
        update = self.can.itemconfig(self.z['item'][TYPE][NUM] , image=image)
        if "ROTATE" not in self.z["MISSILE"]:
            self.z["MISSILE"]["ROTATE"] = {}
        self.z["MISSILE"]["ROTATE"][NUM] = {'image': image ,'update': update}
        
    def shooting(self): #new shooting method:
        if self.SURE == True:
            if self.z["BulletMove"] == 0:
                self.Drawparticle('blt1.png',self.g-50,self.t,0,"BULIT")
                self.z["BulletMove"] = 1
            if self.z["BulletMove"] == 1: 
                self.can.move(self.z['item']['BULIT'][0],0,-3)
                self.z["pos"]["BULIT"][0]['x'] = (self.can.coords(self.z['item']['BULIT'][0]))[0]
                self.z["pos"]["BULIT"][0]['y'] = (self.can.coords(self.z['item']['BULIT'][0]))[1]
                self.IfTouchBang("bullet")
                if -12 < int(self.z["pos"]["BULIT"][0]['y']) <  -8:
                    self.Drawparticle('',(self.z["pos"]["BULIT"][0]['x']),(self.z["pos"]["BULIT"][0]['y']),0,"BULIT")
                    self.SURE = False
                    self.z["BulletMove"] = 0
                    self.IfTouchBang("bullet")

    def BulletObject2(self,event):
        self.g = event.x + 31
        self.t = event.y
        self.SURE = True

    def TraficText(self,LV):
        self.txt1="HIGH-SCORE"
        self.txt2="UP"
        self.txt3="LIVES"
        self.txt4=LV
        self.txt5 = 0
        self.txt6 = 0
        self.txt7 = "00:00:00"
        TIME_x = 375
        HSCORE_x = 215
        UP_x = 40
        LIVES_x = 95
        self.HISCOURE = self.can.create_text(HSCORE_x,17,fill="#ff4000",font="Future 19 bold",text=self.txt1)
        self.SCORE_NUM = self.can.create_text(HSCORE_x+100,17,fill="#00ff00",font="Future 16 bold",text=str(self.txt5).zfill(5))
        self.UP = self.can.create_text(UP_x,17,fill="#ff4000",font="Future 19 bold",text=self.txt2)
        self.LEVEL_NUM = self.can.create_text(UP_x-25,17,fill="#00ff00",font="Future 16 bold",text=self.txt6)
        self.LIVES = self.can.create_text(LIVES_x ,17,fill="#ff4000",font="Future 19 bold",text=self.txt3)
        self.LIVENUM = self.can.create_text(LIVES_x+40,17,fill="#00ff00",font="Future 16 bold",text=self.txt4)
        self.TIME = self.can.create_text(TIME_x ,17,fill="#ff4000",font="Future 19 bold",text="TIME")
        self.TIME_NUM = self.can.create_text(TIME_x+75 ,17,fill="#00ff00",font="Future 16 bold",text=self.txt7)
 
    def AlianMoveOneStep(self,X,Y,NUM,TYPE):
        if self.z[TYPE]["ALIVE"][NUM] == 1:
            self.can.move(self.z['item'][TYPE][NUM],X,Y)
            self.z["pos"][TYPE][NUM]['x'] = int((self.can.coords(self.z['item'][TYPE][NUM]))[0])
            self.z["pos"][TYPE][NUM]['y'] = int((self.can.coords(self.z['item'][TYPE][NUM]))[1])
            self.IfTouchBang("alian_ship",TYPE,NUM)
            #print(f'problem in self.IfTouchBang("alian_ship",TYPE,NUM), lives is :{self.lives}')

    def MoveOneStepMultiAlians(self,RANGE,X,Y):
        n = 0
        for NUM in self.z['ALIAN']['ALIVE'].keys():
            if type(X) == list:
                x = X[n]
            elif type(X) != list:
                x = X
            if type(Y) == list:
                y = Y[n]
            elif type(Y) != list:
                y = Y
            self.shooting()
            self.AlianMoveOneStep(x,y,NUM,"ALIAN")

            if self.z["ALIAN"]["ALIVE"][NUM] == 1:
                self.bombing(RANGE,NUM)
            n += 1

    def MoveLordOneStep(self,SPEED,RANGE,NUM):
        if "DIRECTION" not in self.z["LORDALIAN"]:
            self.z["LORDALIAN"]["DIRECTION"] = {}
        if self.z["LORDALIAN"]["ALIVE"][NUM] == 1:
            if  540 < self.z["pos"]["LORDALIAN"][NUM]['x'] < 600:
                self.z["LORDALIAN"]["DIRECTION"][NUM] = -1 * SPEED
            elif -540 < self.z["pos"]["LORDALIAN"][NUM]['x']  < 0  :
                self.z["LORDALIAN"]["DIRECTION"][NUM] = 1 * SPEED
            else:
                pass
            self.shooting()
            if RANGE != None:
                self.MissileLunch(1,RANGE,NUM)
            self.AlianMoveOneStep(self.z["LORDALIAN"]["DIRECTION"][NUM],0,NUM,"LORDALIAN")
        if RANGE != None:
            if self.z["LORDALIAN"]["ALIVE"][NUM] != 1:
                if self.z["MISSILE"]["ALIVE"][NUM] == 1:
                    self.MissileLunch(1,RANGE,NUM)

    def UpdateAfter(self,NUM=5):
        self.can.after(NUM)
        self.can.update()
        
    def UpdateAltitude(self):
        self.CheckSameAltitude()
        if self.SAMEALTITUDE == False:
            for NUM in self.z['ALIAN']['LIVETOPS'].keys():
                if self.z['ALIAN']['ALIVE'][NUM] != 1:
                    self.z['ALIAN']['LIVETOPS'][NUM] = 0
            for NUM in self.z['ALIAN']['LIVEBUTS'].keys():
                if self.z['ALIAN']['ALIVE'][NUM] != 1:
                    self.z['ALIAN']['LIVEBUTS'][NUM] = 0

    def GameOver(self):
        if self.GAMEOVER == True:
            if self.NEXT_LEVEL == False:
                self.Drawparticle('',0,0,0,'SPACESHIP')
                self.Drawparticle('',0,0,0,'BULIT')
                for NUM in self.z["pos"]["BOMB"].keys():
                    self.Drawparticle('',0,0,NUM,'BOMB')
                for NUM in self.z["pos"]["ALIAN"].keys():
                    self.Drawparticle('',0,0,NUM,'ALIAN')
                if self.z["pos"]["LORDALIAN"]:
                    for NUM in self.z["pos"]["LORDALIAN"].keys():
                        self.Drawparticle('',0,0,NUM,'LORDALIAN')
                if "MISSILE" in self.z["pos"]:
                    for NUM in self.z["pos"]["MISSILE"].keys():
                        self.z['img']["MISSILE"][NUM]  = tkinter.PhotoImage(file = '')
                        self.can.itemconfig(self.z['item']["MISSILE"][NUM], image = self.z['img']["MISSILE"][NUM])
                        self.can.update()
                self.can.itemconfigure(self.LIVENUM,text=0) # update levels number
                fen.after(50,lambda:self.can.create_text(242,250,fill="#ffffff",font="fixedsys 25 bold",text="GAME OVER"))
        else:
            pass
        
    def setter(self,X,Y,LEVNUM,LORD_X=None,LORD_Y=None,CRAFTALIAN=None):
        b        =   0
        f        =   0
        n        =   0
        self.X   =   X
        self.Y   =   Y
        self.can.itemconfigure(self.LEVEL_NUM,text=LEVNUM) # update levels number 
        self.lives        =    self.LIVESONGUI
        self.Alians       =    len(X)
        if len(X) != 0:
            self.CheckSameAltitude()
        self.z["pos"] = {}
        self.z["pos"]["BULIT"] = {}
        self.z["pos"]["BULIT"][0] = {'x':0,'y':0}
        self.z["pos"]["ALIAN"] = {}
        self.z["pos"]["BOMB"] = {}
        self.z["ALIAN"]  = {}
        self.z["ALIAN"]["ALIVE"] = {}
        self.z["ALIAN"]["MOVE"] = {}
        self.z["TRIGGER"] = {}
        self.z["RAND"] = {}
        self.z["BulletMove"] = 0
        if "SPACESHIP" not in self.z["pos"]:
            self.z["pos"]["SPACESHIP"] = {}
            self.z["pos"]["SPACESHIP"][0] = {'x':250,'y':250} 
        self.Drawparticle('sp3.png',self.z["pos"]["SPACESHIP"][0]['x'],self.z["pos"]["SPACESHIP"][0]['y'],0,'SPACESHIP')
        if len(X) != 0:
            for i in range(len(X)):
                self.z["pos"]["ALIAN"][n] = {"x" : X[n] , "y" : Y[n]}
                self.z["ALIAN"]["ALIVE"][n] = 1
                self.z["pos"]["BOMB"][n] = {'x':0,'y':0}
                self.z["ALIAN"]["MOVE"][n] = 1
                self.z["TRIGGER"][n] = 0
                self.Drawparticle('alian102.png',self.z["pos"]["ALIAN"][n]['x'],self.z["pos"]["ALIAN"][n]['y'],n,"ALIAN")# draw alian
                n += 1
        #if hieght is not equals:
        if self.SAMEALTITUDE == False:
            self.z['ALIAN']['ALTITUDE']                   =     {}
            self.z['ALIAN']['LIVETOPS']                   =     {}
            self.z['ALIAN']['LIVEBUTS']                   =     {}
            self.z['ALIAN']['ALTITUDE']['Y']              =     {}
            self.z['ALIAN']['ALTITUDE']['Y'][self.Y[0]]   =     {0:self.Y[0]}
            for i in self.Y:
                if self.Y[0] == i:
                    self.z['ALIAN']['ALTITUDE']['Y'][self.Y[0]][f] = i
                    f += 1
                else:
                    if i in self.z['ALIAN']['ALTITUDE']['Y']:
                        self.z['ALIAN']['ALTITUDE']['Y'][i][f] = i
                        f += 1
                    elif i not in self.z['ALIAN']['ALTITUDE']['Y']:
                        self.z['ALIAN']['ALTITUDE']['Y'][i] = {}
                        self.z['ALIAN']['ALTITUDE']['Y'][i][f] = i
                        f += 1
            ALTI_keys = []
            for i in self.z['ALIAN']['ALTITUDE']['Y'].keys():
                ALTI_keys.append(i)
            mid = int((ALTI_keys[0]+ALTI_keys[1])/2)
            for i in ALTI_keys:
                if i < mid:
                    self.tops = i
                elif i > mid:
                    self.buttoms = i
            for NUM in self.z['ALIAN']['ALTITUDE']['Y'][self.tops].keys():
                if self.z['ALIAN']['ALIVE'][NUM] == 1:
                    self.z['ALIAN']['LIVETOPS'][NUM] = 1
            for NUM in self.z['ALIAN']['ALTITUDE']['Y'][self.buttoms].keys():
                if self.z['ALIAN']['ALIVE'][NUM] == 1:
                    self.z['ALIAN']['LIVEBUTS'][NUM] = 1

        if LORD_X != None:
            self.z["pos"]["LORDALIAN"]        =     {}
            self.z['ALIAN']["LORDALIAN"]      =     {}
            self.z["LORDALIAN"]               =     {}
            self.z["LORDALIAN"]["ALIVE"]      =     {}
            self.z["LORDALIAN"]["MOVE"]       =     {}
            self.z["MISSILE"]                 =     {}
            self.z["MISSILE"]["RAND"]         =     {}
            self.z["MISSILE"]["ALIVE"]        =     {}
            self.z["MISSILE"]["TRIGGER"]      =     {}
            self.z["MISSILE"]["ALIVE"]        =     {}
            self.z["MISSILE"]["MOVE"]         =     {}
            if type(LORD_X) == int:
                self.z["pos"]["LORDALIAN"][0]      =     {"x" : LORD_X , "y" : LORD_Y}
                self.z["LORDALIAN"]["ALIVE"][0]    =     1
                self.z["LORDALIAN"]["MOVE"][0]     =     1
                self.z["MISSILE"]["TRIGGER"][0]    =     0
                self.z["MISSILE"]["ALIVE"][0]      =     0
                self.z["MISSILE"]["MOVE"][0]       =     0
                self.Alians += 1
                self.Drawparticle("lordalian.png",LORD_X,LORD_Y,0,"LORDALIAN")
            elif type(LORD_X) == list:
                for NUM in range(len(LORD_X)):
                    self.z["pos"]["LORDALIAN"][NUM]      =     {"x" : LORD_X[NUM] , "y" : LORD_Y[NUM]}
                    self.z["LORDALIAN"]["ALIVE"][NUM]    =     1
                    self.z["LORDALIAN"]["MOVE"][NUM]     =     1
                    self.z["MISSILE"]["TRIGGER"][NUM]    =     0
                    self.z["MISSILE"]["ALIVE"][NUM]      =     0
                    self.z["MISSILE"]["MOVE"][NUM]       =     0
                    self.Drawparticle("lordalian.png",LORD_X[NUM],LORD_Y[NUM],NUM,"LORDALIAN")
                    self.Alians += 1
            else:
                print('something went wrong  with LORDALIAN')
        ###############|#######################################
        #define images |                                      #
        #++++++++++++++|++++++++++++++++++++++++++++++++++++++#        
        self.z["IMAGES"]                 =   {}
        self.z["IMAGES"]["BOMB"]         =   'bomb6.png'
        self.z["IMAGES"]["ALIAN"]        =   'alian102.png'
        self.z["IMAGES"]["MISSILE"]      =   'missile7.png'
        self.z["IMAGES"]["SPACESHIP"]    =   'sp3.png'
        self.z["IMAGES"]["LORDALIAN"]    =   'lordalian.png'
        self.z["IMAGES"]["FIRE"]         =   'fire2.png'
        self.z["IMAGES"]["NOTHING"]      =   ''
        if CRAFTALIAN == 'OK':
            self.z["CRAFTALIAN"]            =   {}
            self.z["CRAFTALIAN"]["ALIVE"]   =   {}
            self.z["pos"]["CRAFTALIAN"]     =   {}
            self.z["CRAFTALIAN"]["MOVE"] = {} 
            self.CRAFTALIAN_X               =   []
            self.CRAFTALIAN_Y               =   []
            for NUM in range(16):
                self.z["CRAFTALIAN"]["ALIVE"][NUM]   =   1
                self.z["CRAFTALIAN"]["MOVE"][NUM]    =   1
                self.Alians += 1

    def CraftAlianPositioning(self):
        for NUM in range(16):
                if NUM < 8:
                    x = 650
                    y = -100
                    #x = 450
                    #y = 25
                else:
                    #x =  25
                    #y =  25
                    x = -225
                    y = -100
                self.Drawparticletwoflip('alian105.png',x,y,NUM,"CRAFTALIAN")
        for NUM in range(16):
            if NUM < 8:
                d = -0.5
                f = -0.08
                b = 6
                e = 6
            else:
                d = 0.6
                f = 0.03
                b = 8
                e = 4
            if NUM == 0:
                a = 8
                RANGE = a * e
            elif NUM == 8:
                a = 17
                RANGE = a * e  
            self.CRAFTALIAN_X.insert(NUM,d)
            self.CRAFTALIAN_Y.insert(NUM,(1 / (self.CRAFTALIAN_X[NUM] * self.CRAFTALIAN_X[NUM])))
            #print(f'alian is :{NUM} e for range is: {e}')
            for i in range(RANGE):
                self.CRAFTALIAN_X[NUM] += f
                self.AlianMoveOneStep(self.CRAFTALIAN_X[NUM],self.CRAFTALIAN_Y[NUM],NUM,"CRAFTALIAN")
            RANGE -= b
        self.can.update()

    def AlianTracker(self,TRACKED_NUM,TRACKER_NUM,TYPE):
        speed = 0.06
        tracker_Pos_x = self.z["pos"][TYPE][TRACKED_NUM]['x'] - self.z["pos"][TYPE][TRACKER_NUM]['x']
        tracker_Pos_y = self.z["pos"][TYPE][TRACKED_NUM]['y'] - self.z["pos"][TYPE][TRACKER_NUM]['y']
        fd = math.atan2(tracker_Pos_x , tracker_Pos_y)/math.pi*180
        X = round((((self.z["pos"][TYPE][TRACKED_NUM]['x']-70) - self.z["pos"][TYPE][TRACKER_NUM]['x'])*speed)+0.1,3)
        Y = round(((self.z["pos"][TYPE][TRACKED_NUM]['y'] - self.z["pos"][TYPE][TRACKER_NUM]['y'])*speed),3)
        x = float(re.sub(r'([0-9]+\.)0+([1-9]+)',r'\1\2',str(X))) # increase speed when getting closer 
        y = float(re.sub(r'([0-9]+\.)0+([1-9]+)',r'\1\2',str(Y))) # increase speed when getting closer
        self.AlianMoveOneStep(x+0.1,y+0.1,TRACKER_NUM,"CRAFTALIAN")
        self.AlianFlip(fd,TRACKER_NUM,TYPE)
        
    def AlianFlip(self,deg,NUM,TYPE):
        image = ImageTk.PhotoImage(self.z['img'][TYPE][NUM].rotate(deg))
        update = self.can.itemconfig(self.z['item'][TYPE][NUM] , image=image)
        if "ROTATE" not in self.z["CRAFTALIAN"]:
            self.z[TYPE]["ROTATE"] = {}
        self.z[TYPE]["ROTATE"][NUM] = {'image': image ,'update': update}
        
    def Level1(self):
        self.setter([500],[200],1) # set main variables for level
        while self.lives > 0:
            self.RandGen()
            for i in range(480):
                self.MoveOneStepMultiAlians(i,-1,0)
                self.UpdateAfter()
            if self.lives > 0:
                self.RandGen()
                for i in range(480):
                    self.MoveOneStepMultiAlians(i,1,0)
                    self.UpdateAfter()
        self.GameOver() # if game over , then finieshs game 
        
    def Level2(self):
        self.setter([500,35],[200,180],2) # set main variables for level
        while self.lives > 0:
            self.RandGen()
            for i in range(480):
                self.MoveOneStepMultiAlians(i,[-1,1],0,)
                self.UpdateAfter()   
            if self.lives > 0:
                self.RandGen()
                for i in range(480):
                    self.MoveOneStepMultiAlians(i,[1,-1],0)
                    self.UpdateAfter()
        self.GameOver()

    def Level3(self):
        self.setter([500,450,400,350,300],[200,200,200,200,200],3) # set main variables for level
        while self.lives > 0:
            self.RandGen(min=6,max=1500)
            for i in range(270):
                self.MoveOneStepMultiAlians(i,-1,0)
                self.UpdateAfter()
            if self.lives > 0:
                self.RandGen(min=6,max=1500)
                for i in range(270):
                    self.MoveOneStepMultiAlians(i,1,0)
                    self.UpdateAfter()
        self.GameOver()

    def Level4(self):
        self.setter([500,450,400,350,350,400,450,500],[65,65,65,65,25,25,25,25],4) # set main variables for level
        while self.lives > 0:
            #define new pos for alians  flip alians from fisrt of space:
            self.FlipAgainAlianPos()
            self.loop1 = 1
            while self.loop1 > 0:
                self.RandGen(min=6,max=1500)
                for i in range(330):
                    self.MoveOneStepMultiAlians(i,-1,0.1)        
                    self.UpdateAfter()
                    self.UpdateAltitude()
                    self.AsignAlianGuide()
                    if int(self.z["pos"]["ALIAN"][self.guide]['y']) == 500:
                        self.loop1 = 0
                        break
                if self.loop1 > 0:
                    self.RandGen(min=6,max=1500)
                    for i in range(330):
                        self.MoveOneStepMultiAlians(i,1,0.1)
                        self.UpdateAfter()
                        self.UpdateAltitude()
                        self.UpdateAltitude()
                        self.AsignAlianGuide()
                        if int(self.z["pos"]["ALIAN"][self.guide]['y']) == 500:
                            self.loop1 = 0
                            break
        self.GameOver()

    def Level5(self):
        self.setter([500,450,400,350,300,350,400,450,500,300,300,350,400,450,500],[130,130,130,130,130,90,90,90,90,90,165,165,165,165,165],5,600,45)
        while self.lives > 0:
            self.loop1 = 1
            while self.loop1 > 0:
                self.RandGen(min=6,max=1500)
                for i in range(280):
                    self.MoveLordOneStep(0.7)
                    self.MoveOneStepMultiAlians(i,-1,0)        
                    self.UpdateAfter()
                    self.UpdateAltitude()
                    self.AsignAlianGuide()
                if self.loop1 > 0:
                    self.RandGen(min=6,max=1500)
                    for i in range(50):
                        self.MoveLordOneStep(0.7)
                        self.MoveOneStepMultiAlians(i,0,0.3)
                        self.UpdateAfter()
                        self.UpdateAltitude()
                        self.AsignAlianGuide()
                if self.loop1 > 0:
                    self.RandGen(min=6,max=1500)
                    for i in range(280):
                        self.MoveLordOneStep(0.7)
                        self.MoveOneStepMultiAlians(i,1,0)
                        self.UpdateAfter()
                        self.UpdateAltitude()
                        self.AsignAlianGuide()
                if self.loop1 > 0:
                    self.RandGen(min=6,max=1500)
                    for i in range(50):
                        self.MoveLordOneStep(0.7)
                        self.MoveOneStepMultiAlians(i,0,0.3)
                        self.UpdateAfter()
                        self.UpdateAltitude()
                        self.AsignAlianGuide()
        self.GameOver()

    def Level6(self):
        self.setter([500,450,400,350,300,350,400,450,500,300,300,350,400,450,500],[130,130,130,130,130,90,90,90,90,90,165,165,165,165,165],6,600,45)
        while self.lives > 0:
            self.loop1 = 1
            while self.loop1 > 0:
                self.RandGen(min=6,max=380)
                for i in range(380):
                    self.MoveLordOneStep(0.7,i,0)
                    self.MoveOneStepMultiAlians(i,-1,0)       
                    self.UpdateAfter()
                    self.UpdateAltitude()
                    self.AsignAlianGuide()
                if self.loop1 > 0:
                    self.RandGen(min=6,max=1500)
                    for i in range(50):
                        self.MoveLordOneStep(0.7,i,0)
                        self.MoveOneStepMultiAlians(i,0,0.3)
                        self.UpdateAfter()
                        self.UpdateAltitude()
                        self.AsignAlianGuide()
                if self.loop1 > 0:
                    self.RandGen(min=6,max=1500)
                    for i in range(280):
                        self.MoveLordOneStep(0.7,i,0)
                        self.MoveOneStepMultiAlians(i,1,0)
                        self.UpdateAfter()
                        self.UpdateAltitude()
                        self.AsignAlianGuide()
                if self.loop1 > 0:
                    self.RandGen(min=6,max=1500)
                    self.z["MISSILE"]["RAND"][0] = random.randint(1,1500)
                    for i in range(50):
                        self.MoveLordOneStep(0.7,i,0)
                        self.MoveOneStepMultiAlians(i,0,0.3)
                        self.UpdateAfter()
                        self.UpdateAltitude()
                        self.AsignAlianGuide()
        self.GameOver()

    def Level7(self):
        self.setter([500,450,400,350,350,400,450,500],[150,150,150,150,100,100,100,100],7,[550,-45],[45,20])
        while self.lives > 0:
            self.RandGen(min=6,max=1500)
            for i in range(480):
                self.shooting()
                self.MoveLordOneStep(0.7,i,0)
                self.MoveLordOneStep(0.7,i,1)
                self.MoveOneStepMultiAlians(i,-1,0) 
                self.UpdateAfter()
            self.RandGen(min=6,max=1500)
            for i in range(480):
                self.shooting()
                self.MoveLordOneStep(0.7,i,0)
                self.MoveLordOneStep(0.7,i,1)
                self.MoveOneStepMultiAlians(i,1,0) 
                self.UpdateAfter()
        self.GameOver()

    def CraftAlianMultiMoves(self):
        print(f'alians: {self.Alians} , loop: {self.loop} , rangeis: {self.mm} , steps: {self.STEPS} , craftalian: {self.CRAFTALIAN_NUM}')
        if self.STEPS < 170:
            if self.loop == True:
                if self.CRAFTALIAN_NUM == 8:
                    self.CRAFTALIAN_NUM = 0
                self.CraftAlianMove()
        elif self.STEPS >= 170:
            if self.loop == True:
                self.loop = False 

    def CraftAlianMove(self):
        self.STEPS += 1
        NUM = 10
        RANGE = NUM * 1
        #for NUM in range(8):
        for i in range(RANGE):
            self.shooting()
            if self.z["CRAFTALIAN"]["ALIVE"][self.CRAFTALIAN_NUM] == 1:
                self.CRAFTALIAN_X[self.CRAFTALIAN_NUM] -= 0.08
                self.AlianMoveOneStep(self.CRAFTALIAN_X[self.CRAFTALIAN_NUM],self.CRAFTALIAN_Y[self.CRAFTALIAN_NUM],self.CRAFTALIAN_NUM,"CRAFTALIAN")
                bb = math.atan2(self.CRAFTALIAN_X[self.CRAFTALIAN_NUM],self.CRAFTALIAN_Y[self.CRAFTALIAN_NUM])/math.pi*180
                self.AlianFlip(bb,self.CRAFTALIAN_NUM,"CRAFTALIAN")
        for i in range(RANGE):
            self.shooting()
            if self.z["CRAFTALIAN"]["ALIVE"][self.CRAFTALIAN_NUM+8] == 1:
                self.CRAFTALIAN_X[self.CRAFTALIAN_NUM+8] += 0.03
                self.AlianMoveOneStep(self.CRAFTALIAN_X[self.CRAFTALIAN_NUM+8],self.CRAFTALIAN_Y[self.CRAFTALIAN_NUM+8],self.CRAFTALIAN_NUM+8,"CRAFTALIAN")
                dd = math.atan2(self.CRAFTALIAN_X[self.CRAFTALIAN_NUM+8],self.CRAFTALIAN_Y[self.CRAFTALIAN_NUM+8])/math.pi*180
                self.AlianFlip(dd,self.CRAFTALIAN_NUM+8,"CRAFTALIAN")
        self.CRAFTALIAN_NUM += 1


    def Level8(self):
        self.setter([500,450,400,350,350,400,450,500],[150,150,150,150,100,100,100,100],8,[550,-45],[45,20],CRAFTALIAN='OK')
        print(self.z["CRAFTALIAN"]["ALIVE"].keys())
        while self.lives > 0:
            self.CraftAlianPositioning()
            self.loop = True
            self.STEPS = 0
            self.CRAFTALIAN_NUM = 0
            self.RandGen(min=6,max=1500)
            for self.mm in range(480):
                self.shooting()
                self.CraftAlianMultiMoves()
                self.MoveLordOneStep(0.7,self.mm,0)
                self.MoveLordOneStep(0.7,self.mm,1)
                self.MoveOneStepMultiAlians(self.mm,-1,0)
                self.UpdateAfter(10)
            self.RandGen(min=6,max=1500)
            for self.mm in range(480):
                self.shooting()
                self.CraftAlianMultiMoves()
                self.MoveLordOneStep(0.7,self.mm,0)
                self.MoveLordOneStep(0.7,self.mm,1)
                self.MoveOneStepMultiAlians(self.mm,1,0)
                self.UpdateAfter(10)
        self.GameOver()

        # self.CraftAlianPositioning()
        # self.STEPS = 0
        # self.loop = True
        # #self.CraftAlianMove()
        # while True:
        #     self.CraftAlianPositioning()
        #     self.loop = True
        #     self.STEPS = 0
        #     for self.mm in range(480):
        #         self.shooting()
        #         self.CraftAlianMultiMoves()
        #         self.shooting()
        #         self.UpdateAfter()
                #self.can.update()
                #time.sleep(1)



    def Level9(self):
        self.setter([],[],8,[],[],CRAFTALIAN='OK')
        self.z["CRAFTALIAN"]["ALIVE"][0]   =  1 
        self.z["CRAFTALIAN"]["ALIVE"][1]   =  1 
        self.z["pos"]["CRAFTALIAN"][0]     = {'x':150 , 'y':150} 
        self.z["pos"]["CRAFTALIAN"][1]     = {'x':250 , 'y':250}
        self.z["CRAFTALIAN"]["MOVE"] = {}  
        self.z["CRAFTALIAN"]["MOVE"][0] = 1
        self.z["CRAFTALIAN"]["MOVE"][1] = 1
        print(self.z["pos"])
        #self.Drawparticletwoflip('alian105.png',150,150,0,"CRAFTALIAN")
        #self.Drawparticletwoflip('alian105.png',250,250,1,"CRAFTALIAN")
        while True:
            for i in range(480):
                self.shooting()
                self.UpdateAfter()

        #self.Deleteparticletwoflip(0,"CRAFTALIAN")
        #self.Deleteparticletwoflip(1,"CRAFTALIAN")


    def Levels(self): #new move alian:
        #self.Level1()
        #if self.GAMEOVER == False:
        #     if self.NEXT_LEVEL == True:
        #         self.Level2()
        # if self.GAMEOVER == False:
        #     if self.NEXT_LEVEL == True:
        #         self.Level3()
        # if self.GAMEOVER == False:
        #     if self.NEXT_LEVEL == True:
        #         self.Level4()
        # if self.GAMEOVER == False:
        #     if self.NEXT_LEVEL == True:
        #         self.Level5()
        # if self.GAMEOVER == False:
        #     if self.NEXT_LEVEL == True:
        #         self.Level6()
        # if self.GAMEOVER == False:
        #     if self.NEXT_LEVEL == True:
        #self.Level7()
        self.Level8()
        #self.Level9()

if __name__ == '__main__':                    
    fen  = tkinter.Tk()
    fen.resizable(0,0) # fixed size widget
    c = main_class(fen)
    fen.mainloop()
    #fen.destroy()


