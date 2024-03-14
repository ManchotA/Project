from tkinter import *
from random import *
from math import *
from PIL import Image

resox=750
resoy=750
resolutionstr=str(resox)+"x"+str(resoy)
reso=resox/30

root = Tk()
root.geometry(resolutionstr)

tailleP=100
Plateau=[]
for i in range(tailleP) :
    Plateau+=[[0]*tailleP]
a=0
fin=False
Bot=[49, 0, 2, 1, 1, 1] #X, Y, diretion(0=nord, 1=est, 2=sud, 3=ouest), probaD, probaF, probaB
BOT=[[], [], []]
Plateau[Bot[1]][Bot[0]]=2
Tipe=1 #0=sauvegardeimage, 1=affichage en cours
CHEMIN="C:/Users/33612/Desktop/NC/Programmes/IMAGE"

def tksleep(self, time:float) -> None :
    self.after(int(time), self.quit)
    self.mainloop()

def invD(k) :
    if k==0 :
        return 2
    elif k==1 :
        return 3
    elif k==2 :
        return 0
    elif k==3 :
        return 1

def Affichage() :
    global a, fin, BOT
    for w in root.winfo_children():
        w.destroy()
    root.pack_propagate(0)
    fond = Canvas(root, width=resox, height=resoy, bg="white")
    fond.pack()
    for i in range(len(Plateau)) :
        for j in range(len(Plateau[i])) :
            if Plateau[i][j]==0 :
                fond.create_rectangle(25+j*7, 25+i*7, 25+j*7+7, 25+i*7+7, fill="grey")
    while not fin :
        a+=1
        if Bot[2]==0 :
            if Bot[1]>0 and Plateau[Bot[1]-1][Bot[0]]==1 :
                Bot[3]=100
        elif Bot[2]==1 :
            if Bot[0]<99 and Plateau[Bot[1]][Bot[0]+1]==1 :
                Bot[3]=100
        elif Bot[2]==2 :
            if Bot[1]<99 and Plateau[Bot[1]+1][Bot[0]]==1 :
                Bot[3]=100
        elif Bot[2]==3 :
            if Bot[0]>0 and Plateau[Bot[1]][Bot[0]-1]==1 :
                Bot[3]=100
        Pif=randint(1, 100)
        if Pif<=Bot[3] :
            feb=Bot[2]
            while Bot[2]==feb or Bot[2]==invD(feb) :
                Bot[2]=randint(0, 3)
            Bot[3]=1
        Pif=randint(1, 5000)
        if Pif<=Bot[4] :
            if Tipe==0 :
                Plateau[Bot[1]][Bot[0]]=3
                fond.create_rectangle(25+Bot[0]*7, 25+Bot[1]*7, 25+Bot[0]*7+7, 25+Bot[1]*7+7, fill="red")
                with open(CHEMIN+"/NUM.txt", 'r') as file:
                    content = file.read()
                with open(CHEMIN+"/NUM.txt", 'w') as file:
                    file.write(str(int(content)+1))
                output_path = CHEMIN+"/Lab"+content+".png"
                with open(CHEMIN+"/Lab"+content+".txt", 'w') as file:
                    file.write(str(Plateau))
                create_colored_image(Plateau, output_path)
                fin=True
                REDO()
                return
            if Tipe==1 :
                Plateau[Bot[1]][Bot[0]]=3
                fond.create_rectangle(25+Bot[0]*7, 25+Bot[1]*7, 25+Bot[0]*7+7, 25+Bot[1]*7+7, fill="red")
                fond.create_rectangle(25+49*7, 25+0*7, 25+49*7+7, 25+0*7+7, fill="green")
                tksleep(root, 3000)
                REDO()
                fin=True
                return
        Pif=randint(1, 100)
        if Pif<=Bot[5] :
            Bot[5]=1
            for i in range(len(BOT)) :
                if BOT[i]==[] :
                    BOT[i]=[Bot[0], Bot[1], randint(0, 3), 1, 1]
                    while BOT[i][2]==Bot[2] or BOT[i][2]==invD(Bot[2]) :
                        BOT[i][2]=randint(0, 3)
                    break
        Bot[3]*=1.2
        Bot[4]*=1.01
        Bot[5]*=1.5
        if Bot[2]==0 :
            if Bot[1]==0 :
                Bot[3]=100
            else :
                Bot[1]-=1
        elif Bot[2]==1 :
            if Bot[0]==99 :
                Bot[3]=100
            else :
                Bot[0]+=1
        elif Bot[2]==2 :
            if Bot[1]==99 :
                Bot[3]=100
            else :
                Bot[1]+=1
        elif Bot[2]==3 :
            if Bot[0]==0 :
                Bot[3]=100
            else :
                Bot[0]-=1
        for i in range(len(BOT)) :
            if BOT[i]!=[] :
                BOT[i][3]*=1.01
                BOT[i][4]*=1.5
                PIF=randint(100, 100)
                if PIF<BOT[i][3] :
                    fef=BOT[i][2]
                    while BOT[i][2]==fef or BOT[i][2]==invD(fef) :
                        BOT[i][2]=randint(0, 3)
                if BOT[i][2]==0 :
                    if BOT[i][1]==0 :
                        BOT[i][3]=100
                    elif Plateau[BOT[i][1]-1][BOT[i][0]]==1 :
                        BOT[i][4]=100
                    else :
                        BOT[i][1]-=1
                elif BOT[i][2]==1 :
                    if BOT[i][0]==99 :
                        BOT[i][3]=100
                    elif Plateau[BOT[i][1]][BOT[i][0]+1]==1 :
                        BOT[i][4]=100
                    else :
                        BOT[i][0]+=1
                elif BOT[i][2]==2 :
                    if BOT[i][1]==99 :
                        BOT[i][3]=100
                    elif Plateau[BOT[i][1]+1][BOT[i][0]]==1 :
                        BOT[i][4]=100
                    else :
                        BOT[i][1]+=1
                elif BOT[i][2]==3 :
                    if BOT[i][0]==0 :
                        BOT[i][3]=100
                    elif Plateau[BOT[i][1]][BOT[i][0]-1]==1 :
                        BOT[i][4]=100
                    else :
                        BOT[i][0]-=1
                Plateau[BOT[i][1]][BOT[i][0]]=1
                fond.create_rectangle(25+BOT[i][0]*7, 25+BOT[i][1]*7, 25+BOT[i][0]*7+7, 25+BOT[i][1]*7+7, fill="white")
                PIF=randint(1, 1000)
                if PIF<BOT[i][4] :
                    BOT[i]=[]
        Plateau[Bot[1]][Bot[0]]=1
        fond.create_rectangle(25+Bot[0]*7, 25+Bot[1]*7, 25+Bot[0]*7+7, 25+Bot[1]*7+7, fill="white")
        tksleep(root, 10)

def Affichageevt(evt) :
    Affichage()

def REDO() :
    global Plateau, a, fin, Bot, BOT
    Plateau=[]
    for i in range(tailleP) :
        Plateau+=[[0]*tailleP]
    a=0
    fin=False
    Bot=[49, 0, 2, 1, 1, 1] #X, Y, diretion(0=nord, 1=est, 2=sud, 3=ouest), probaD, probaF, probaB
    BOT=[[], [], []]
    Plateau[Bot[1]][Bot[0]]=2
    Affichage()

def create_colored_image(array, output_path):
    color_mapping = {
        0: (0, 0, 0),
        1: (255, 255, 255),
        2: (0, 255, 0),
        3: (0, 0, 255)
    }
    height = len(array)
    width = len(array[0]) if height > 0 else 0
    image = Image.new("RGB", (width, height))
    pixels = image.load()
    for y in range(height):
        for x in range(width):
            pixel_value = array[y][x]
            if pixel_value in color_mapping:
                pixels[x, y] = color_mapping[pixel_value]
            else:
                raise ValueError(f"La valeur {pixel_value} dans le tableau n'a pas de correspondance de couleur.")
    image.save(output_path)

root.bind("e", Affichageevt)
Affichage()
root.mainloop()