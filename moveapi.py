
import time,random


blocks=["f","o","X","1","2","3","4"]
items_list=["ifb"]

def getavailableplaces(carte,joueur):
    posJ=getPos(joueur,carte)
    places=[]
    cas=[]
    try:
        if (carte[posJ[0]][posJ[1]+1] == " "):
            places.append([0,1])
            cas.append(1)
    except:
        print("unavail")
    
    
    try:
        if (carte[posJ[0]][posJ[1]-1] == " " and posJ[1]-1 >= 0):
            places.append([0,-1])
            cas.append(2)
    except:
        print("unavail")

    
    try: 
        if (carte[posJ[0]+1][posJ[1]] == " "):
            places.append([1,0])
            cas.append(4)
    except:
        print("unavail")
    try:
        if (carte[posJ[0]-1][posJ[1]]== " " and posJ[0]-1 >= 0):

            places.append([-1,0])
            cas.append(3)
    except:
        print("unavail")
    return [places, cas]


def getPos(joueur,carte):
    for i in range(0,len(carte)):
        for j in range(0,len(carte[i])):
            if carte[i][j]==joueur:
                return [i,j]
    return [-1,-1]


# si possible, bouger à gauche
def moveleft(carte,player,items):
    global items_list
    position=getPos(player,carte)
    if position[1]-1>=0 and carte[position[0]][position[1]-1] not in blocks:
        if carte[position[0]][position[1]-1] in items_list:
            items.append(carte[position[0]][position[1]-1])
        carte[position[0]][position[1]]=" "
        carte[position[0]][position[1]-1]=player
    return carte, items

# si possible, bouger à droite

def moveright(carte,player,items):
    global items_list
    position=getPos(player,carte)
    if position[1]<len(carte[0])-1:
        if carte[position[0]][position[1]+1] not in blocks:
            if carte[position[0]][position[1]+1] in items_list:
                items.append(carte[position[0]][position[1]+1])
            carte[position[0]][position[1]]=" "
            carte[position[0]][position[1]+1]=player
    return carte,items

def moveup(carte,player,items):
    global items_list
    position=getPos(player,carte)
    if position[0]-1>=0 and carte[position[0]-1][position[1]] not in blocks:
        if carte[position[0]-1][position[1]] in items_list:
            items.append(carte[position[0]-1][position[1]])
        carte[position[0]][position[1]]=" "
        carte[position[0]-1][position[1]]=player
    return carte,items

def movedown(carte,player,items):
    global items_list
    position=getPos(player,carte)
    if position[0]<len(carte)-1:
        if carte[position[0]+1][position[1]] not in blocks:
            if carte[position[0]+1][position[1]] in items_list:
                items.append(carte[position[0]+1][position[1]])
            carte[position[0]][position[1]]=" "
            carte[position[0]+1][position[1]]=player
    return carte,items


def safe(carte,player,items):
    global items_list
    position = getPos(player,carte)
    if position[1]-1>=0 and carte[position[0]][position[1]-1] not in blocks:
        if carte[position[0]][position[1]-1] in items_list:
            items.append(carte[position[0]][position[1]-1])
        carte[position[0]][position[1]]=" "
        carte[position[0]][position[1]-1]=player
    if position[1]<len(carte[0])-1:
        if carte[position[0]][position[1]+1] not in blocks:
            if carte[position[0]][position[1]+1] in items_list:
                items.append(carte[position[0]][position[1]+1])
            carte[position[0]][position[1]]=" "
            carte[position[0]][position[1]+1]=player
    if position[0]-1>=0 and carte[position[0]-1][position[1]] not in blocks:
        if carte[position[0]-1][position[1]] in items_list:
            items.append(carte[position[0]-1][position[1]])
        carte[position[0]][position[1]]=" "
        carte[position[0]-1][position[1]]=player
    if position[0]<len(carte)-1:
        if carte[position[0]+1][position[1]] not in blocks:
            if carte[position[0]+1][position[1]] in items_list:
                items.append(carte[position[0]+1][position[1]])
            carte[position[0]][position[1]]=" "
            carte[position[0]+1][position[1]]=player
    return carte,items


def posebombe(player,carte):
    posplayer=getPos(player,carte)
    possible=True
    cas=0
    mabombe=[0,0]
    possibilites=getavailableplaces(carte,player)
    if len(possibilites[0]) != 0 and len(possibilites[1]) != 0:
        possible=True
        cases=possibilites[1]
        if len(cases) > 1:
            cas=cases[random.randint(0,len(cases)-1)]
        else:
            cas=cases[0]      

    if possible:
        mabombe=[posplayer[0],posplayer[1]]
        
    return [carte,mabombe]


def laluck():
    nombre=random.randint(0,100)
    if nombre in range(0,5):
        rendu="ifb"
    else:
        rendu=" "
    return rendu



def explosionbombe(carte,posebombe):
    positionbombe=[]
    carte[posebombe[0]][posebombe[1]]=" "
    
    try:
        e=carte[posebombe[0]+1][posebombe[1]]
        if(e != "X"):
            carte[posebombe[0]+1][posebombe[1]]=laluck()
    except:
        print("pos impossible")
    try:
        e=carte[posebombe[0]-1][posebombe[1]]
        if(e != "X" and posebombe[0]-1>0):
            carte[posebombe[0]-1][posebombe[1]]=laluck()
    except:
        print("pos impossible")
    try:
        e=carte[posebombe[0]][posebombe[1]+1]
        if(e != "X"):
            carte[posebombe[0]][posebombe[1]+1]=laluck()
    except:
        print("pos impossible")

    try:
        e=carte[posebombe[0]][posebombe[1]-1]
        if(e != "X" and posebombe[1]-1>0):
            carte[posebombe[0]][posebombe[1]-1]=laluck()
    except:
        print("pos impossible")
    
    return carte