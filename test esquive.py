from tkinter import *
from random import *
from math import *

resox=750
resoy=750
resolutionstr=str(resox)+"x"+str(resoy)
reso=resox/30

root = Tk()
root.geometry(resolutionstr)

posX=resox/2
posY=resoy/2
posX1=resox/2
posY1=resoy/2
pos=[]
fin=False
vie=10
vie1=10
attente=10
vitessedeplacement=3
vitessedebris=2
tailledebris=10
cooldown=100
point=0
point1=0
a=0
b=0
PA=False
multi=False
POINT=False
Z=False
Q=False
S=False
D=False
Z1=False
Q1=False
S1=False
D1=False

def tksleep(self, time:float) -> None :
    self.after(int(time), self.quit)
    self.mainloop()

def dellist(a) :
    b=[]
    for i in range(len(a)) :
        if a[i]!=-1 :
            b+=[a[i]]
    return b

def rejouer() :
    global posX,posX1,posY,posY1,pos,fin,vie,vie1,vitessedebris,tailledebris,cooldown,a,b,point,point1
    posX=resox/2
    posY=resoy/2
    posX1=resox/2
    posY1=resoy/2
    pos=[]
    fin=False
    vie=10
    vie1=10
    vitessedebris=2
    tailledebris=10
    cooldown=100
    point=0
    point1=0
    a=0
    b=0
    Menu()

def SoloS() :
    Affichage()

def SoloP() :
    global POINT
    POINT=True
    Affichage()

def MultiS() :
    global multi
    multi=True
    Affichage()

def MultiP() :
    global multi
    global POINT
    multi=True
    POINT=True
    Affichage()

def Menu() :
    for w in root.winfo_children():
        w.destroy()
    root.pack_propagate(0)
    fond = Canvas(root, width=resox, height=resoy, bg="black")
    fond.pack()
    btn = Button (root, text="Solo Survie", width=15, height=5, bd='3', command=SoloS)
    btn.place(x=resox/2-80, y=100)
    btn = Button (root, text="Multijoueur Survie", width=15, height=5, bd='3', command=MultiS)
    btn.place(x=resox/2-80, y=200)
    btn = Button (root, text="Solo partie", width=15, height=5, bd='3', command=SoloP)
    btn.place(x=resox/2-80, y=300)
    btn = Button (root, text="Multijoueur partie", width=15, height=5, bd='3', command=MultiP)
    btn.place(x=resox/2-80, y=400)

def Affichage() :
    global posX,posY,fin,a,pos,vie,cooldown,vitessedebris,tailledebris,posX1,posY1,vie1,point,point1,b
    while not fin :
        for w in root.winfo_children():
            w.destroy()
        root.pack_propagate(0)
        fond = Canvas(root, width=resox+150, height=resoy, bg="black")
        fond.pack()
        a+=1
        b+=1
        if a>=cooldown :
            if POINT :
                point+=1
                point1+=1
            if b>=100 :
                b=0
                if cooldown>10 :
                    cooldown-=10
                elif cooldown<=10 and cooldown>5 :
                    cooldown-=1
                elif vitessedebris<4 :
                    vitessedebris+=0.25
                elif tailledebris<50 :
                    tailledebris+=2
                elif POINT :
                    fin=True
                    print(point,point1)
                    rejouer()
                    return
            a=0
            pif=randint(1,4)
            pif2=randint(1,100)
            BON="white"
            if pif2==75 or pif2==28 :
                BON="green"
            if pif==1 :
                pos+=[[randint(1,int(resox-reso-1)),1,uniform(-1, 1),1,BON]]
            if pif==2 :
                pos+=[[randint(1,int(resox-reso-1)),resoy-reso-1,uniform(-1, 1),-1,BON]]
            if pif==3 :
                pos+=[[1,randint(1,int(resoy-reso-1)),1,uniform(-1, 1),BON]]
            if pif==4 :
                pos+=[[resox-reso-1,randint(1,int(resoy-reso-1)),-1,uniform(-1, 1),BON]]
        fond.create_rectangle(posX, posY, posX+reso-5, posY+reso-5, fill="blue")
        if multi :
            fond.create_rectangle(posX1, posY1, posX1+reso-5, posY1+reso-5, fill="red")
            if not POINT :
                fond.create_text(posX1+(reso-5)/2, posY1+(reso-5)/2, text=vie1, font=("arial", 15, "bold italic"))
            else :
                fond.create_text(resox-100, 10, text=point1, font=("arial", 15, "bold italic"), fill="white")
        if not POINT :
            fond.create_text(posX+(reso-5)/2, posY+(reso-5)/2, text=vie, font=("arial", 15, "bold italic"))
        else :
            fond.create_text(100, 10, text=point, font=("arial", 15, "bold italic"), fill="white")
        for i in range(len(pos)) :
            if pos[i]!=-1 :
                H=[[pos[i][0],pos[i][1]],[pos[i][0]+tailledebris,pos[i][1]+tailledebris],[pos[i][0]+tailledebris/2,pos[i][1]+tailledebris/2],[pos[i][0],pos[i][1]+tailledebris],[pos[i][0]+tailledebris,pos[i][1]]]
                fond.create_rectangle(pos[i][0], pos[i][1], pos[i][0]+tailledebris, pos[i][1]+tailledebris, fill=pos[i][4])
                pos[i][0]+=pos[i][2]*vitessedebris
                pos[i][1]+=pos[i][3]*vitessedebris
                for e in H :
                    if e[0]<posX+reso-5 and e[0]>posX :
                        if e[1]<posY+reso-5 and e[1]>posY :
                            pos[i][0]=-100
                            if pos[i][4]=="green" :
                                vie+=3
                                if POINT :
                                    point+=10
                            elif not POINT :
                                vie-=1
                            elif point>=10 :
                                point-=10
                            elif point<=10 :
                                point=0
                for e in H :
                    if e[0]<posX1+reso-5 and e[0]>posX1 :
                        if e[1]<posY1+reso-5 and e[1]>posY1 :
                            pos[i][0]=-100
                            if pos[i][4]=="green" :
                                vie1+=3
                                if POINT :
                                    point1+=10
                            elif not POINT :
                                vie1-=1
                            elif point1>=10 :
                                point1-=10
                            elif point1<=10 :
                                point1=0
                if pos[i][0]>resox or pos[i][0]<0 or pos[i][1]>resoy or pos[i][1]<0 :
                    pos[i]=-1
        pos=dellist(pos)
        if Q and posX>vitessedeplacement+10 :
            posX-=vitessedeplacement
        if D and posX<resox-reso-10 :
            posX+=vitessedeplacement
        if Z and posY>vitessedeplacement+10 :
            posY-=vitessedeplacement
        if S and posY<resoy-reso-10 :
            posY+=vitessedeplacement
        if vie<=0 :
            finJ1()
            fin=True
        if Q1 and posX1>vitessedeplacement+10 :
            posX1-=vitessedeplacement
        if D1 and posX1<resox-reso-10 :
            posX1+=vitessedeplacement
        if Z1 and posY1>vitessedeplacement+10 :
            posY1-=vitessedeplacement
        if S1 and posY1<resoy-reso-10 :
            posY1+=vitessedeplacement
        if vie1<=0 and multi :
            finJ2()
            fin=True
        tksleep(root,attente)

