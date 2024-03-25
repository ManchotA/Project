from tkinter import *
from random import *
from math import *
import copy

resox=1200
resoy=600
resolutionstr=str(resox)+"x"+str(resoy)
reso=resox/50

root = Tk()
root.geometry(resolutionstr)

a=0
fin=False
INFO=[0, 0, 0, 0]
Bloc=[101, 451, 100, 0, [0,0]]
Z=False
Q=False
S=False
D=False
O=False
B=False
Tuto=300

def tksleep(self, time:float) -> None :
    self.after(int(time), self.quit)
    self.mainloop()

def VECTEUR(X1, Y1, X2, Y2, T) :
    if sqrt((X1-X2)**2+(Y1-Y2)**2)>0 :
        return [X1+(T/sqrt((X1-X2)**2+(Y1-Y2)**2))*(X2-X1), Y1+(T/sqrt((X1-X2)**2+(Y1-Y2)**2))*(Y2-Y1)]
    else :
        return [X1+(T/1)*(X2-X1), Y1+(T/1)*(Y2-Y1)]

def VECTEUR1(X1, Y1, X2, Y2, T) :
    return [(X2-X1)/T, (Y2-Y1)/T]

Bloc[4]=VECTEUR1(Bloc[0], Bloc[1], (resox/2+INFO[0]), (resoy/2+INFO[1]), 1000)

