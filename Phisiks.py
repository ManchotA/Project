"""
En gros ce programme fonctionne de la manière suivante :
Des blocs sont définis par des listes de variables changeantes (comme leurs coordonnées) dans une liste.
Ces blocs sont testés à chaque temps (tick en quelque sorte) et des calculs sont faits.
Si ces cubes ne sont pas sur le sol ou sur un autre bloc, ils gagnent à chaque tick un nombre (vitesse Y) auquel est ajouté un facteur de gravité lié à chaque cube et qui est lui-même multiplié par un facteur de gravité universelle à tout le code.
Ainsi ces variables sont manipulées de telle sorte que les cubes tombent avec un certain réalisme.

Lors de collisions, des opérations à base de facteur de rebond sont appliquées.
Et lors de collisions avec d'autres cubes, leur nouvelle vitesse est calculée par une formule.

Et en X, les cubes subissent une force de friction universelle à tout le code.

Afin de pouvoir jeter les cubes, leurs positions entre le tick actuel et celui d'avant sont comparées afin de déterminer leur vitesse quand le bouton est relâché.

Chaque partie du programme et de la fonction de base est expliquée en général et ensuite les lignes de code sont expliquées.
Les parties du code sont assez indépendantes, donc si l'une n'est pas compréhensible, il est possible de la passer.
"""
#import des modules :
from tkinter import *#module visuel
from random import *#module aléatoire
from math import *#module pour des opérations mathématiques
import copy#module pour faire des copies de listes complètes (pas juste des pointeurs)

#Définition des dimensions de la fenêtre
resox=1200#taille en largeur
resoy=800#taille en hauteur
resolutionstr=str(resox)+"x"+str(resoy)#str qui définit les dimensions de la fenêtre
reso=resox/50#Taille relative à la taille de la fenêtre afin de ne pas la changer à chaque nouvelle définition

root=Tk()#création de la fenêtre
root.geometry(resolutionstr)#définition de sa taille

#Définition des variables
pos=[[50,750-reso,0,0,[50,150],[750-reso,750-reso],0.5,0.5,1,0,True],
[250,750-reso,0,0,[250,250],[750-reso,750-reso],0.5,0.5,1,0,True],
[450,750-reso,0,0,[450,450],[750-reso,750-reso],0.5,0.5,1,0,True],
[650,750-reso,0,0,[650,650],[750-reso,750-reso],0.5,0.5,1,0,True],
[850,750-reso,0,0,[850,850],[750-reso,750-reso],0.5,0.5,1,0,True],
[1050,750-reso,0,0,[1050,1050],[750-reso,750-reso],0.5,0.5,1,0,True]]
#/\ Liste des blocs avec les informations dans l'ordre : position à l'origine en X(0), position à l'origine en Y(1), vitesse de l'objet horizontalement (2), vitesse de l'objet verticalement(3), positions en X au dernier tour de boucle et à l'actuel (4), positions en Y au dernier tour de boucle et à l'actuel (5), gain de vitesse en Y à chaque tour de boucle à savoir le facteur de gravité(6), facteur de rebondissement (7), masse de l'objet(8), Sert juste à savoir à quel moment l'objet passe d'aller vers le haut à vers le bas pour remettre à 0 son facteur de gravité(9), savoir s'il est ou non sur un mur(10)
mur=[]
for i in range(len(pos)) :
    if pos[i][4][0]!=pos[i][0] :
        pos[i][4][0]=pos[i][0]
    if pos[i][4][1]!=pos[i][0] :
        pos[i][4][1]=pos[i][0]

    if pos[i][5][0]!=pos[i][1] :
        pos[i][5][0]=pos[i][1]
    if pos[i][5][1]!=pos[i][1] :
        pos[i][5][1]=pos[i][1]
