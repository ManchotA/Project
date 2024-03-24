from tkinter import *
from random import *
from math import *

resox=1200
resoy=800
resolutionstr=str(resox)+"x"+str(resoy)
reso=resoy-200

root = Tk()
root.geometry(resolutionstr)

pos=[]
SERP=[700, 700, 700, 700, 700, 700, 700, 700, 700, 700]
score=0
tps=30
fin=False
cheat=1
noclip=0
A=0
difi=1
vit=10
tai=25
Tuto=300

def tksleep(self, time:float) -> None :
    self.after(int(time), self.quit)
    self.mainloop()

def restart(evt) :
    global SERP, pos, score, tps, A, fin, difi, vit, tai, cheat
    for w in root.winfo_children():
        w.destroy()
    root.pack_propagate(0)
    fond = Canvas(root, width=1600, height=1000, bg="white")
    fond.pack()
    pos=[]
    SERP=[700, 700, 700, 700, 700, 700, 700, 700, 700, 700]
    score=0
    tps=30
    fin=False
    cheat=1
    A=0
    difi=1
    vit=10
    tai=25
    Affichage()

def dellist(a) :
    b=[]
    for i in range(len(a)) :
        if a[i]!=-1 :
            b+=[a[i]]
    return b

def Affichage() :
    global pos, score, tps, A, fin, difi, vit, tai, Tuto
    while not fin :
        A+=1
        a,b=ceil(root.winfo_pointery() - root.winfo_rooty()), floor(root.winfo_pointerx() - root.winfo_rootx())
        for w in root.winfo_children():
            w.destroy()
        root.pack_propagate(0)
        fond = Canvas(root, width=1600, height=1000, bg="white")
        fond.pack()
        fond.create_rectangle(500, 50, 900, 1000, fill="grey")
        fond.create_text(1150, 125, text=score, font=("arial", 10, "bold italic"))
        if Tuto>0 :
            Tuto-=1
            fond.create_text(700, 200, text="<------------------>", font=("arial", 30))
            fond.create_text(700, 230, text="Bouez la souris pour deplacer le serpent", font=("arial", 30))
        if b-10<=500 :
            b=510
        if b+10>=900 :
            b=890
        for i in range(len(SERP)-1) :
            SERP[-i-1]=SERP[-i-2]
        SERP[0]=b

        if A>=tps :
            if tps>5 :
                vit*=1.01
                tai*=1.005
                tps-=difi
                if tps>21 :
                    difi*=0.90
                elif tps>20 and tps<21 :
                    difi=1
                elif tps <20 and tps>11 :
                    difi*=0.90
            pos+=[[randint(floor(500+tai),ceil(900-tai)), tai]]
            A=0

        for i in range(len(pos)) :
            pos[i][1]+=vit
            fond.create_rectangle(pos[i][0]-tai, pos[i][1]-tai, pos[i][0]+tai, pos[i][1]+tai, fill="green")
            if abs(pos[i][1]-reso)<19+tai and abs(SERP[0]-pos[i][0])<=10+tai :
                fin=True
                pos[i]=-1
            if pos[i]!=-1 and pos[i][1]>resoy :
                pos[i]=-1
                score+=1
        pos=dellist(pos)

        for i in range(len(SERP)) :
            fond.create_rectangle(SERP[i]-10, reso+i*20, SERP[i]+10, reso+i*20+19, fill="black", outline="")
        tksleep(root,10)

root.bind('w',restart)
Affichage()
root.mainloop()