def Affichage() :
    global a,Bloc,Tuto
    while not fin :
        a+=1
        for w in root.winfo_children():
            w.destroy()
        root.pack_propagate(0)
        fond = Canvas(root, width=resox, height=resoy, bg="white")
        fond.pack()
        fond.create_rectangle(0, resoy/2+INFO[1], resox, resoy, fill="green")

        fond.create_oval(resox/2+INFO[0]-10, resoy/2+INFO[1]-10, resox/2+INFO[0]+10, resoy/2+INFO[1]+10, fill="black")

        if Tuto>0 :
            Tuto-=1
            fond.create_text(resox/2, 100, text="Deplacez le bloc avec Q/D horizontalement", font=("arial", 20))
            fond.create_text(resox/2, 130, text="Deplacez le bloc avec Espace/ShiftL verticalement", font=("arial", 20))
            fond.create_text(resox/2, 160, text="Deplacez le bloc avec Z/S en profondeur", font=("arial", 20))

        Bloc[2]=100-Bloc[3]/10
        if Bloc[3]>0 :
            FRD=Bloc[2]/2-Bloc[3]/5000-abs(Bloc[2]-resox/2)/110
        else :
            FRD=Bloc[2]/2-abs(Bloc[2]-resox/2)/110
        Vect=VECTEUR((Bloc[0]+INFO[0]+Bloc[2]*0.5), (Bloc[1]+INFO[1]+Bloc[2]*0.5), (resox/2+INFO[0]), (resoy/2+INFO[1]), FRD)
        fEf=sqrt((Bloc[0]+INFO[0]+Bloc[2]*0.5-(resox/2+INFO[0]))**2+((Bloc[1]+INFO[1]+Bloc[2]*0.5)-(resoy/2+INFO[1]))**2)
        if (Bloc[2]*4)/fEf!=0 :
            vect=[(Vect[0]-(Bloc[0]+INFO[0]+Bloc[2]*0.5))/((Bloc[2]*4)/fEf), (Vect[1]-(Bloc[1]+INFO[1]+Bloc[2]*0.5))/((Bloc[2]*4)/fEf)]
        else :
            vect=[0, 0]

        RATIO=sqrt(vect[0]**2+vect[1]**2)/sqrt(((Bloc[0]+INFO[0]+Bloc[2]*0.5)-(resox/2+INFO[0]))**2+((Bloc[1]+INFO[1]+Bloc[2]*0.5)-(resoy/2+INFO[1]))**2)
        vect1=VECTEUR1((Bloc[0]+INFO[0]), (Bloc[1]+INFO[1]), (resox/2+INFO[0]), (resoy/2+INFO[1]), 1)
        vect2=VECTEUR1((Bloc[0]+INFO[0]+Bloc[2]), (Bloc[1]+INFO[1]), (resox/2+INFO[0]), (resoy/2+INFO[1]), 1)
        vect3=VECTEUR1((Bloc[0]+INFO[0]), (Bloc[1]+INFO[1]+Bloc[2]), (resox/2+INFO[0]), (resoy/2+INFO[1]), 1)
        vect4=VECTEUR1((Bloc[0]+INFO[0]+Bloc[2]), (Bloc[1]+INFO[1]+Bloc[2]), (resox/2+INFO[0]), (resoy/2+INFO[1]), 1)

        vect1=[vect1[0]*RATIO+Bloc[0]+INFO[0], vect1[1]*RATIO+Bloc[1]+INFO[1]]
        vect2=[vect2[0]*RATIO+Bloc[0]+INFO[0]+Bloc[2], vect2[1]*RATIO+Bloc[1]+INFO[1]]
        vect3=[vect3[0]*RATIO+Bloc[0]+INFO[0], vect3[1]*RATIO+Bloc[1]+INFO[1]+Bloc[2]]
        vect4=[vect4[0]*RATIO+Bloc[0]+INFO[0]+Bloc[2], vect4[1]*RATIO+Bloc[1]+INFO[1]+Bloc[2]]

        fond.create_polygon(Bloc[0]+INFO[0], Bloc[1]+INFO[1],   Bloc[0]+INFO[0]+Bloc[2], Bloc[1]+INFO[1],   vect2[0], vect2[1],   vect1[0], vect1[1], fill="red", width=3)
        fond.create_polygon(Bloc[0]+INFO[0]+Bloc[2], Bloc[1]+INFO[1]+Bloc[2],   Bloc[0]+INFO[0]+Bloc[2], Bloc[1]+INFO[1],   vect2[0], vect2[1],   vect4[0], vect4[1], fill="red", width=3)
        fond.create_polygon(Bloc[0]+INFO[0], Bloc[1]+INFO[1]+Bloc[2],   Bloc[0]+INFO[0]+Bloc[2], Bloc[1]+INFO[1]+Bloc[2],   vect4[0], vect4[1],   vect3[0], vect3[1], fill="red", width=3)
        fond.create_polygon(Bloc[0]+INFO[0], Bloc[1]+INFO[1],   Bloc[0]+INFO[0], Bloc[1]+INFO[1]+Bloc[2],   vect3[0], vect3[1],   vect1[0], vect1[1], fill="red", width=3)
        fond.create_rectangle(Bloc[0]+INFO[0], Bloc[1]+INFO[1], Bloc[0]+INFO[0]+Bloc[2], Bloc[1]+INFO[1]+Bloc[2], fill="red", width=3)
        

        fond.create_line(Bloc[0]+INFO[0], Bloc[1]+INFO[1], vect1[0], vect1[1], fill="black", width=3)
        fond.create_line(Bloc[0]+INFO[0]+Bloc[2], Bloc[1]+INFO[1], vect2[0], vect2[1], fill="black", width=3)
        fond.create_line(Bloc[0]+INFO[0]+Bloc[2], Bloc[1]+INFO[1]+Bloc[2], vect4[0], vect4[1], fill="black", width=3)
        fond.create_line(Bloc[0]+INFO[0], Bloc[1]+INFO[1]+Bloc[2], vect3[0], vect3[1], fill="black", width=3)

        fond.create_line(vect2[0], vect2[1], vect1[0], vect1[1], fill="black", width=3)
        fond.create_line(vect2[0], vect2[1], vect4[0], vect4[1], fill="black", width=3)
        fond.create_line(vect4[0], vect4[1], vect3[0], vect3[1], fill="black", width=3)
        fond.create_line(vect3[0], vect3[1], vect1[0], vect1[1], fill="black", width=3)
        

        fde=(-Bloc[3]+1001)/200
        if O :
            Bloc[1]-=10-(Bloc[3]/100)
            Bloc[4]=VECTEUR1(Bloc[0], Bloc[1], (resox/2+INFO[0]), (resoy/2+INFO[1]), 1000-Bloc[3])
        if Q :
            Bloc[0]-=10-(Bloc[3]/100)
            Bloc[4]=VECTEUR1(Bloc[0], Bloc[1], (resox/2+INFO[0]), (resoy/2+INFO[1]), 1000-Bloc[3])
            if Bloc[0]<-(1800+resox/2) :
                Bloc[0]=(1800+resox/2)
        if B :
            Bloc[1]+=10-(Bloc[3]/100)
            Bloc[4]=VECTEUR1(Bloc[0], Bloc[1], (resox/2+INFO[0]), (resoy/2+INFO[1]), 1000-Bloc[3])
        if D :
            Bloc[0]+=10-(Bloc[3]/100)
            Bloc[4]=VECTEUR1(Bloc[0], Bloc[1], (resox/2+INFO[0]), (resoy/2+INFO[1]), 1000-Bloc[3])
            if Bloc[0]>(1800+resox/2) :
                Bloc[0]=-(1800+resox/2)
        if Z and Bloc[3]<1000 :
            Bloc[3]+=fde
            Bloc[0]+=(Bloc[4][0])*fde
            Bloc[1]+=(Bloc[4][1])*fde
        if S and Bloc[3]<=1000 :
            Bloc[3]-=fde
            Bloc[0]-=(Bloc[4][0])*fde
            Bloc[1]-=(Bloc[4][1])*fde
        tksleep(root, 10)

def OP(evt) :
    global O
    O=True

def QP(evt) :
    global Q
    Q=True

def BP(evt) :
    global B
    B=True

def DP(evt) :
    global D
    D=True

def OR(evt) :
    global O
    O=False

def QR(evt) :
    global Q
    Q=False

def BR(evt) :
    global B
    B=False

def DR(evt) :
    global D
    D=False


def ZP(evt) :
    global Z
    Z=True

def ZR(evt) :
    global Z
    Z=False

def SP(evt) :
    global S
    S=True

def SR(evt) :
    global S
    S=False

def KEY(evt) :
    print(evt.keysym)

root.bind("<KeyPress-space>", OP)
root.bind("<KeyRelease-space>", OR)
root.bind("<KeyPress-q>", QP)
root.bind("<KeyRelease-q>", QR)
root.bind("<KeyPress-Shift_L>", BP)
root.bind("<KeyRelease-Shift_L>", BR)
root.bind("<KeyPress-d>", DP)
root.bind("<KeyRelease-d>", DR)
root.bind("<KeyPress-s>", SP)
root.bind("<KeyRelease-s>", SR)
root.bind("<KeyPress-z>", ZP)
root.bind("<KeyRelease-z>", ZR)
root.bind("<Key>", KEY)
Affichage()
root.mainloop()