def finJ1() :
    for w in root.winfo_children():
        w.destroy()
    root.pack_propagate(0)
    fond = Canvas(root, width=resox, height=resoy, bg="white")
    fond.pack()
    fond.create_text(int(resox//2), int(resoy//2), text="J1 perdu", font=("arial", 15, "bold italic"))
    btn = Button (root, text="rejouer", width=10, height=3, bd='3', command=rejouer)
    btn.place(x=int(resox//2)-40, y=int(resoy//2)+100)

def finJ2() :
    for w in root.winfo_children():
        w.destroy()
    root.pack_propagate(0)
    fond = Canvas(root, width=resox, height=resoy, bg="white")
    fond.pack()
    fond.create_text(int(resox//2), int(resoy//2), text="J2 perdu", font=("arial", 15, "bold italic"))
    btn = Button (root, text="rejouer", width=10, height=3, bd='3', command=rejouer)
    btn.place(x=int(resox//2)-40, y=int(resoy//2)+100)

def q_p(evt) :
    global Q
    global direction
    direction="Ouest"
    Q=True

def d_p(evt) :
    global D
    global direction
    direction="Est"
    D=True

def q_r(evt) :
    global Q
    Q=False

def d_r(evt) :
    global D
    D=False

def z_p(evt) :
    global Z
    global direction
    direction="Nord"
    Z=True

def s_p(evt) :
    global S
    global direction
    direction="Sud"
    S=True

def z_r(evt) :
    global Z
    Z=False

def s_r(evt) :
    global S
    S=False


def k_p(evt) :
    global Q1
    global direction
    direction="Ouest"
    Q1=True

def m_p(evt) :
    global D1
    global direction
    direction="Est"
    D1=True

def k_r(evt) :
    global Q1
    Q1=False

def m_r(evt) :
    global D1
    D1=False

def o_p(evt) :
    global Z1
    global direction
    direction="Nord"
    Z1=True

def l_p(evt) :
    global S1
    global direction
    direction="Sud"
    S1=True

def o_r(evt) :
    global Z1
    Z1=False

def l_r(evt) :
    global S1
    S1=False

def BUG(evt) :
    print(rezteztezr)

def pause(evt) :
    global PA,fin
    if PA :
        PA=False
        fin=False
        Affichage()
    else :
        PA=True
        fin=True

root.bind("<KeyPress-q>", q_p)
root.bind("<KeyRelease-q>", q_r)
root.bind("<KeyPress-d>", d_p)
root.bind("<KeyRelease-d>", d_r)
root.bind("<KeyPress-z>", z_p)
root.bind("<KeyRelease-z>", z_r)
root.bind("<KeyPress-s>", s_p)
root.bind("<KeyRelease-s>", s_r)
root.bind("<KeyPress-k>", k_p)
root.bind("<KeyRelease-k>", k_r)
root.bind("<KeyPress-m>", m_p)
root.bind("<KeyRelease-m>", m_r)
root.bind("<KeyPress-o>", o_p)
root.bind("<KeyRelease-o>", o_r)
root.bind("<KeyPress-l>", l_p)
root.bind("<KeyRelease-l>", l_r)
root.bind("<K>", BUG)
root.bind("<w>", pause)
Menu()









root.mainloop()