posS=copy.deepcopy(pos)#copie des informations des cubes pour la réinitialisation
fin=False#Savoir si la boucle principale est active (True=inactive, False=active)
CurseurX=0#Décalage entre la droite de la fenêtre et du canvas(par exemple si la fenêtre est en plein écran) car les coordonnées des cubes étant par rapport au canvas, il faut qu'elles soient comparables à celle de la souris
CurseurY=0#même chose mais décalage entre le haut de la fenêtre et celui du canvas
SELECTION=-1#cube sélectionné par la souris (id) si égal à -1, aucune sélection
ge=0#compteur de tour de boucle (pas d'utilité dans le code)
GRAVITE=1.01#intensité de la gravité (multiplicateur de du facteur de gravité des cubes) si <0 alors bug, si <1 alors n'importe quoi si >1 et <2 ça va si >2 alors bug
FRICTION=0.05#intensité des frottements (enlevée à la vitesse en X à chaque tour)
rect=False#sert à savoir si le rectangle est affiché ou pas (le truc pour voir plus haut)
Tuto=0#Étape du tuto
tuto1c=0#Temps d'affichage du tuto 2 et 3

#Fonction qui agit comme un sleep mais sans faire bugger tkinter

def tksleep(self,time:float)->None :
self.after(int(time),self.quit)
self.mainloop()

#Fonction principale

def Affichage():
    global SELECTION,pos,ge,a,b,rect,tuto1c,Tuto #variables définies en global
    while not fin: #boucle générale
        ge+=1 #compteur mis à jour

        #Nettoyage de la fenêtre
        for w in root.winfo_children():
            w.destroy()
        root.pack_propagate(0)

        #Création du canvas
        fond=Canvas(root,width=resox,height=resoy,bg="white")
        fond.pack()

        #Création des murs
        fond.create_rectangle(0,0,50,resoy,fill="grey")
        fond.create_rectangle(0,resoy,resox,resoy-50,fill="grey")
        fond.create_rectangle(resox,0,resox-50,resoy,fill="grey")

        #Création des rectangles (les objets) et des numéros dessus
        for i in range(len(pos)):
            fond.create_rectangle(pos[i][0],pos[i][1],pos[i][0]+reso,pos[i][1]+reso,fill="#5A5A5A")
            fond.create_text(pos[i][0]+reso/2,pos[i][1]+reso/2,text=i,font=("arial",15,"bold italic"))

        for i in range(len(mur)):
            fond.create_rectangle(mur[i][0],mur[i][1],mur[i][2],mur[i][3],fill="grey")

        #Position de la souris
        a,b=ceil(root.winfo_pointery()-root.winfo_rooty()-CurseurY),floor(root.winfo_pointerx()-root.winfo_rootx()-CurseurX)

        #Affichage des tutoriels
        if Tuto==0: #Premier tutoriel
            fond.create_text(resox/2,resoy/4,text="Sélectionnez un cube avec le clic gauche\nmaintenu et déplacez-le en\nbougeant la souris.",font=("arial",15))
        elif Tuto==1: #Deuxième tutoriel
            if tuto1c==0:
                tuto1c=ge
            fond.create_text(resox/2,resoy/4,text="Les cubes sont soumis à des forces artificielles\net peuvent entrer en collision\nentre eux et avec les murs.",font=("arial",15))
            if ge-tuto1c==500: #au bout de 500 tours, le tutoriel change
                Tuto=2
                tuto1c=0
        elif Tuto==2: #Troisième tutoriel
            if tuto1c==0:
                tuto1c=ge
            fond.create_text(resox/2,resoy/4,text="Les touches :\n- Maj+K produisent un bug artificiel qui stoppe l'application.\n- E produit une explosion invisible qui expulse les cubes.\n- P réinitialise la position et la vitesse de tous les cubes.",font=("arial",15))
            if ge-tuto1c==500: #au bout de 500 tours, le tutoriel s'arrête
                Tuto=3
                tuto1c=0
        elif Tuto==3: #Quatrième tutoriel
            if tuto1c==0:
                tuto1c=ge
            fond.create_text(resox/2,resoy/4,text="Pour modifier le poids, la position ou le rebondissement\ndes carrés, vous devez le faire dans le code directement\ndans la définition de la variable.",font=("arial",15))
            if ge-tuto1c==500: #au bout de 500 tours, le tutoriel change
                Tuto=4
                tuto1c=0

        #Transport du cube sélectionné (s'il y en a un) à la position de la souris
        if SELECTION!=-1:
            pos[SELECTION][0]=b
            pos[SELECTION][1]=a

        #Boucle pour mettre à jour les paramètres des cubes
        for i in range(len(pos)):
            if SELECTION!=i: #Si le cube n'est pas sélectionné (pour ne pas qu'il bouge lorsqu'il est transporté)

                #Changement de position
                gezx=0 #réinitialise la variable (condition de mouvement X validé ou pas)
                for j in range(len(pos)): #boucle qui vérifie si le bloc peut bouger en X
                    #Si le cube i va entrer en collision avec un autre cube ou s'il est collé au sol alors...
                    if isclose(pos[i][0]+pos[i][2],pos[j][0],abs_tol=reso) and isclose(pos[i][1],pos[j][1],abs_tol=reso) and j!=i and not (pos[i][1]<resoy-50-reso and pos[j][1]<resoy-50-reso):
                        gezx=1 #si le cube n'est pas dans les conditions pour bouger alors la variable passe en 1 (c'est comme false et true)
                        break #pas besoin de vérifier si le cube i est en contact avec d'autres cubes
                if gezx==0: #si le cube est dans les conditions pour bouger en X
                    pos[i][0]+=pos[i][2] #La position du cube gagne sa vitesse déterminée au tour de boucle précédent

                #même chose pour l'axe Y
                gezy=0
                for j in range(len(pos)):
                    if isclose(pos[i][1]+pos[i][3],pos[j][1],abs_tol=reso) and isclose(pos[i][0],pos[j][0],abs_tol=reso) and j!=i and not (pos[i][1]<resoy-50-reso and pos[j][1]<resoy-50-reso):
                        gezy=1
                        BLOCD=j
                        break
                if gezy==0 :
                    pos[i][1]+=pos[i][3]
            

            #mise a jour des variable (On va imaginer qu'on est au tour T)
            pos[i][4][0]=pos[i][4][1] #La position X du tour T-2 est transformé en la position du tours T-1
            pos[i][4][1]=pos[i][0] #La position X du tours T-1 est remplacé par celle du tour T

            pos[i][5][0]=pos[i][5][1] #La position Y du tour T-2 est transformé en la position du tours T-1
            pos[i][5][1]=pos[i][1] #La position Y du tours T-1 est remplacé par celle du tour T

            pos[i][2]=pos[i][4][1]-pos[i][4][0] #La vitesse X est donc la postion actuel en X moins celle du tours precedent (Les operations se font ensuite sur cette vitesse)
            pos[i][3]=pos[i][5][1]-pos[i][5][0] #La vitesse Y est donc la postion actuel en Y moins celle du tours precedent (Les operations se font ensuite sur cette vitesse)


            #Operation sur les vitesse
            if SELECTION!=i :
                #D'abord en X (Il faut comprendre que les position informatiquement sont determiné grace aux coordonnées en pixel de leurs coin haut gauche avec le coin en haut a gauche de la fenetre a 0,0 et que les vitesses ici corresponde a des pixels perdu ou gagné a chaque tours en fonction de la direction IL NE S'AGIT PAS DE VALEURS STRICTEMENT POSITIVE)
                if pos[i][2]>0 : #Si la vitesse en X est positive alors...
                    pos[i][2]-=FRICTION #cette vitesse perd la valeur fixé des frottements
                elif pos[i][2]<0 : #et si elle est negative...
                    pos[i][2]+=FRICTION #elle perd la valeur frottements
                if pos[i][1]<resoy-50-reso and gezy==0 and pos[i][10] : #si le cube peut bouger sur l'axe Y
                    pos[i][3]+=pos[i][6] #La vitesse en Y gagne donc son facteur de gravité
                    pos[i][6]*=GRAVITE #et ce facteur est mis a jour selon la constante de la gravité fixé, ca sert a faire tomber le cube de plus en plus vite
                
                else : #et si le cube ne peut pas bouger
                    if gezy==0 and pos[i][10] : #si le cube est donc sous le sol (si il heurt le sol)
                        gik=True #reinitialisation de la variable
                        rkso=1 #reinitialisation de la variable
                        if pos[i][3]!=0 : #si le cube n'est pas immobile en Y
                            while gik :
                                if abs((resoy-50-reso)-(pos[i][1]+pos[i][3]))-0.5*(1.01**rkso)<=0 : #Compliqué a expliquer : En gros le programme de base si le cube touche le sol, lui inverse sa vitesse avec un facteur rebondissement, cependant ca ne couvre que le cas ou le cube arrive parfaitement au niveau du sol. A ce moment alors le programme marche mais si le cube doit en theorie s'enfoncer dans le sol, alors il rebondira autant que si il tappait le sol precisemment. Alors il faut lui enlever la difference entre son niveau sous le sol et le sol, mais si on fait ca telle quel alors le cube perdra plus par la suite (car la vitesse est multiplié).
                                    gik=False
                                    break
                                rkso+=1
                        else :
                            rkso=1
                        pos[i][3]*=-pos[i][7] #La vitesse en Y du cube va donc etre inversé et multipliépar son facteur de rebond
                        pos[i][3]-=abs((resoy-50-reso)-(pos[i][1]+pos[i][3]))/rkso #mise a niveau de sa vitesse réel (rapport au truc complexe au dessus)
                        pos[i][1]=resoy-50-reso #La position est donc mise au sol (reso=taille du cube est reso-50 c'est le sol)
                        pos[i][6]=0.5 #facteur de gravité remis a 0

                        pos[i][3]+=pos[i][6] #La vitesse prend en plus le facteur de gravité (il tombe plus fort ou va vers le haut moins vite)
                        
                        pos[i][5][0]=pos[i][5][1] #les positions sont remises à jour car puisqu'il y a eu une téléportation, les vitesses peuvent être modifiées et faussées
                        pos[i][5][1]=pos[i][1]
                
                #Ici on fait en sorte que le facteur de gravité se réinitialise lorsque le bloc entame sa chute. Par exemple si il a rebondit très haut il ne faut pas que sa vitesse de chute soit très forte dès qu'il retombe. (car les blocs gagnent de la force de chute en remontant)
                if pos[i][9]==0 and pos[i][3]>0: #si la vitesse de chute est positive, alors le cube tombe et donc on peut réinitialiser la vitesse.
                    pos[i][9]=1 #On met à jour cette variable (que l'on va appeler le booléen de chute) pour pas que la réinitialisation se fasse à chaque tour de la chute
                    pos[i][6]=0.5 #le facteur de gravité est remis à la base
                
                if pos[i][3]<0: #si l'objet remonte (vitesse négative) alors le booléen de chute est remis à 0
                    pos[i][9]=0 
                
                #Afin de ne pas faire baisser les vitesses à l'infini et pouvoir faire des opérations dessus on les met à 0 quand il en sont proches
                if isclose(pos[i][2],0,abs_tol=1):
                    pos[i][2]=0
                if isclose(pos[i][3],0,abs_tol=0.5):
                    pos[i][3]=0
            
            #On gère maintenant les collisions avec les murs
            if pos[i][0]<50: #si la position d'un cube est derrière le mur de gauche
                pos[i][0]=50 #sa position est remise au niveau du mur
                pos[i][2]*=-pos[i][7] #Sa vitesse est inversée et multipliée par le facteur de rebond du bloc
                pos[i][0]+=pos[i][2] #Le cube subit un déplacement
                pos[i][4][0]=pos[i][4][1] #les positions sont remises à jour car puisqu'il y a eu une téléportation, les vitesses peuvent être modifiées et faussées
                pos[i][4][1]=pos[i][0]
            if pos[i][0]>resox-50-reso: #même chose pour l'autre mur
                pos[i][0]=resox-50-reso
                pos[i][2]*=-pos[i][7]
                pos[i][0]+=pos[i][2]
                pos[i][4][0]=pos[i][4][1]
                pos[i][4][1]=pos[i][0]
            
            #Création du grand rectangle si le cube dépasse le plafond
            if pos[i][1]<0: #Si le cube dépasse la hauteur du plafond
                div=10
                if not rect:
                    fond.create_rectangle(resox/2-resox/(2*div),10,resox/2+resox/(2*div),500,fill="#EFEFEF") #Le rectangle blanc est créé
                    rect=True
                fond.create_rectangle((pos[i][0])/div+resox/2-resox/(2*div),500+(pos[i][1])/div,(pos[i][0])/div+reso/div+resox/2-resox/(2*div),500+(pos[i][1])/div+reso/div,fill="#5A5A5A") #Le cube est placé en plus petit (les facteurs de division sont purement mis au pif)
            
            fond.create_line(pos[i][0]+reso/2,pos[i][1]+reso/2,pos[i][0]+reso/2+pos[i][2]*10,pos[i][1]+reso/2+pos[i][3]*10)

            if i==0:
                print(pos[i][5],pos[i][3])
            #Gestion des murs
            cpt=False
            for j in range(len(mur)):
                #Collision
                if abs(((mur[j][2]-mur[j][0])/2+mur[j][0])-(pos[i][0]+pos[i][2]+reso/2))<=abs(mur[j][2]-mur[j][0])/2+reso/2 and abs(((mur[j][3]-mur[j][1])/2+mur[j][1])-(pos[i][1]+pos[i][3]+reso/2))<=abs(mur[j][3]-mur[j][1])/2+reso/2:
                    pos[i][2]*=-pos[i][7]
                    pos[i][0]+=pos[i][2]
                    pos[i][4][0]=pos[i][4][1]
                    pos[i][4][1]=pos[i][0]

                    #Changement des rebonds
                    if abs(pos[i][3])>2: 
                        pos[i][3]*=-pos[i][7]
                    else:
                        pos[i][3]=0
                        pos[i][10]=False
                        cpt=True
                        pos[i][1]=mur[j][1]-reso
                        pos[i][5]=[mur[j][1]-reso,mur[j][1]-reso]
                    pos[i][1]+=pos[i][3]
                    pos[i][5][0]=pos[i][5][1]
                    pos[i][5][1]=pos[i][1]
            if not cpt:
                pos[i][10]=True

            #Maintenant pour les collisions
            for j in range(len(pos)): #On regarde pour tout les autres cubes
                if i!=j: #On enlève de la sélection le cube en cours dans la boucle principale
                    if abs(pos[i][0]+pos[i][2]-(pos[j][0]+pos[j][2]))<=reso and abs(pos[i][1]+pos[i][3]-(pos[j][1]+pos[j][3]))<=reso: #Si les coordonnées sont différentes de la valeur de la taille des cubes
                        pos[i][6]=0.5 #Les facteurs de gravité sont réinitialisés
                        pos[j][6]=0.5
                        if abs(pos[i][2])<=1 and abs(pos[j][2])<=1 and abs(pos[i][3])<=1 and abs(pos[j][3])<=1 and abs(pos[i][1]-pos[j][1])<reso :
                            if pos[i][0]>pos[j][0] :
                                pos[i][0]+=reso
                                pos[i][4][0]+=reso
                                pos[i][4][1]+=reso
                            elif pos[i][0]<pos[j][0] :
                                pos[i][0]-=reso
                                pos[i][4][0]-=reso
                                pos[i][4][1]-=reso
                            if pos[i][1]>pos[j][1] :
                                pos[i][1]+=reso
                                pos[i][5][0]+=reso
                                pos[i][5][1]+=reso
                            elif pos[i][1]<pos[j][1] :
                                pos[i][1]-=reso
                                pos[i][5][0]-=reso
                                pos[i][5][1]-=reso
                        #Cette formule est chargée du transfert d'énergie et donc de vitesse
                        gezef=pos[j][2]
                        pos[j][2]=((pos[j][8]*pos[j][2]+pos[i][8]*pos[i][2]-pos[i][8]*(pos[j][2]-pos[i][2]))/(pos[j][8]+pos[i][8]))*pos[j][7]
                        pos[i][2]=(pos[j][2]+(gezef-pos[i][2]))*pos[i][7]
                        gezef=pos[j][3]
                        pos[j][3]=((pos[j][8]*pos[j][3]+pos[i][8]*pos[i][3]-pos[i][8]*(pos[j][3]-pos[i][3]))/(pos[j][8]+pos[i][8]))*pos[j][7]
                        pos[i][3]=(pos[j][3]+(gezef-pos[i][3]))*pos[i][7]
        rect=False
        tksleep(root, 10) #Si il y a un while en tkinter, le programme va exécuter l'ensemble de la boucle sans actualiser la fenêtre si le while s'effectue trop vite. Donc pour rallonger le while, on utilise cette fonction (Le sleep a le même problème)

#Fonction lié au relachement du clique gauche
def on_button_release(evt) :
    global SELECTION
    SELECTION=-1 #le cube selectionner revient a sa base

#Fonction lié a l'appuie du clique gauche
def KLIK(evt) :
    global SELECTION, Tuto
    a,b=ceil(root.winfo_pointery() - root.winfo_rooty() - CurseurY), floor(root.winfo_pointerx() - root.winfo_rootx() - CurseurX) #La position de la souris
    for i in range(len(pos)) : #dans tout les cubes...
        if b>pos[i][0] and b<pos[i][0]+reso : #... si il y en a un qui a ses coordonné en X qui encadre la position de la souris...
            if a>pos[i][1] and a<pos[i][1]+reso : #... et si ses coordonnées en Y encadre la position Y de la souris alors...
                SELECTION=i #...le cube avec ces coordonnées est alors selectionné
                if Tuto==0 : #Si la premiere etape du tuto est accompli...
                    Tuto=1 #... la deuxieme etape se lance

#De base le tp du bloc se faisait lors du detection du maintien du clique gauche mais il y avait des bugs de transport donc elle s=ne sert plus a rien mais reste en symbole du passé
def CLIC(evt) :
    global pos
    1==1

#Fonction qui genere un bug volontaire pour diverse raison mais pas utilie au programme fini
def BUG(evt) :
    print(efcdwfsgeswd)

#Fonction lié au bouton p
def debug(evt) :
    global pos
    pos=copy.deepcopy(posS) #l'ensemble des blocs sont remis a leur place de base

def Explosion(evt) :
    global pos
    a,b=ceil(root.winfo_pointery() - root.winfo_rooty() - CurseurY), floor(root.winfo_pointerx() - root.winfo_rootx() - CurseurX)
    for i in range(len(pos)) :
        pos[i][2]=-(b-pos[i][0])*1/((sqrt(abs(pos[i][0]-b)**2+abs(pos[i][1]-a)**2))/50)
        pos[i][3]=-(a-pos[i][1])*1/((sqrt(abs(pos[i][0]-b)**2+abs(pos[i][1]-a)**2))/50)

root.bind("<B1-Motion>", CLIC) #lie le maintien du clique gauche a la fonction CLIC
root.bind("<Button-1>", KLIK) #lie l'appuie du clique gauche a la fonction KLIK
root.bind("<ButtonRelease-1>", on_button_release) #lie le relachement du clique gauche a la fonction on_button_release
root.bind("<K>", BUG) #lie l'appuie de maj+k a la fonction BUG
root.bind("<p>", debug) #lie l'appuie de la touche p a la fonction debug
root.bind("<e>", Explosion) #lie l'appuie de la touche p a la fonction debug
Affichage() #Lance la fonction de base au debut du code
root.mainloop() #Definie la boucle principale de la fenetre









