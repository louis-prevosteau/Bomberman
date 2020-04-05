#! /usr/bin/python3
# -*- coding: utf-8 -*-
#

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
import random,time,moveapi



class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.initUI()

    def initUI(self):
        self.setStyle(QStyleFactory.create('fusion'))
        p = self.palette();
        p.setColor(QPalette.Window, QColor(125, 68, 48))
        p.setColor(QPalette.Button, QColor(196, 122, 61))
        p.setColor(QPalette.Highlight, QColor(0, 0, 0))
        p.setColor(QPalette.ButtonText, QColor(0, 0, 0))
        p.setColor(QPalette.WindowText, QColor(0, 0, 0))
        self.setPalette(p)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindow()
        self.setButton()
        self.setCenter()
        self.show()
        self.setObjectName("GamePlan")

    def setCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setWindow(self):
        self.setFixedSize(1280, 720)
        self.setWindowTitle('Bomberman')
        self.statusBar().showMessage('')

        self.setStyle(QStyleFactory.create('fusion'))
        oImage = QImage("Sprites/Menu/Background.jpg")
        sImage = oImage.scaled(QSize(1280,720))
        p = self.palette()
        p.setBrush(10, QBrush(sImage))
        self.setPalette(p)

        self.dialogs = list()
        self.setWindowFlags(Qt.SplashScreen)

    def setButton(self):
        self.buttonStart=QPushButton("",self)
        self.buttonStart.setFixedWidth(400)
        self.buttonStart.setFixedHeight(100)
        self.buttonStart.setObjectName("StartButton")
        self.buttonStart.show()
        self.buttonStart.setStyleSheet("#StartButton{ border-image: url(./Sprites/Menu/Buttons/Start/Start_Button.png);} #StartButton:hover{ border-image: url(./Sprites/Menu/Buttons/Start/Start_Button_hover.png);}")
        self.buttonStart.move(QPoint(self.frameGeometry().width()/7-70,self.frameGeometry().height()/4))
        self.buttonStart.clicked.connect(self.StartGame)

        self.buttonQuit=QPushButton("",self)
        self.buttonQuit.setFixedWidth(400)
        self.buttonQuit.setFixedHeight(100)
        self.buttonQuit.setObjectName("QuitButton")
        self.buttonQuit.show()
        self.buttonQuit.setStyleSheet("#QuitButton{ border-image: url(./Sprites/Menu/Buttons/Quit/Quit_Button.png);} #QuitButton:hover{ border-image: url(./Sprites/Menu/Buttons/Quit/Quit_Button_hover.png);}")
        self.buttonQuit.move(QPoint(self.frameGeometry().width()/7-70,self.frameGeometry().height()/1.75))
        self.buttonQuit.clicked.connect(self.quit)

    def quit(self):
        dialog = QMessageBox(self)
        font = QFont("GameplayFont",15)
        dialog.setFont(font)
        dialog.setWindowTitle("Quitter")
        dialog.setText("Quitter la partie ?")
        dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        dialog.setDefaultButton(QMessageBox.Ok)
        dialog.button(QMessageBox.Ok).clicked.connect(self.ButtonCancel)
        dialog.button(QMessageBox.Cancel).clicked.connect(self.ButtonQuitOk)
        dialog.setWindowFlags(Qt.SplashScreen)
        dialog.exec_()

    def ButtonCancel(self):
        QApplication.instance().quit()
    
    def ButtonQuitOk(self):
        pass


    """VIRGIL"""
    def StartGame(self):
        self.playerId="1"
        self.carte=createGameMap()
        self.startup()
        self.carte=prepareGame(self.nbPlayers,self.carte,False)

    def setnewBG(self):
        self.setStyleSheet("#GamePlan{background-image: url('./Sprites/gradiantwwp.png'); }")

    def startup(self):
        self.nbPlayers=2
        self.bombeposee=[False,0]
        self.Bomb=[]
        self.essai=0
        self.carte=prepareGame(self.nbPlayers,self.carte,False)
        self.starta()
    
    def starta(self):
        self.labelNbJoueurs=QLabel(self)
        self.labelNbJoueurs.move(1180,620)
        self.labelNbJoueurs.setFixedWidth(254)
        self.labelNbJoueurs.show()
        self.setZoneJeu()

        self.setnewBG()
        self.sbar=0
        self.mabombe=False
        #items a voir
        self.mesitems=[]
        self.olditemlist=[]

        self.checkThreadTimer =QTimer(self)
        self.checkThreadTimer.setInterval(16) #.5 seconds
        self.checkThreadTimer.timeout.connect(self.bougeplayer)
        self.checkThreadTimer.start()

        
        if(self.nbPlayers>1):
            self.checkThreadTimerbot =QTimer(self)
            self.checkThreadTimerbot.setInterval(500) #.5 seconds
            self.checkThreadTimerbot.timeout.connect(self.DeplacementBot)
            self.checkThreadTimerbot.start()

        self.checkThreadTimerSB =QTimer(self)
        self.checkThreadTimerSB.setInterval(2000)
        self.checkThreadTimerSB.start()

        self.checkThreadTimerVictory=QTimer(self)
        self.checkThreadTimerVictory.setInterval(500)
        self.checkThreadTimerVictory.timeout.connect(self.verifvictoire)
        self.checkThreadTimerVictory.start()

    def keyPressEvent(self,event):
        key = event.key()
        if (key == Qt.Key_Q):
            self.getMap()
            self.carte,self.mesitems=moveapi.moveleft(self.carte,self.playerId,self.mesitems)
            self.drawNewMap()
        elif (key == Qt.Key_D):
            self.getMap()
            self.carte,self.mesitems=moveapi.moveright(self.carte,self.playerId,self.mesitems)
            self.drawNewMap()
        elif key == Qt.Key_Z:
            self.getMap()
            self.carte,self.mesitems=moveapi.moveup(self.carte,self.playerId,self.mesitems)
            self.drawNewMap()
        elif key == Qt.Key_S:
            self.getMap()
            self.carte,self.mesitems=moveapi.movedown(self.carte,self.playerId,self.mesitems)
            self.drawNewMap()
        elif key == Qt.Key_B:
            if not self.mabombe:
                self.mabombe=True
                zz=moveapi.posebombe(self.playerId,self.carte)
                self.Bomb.append([zz[1],time.time()])
                self.drawNewMap()
                self.bombeposee=[True,time.time()]
            else:
                self.statusBar().showMessage("Vous ne pouvez poser qu'une bombe à la fois")
        elif key == Qt.Key_Escape:
            self.quit()

    def verifvictoire(self):
        self.getMap()
        otherusers=["1","2","3","4"]
        actualuser=self.playerId
        otherusers.remove(actualuser)
        otherusersalive=False
        actualuseralive=False
        for i in self.carte:
            for j in i:
                if j == actualuser:
                    actualuseralive=True
                if j in otherusers:
                    otherusersalive=True
        if not actualuseralive:
            self.checkThreadTimer.stop()
            self.checkThreadTimerVictory.stop()
            errbox=QMessageBox.critical(self,"Game Over!","Vous êtes mort.",QMessageBox.Ok)
            sys.exit(0)
        if not otherusersalive:
            print("Victoire !")
            self.checkThreadTimerVictory.stop()
            self.checkThreadTimerSB.stop()
            self.statusBar().showMessage("Vous venez de gagner la partie!")
            infobox = QMessageBox.information(self,"Félicitations!","Vous venez de gagner la partie !",QMessageBox.Ok)
            sys.exit(0)

    def bougeplayer(self):
        if len(self.Bomb)>0:
            if self.Bomb[0][1]+3<time.time():
                infobombe=self.Bomb.pop(0)
                mynewcontent=moveapi.explosionbombe(self.carte,infobombe[0])
                self.carte=mynewcontent
                self.mabombe=False
                self.drawNewMap()


    def DeplacementBot(self):
        choixdeplacement = random.randint(0,4)
        #choixbombe = random.randint(0,1)
        choixbombe=1
        if choixdeplacement == 0:
            self.getMap()
            self.carte,rien=moveapi.moveleft(self.carte,"2",[])
            self.drawNewMap()

        elif choixdeplacement == 1:
            self.getMap()
            self.carte,rien=moveapi.moveright(self.carte,"2",[])
            self.drawNewMap()

        elif choixdeplacement == 2:
            self.getMap()
            self.carte,rien=moveapi.moveup(self.carte,"2",[])
            self.drawNewMap()

        elif choixdeplacement == 3:
            self.getMap()
            self.carte,rien=moveapi.movedown(self.carte,"2",[])
            self.drawNewMap()

        for i in self.Bomb:
            if getPos("2",self.carte) in i[0]:
                self.getMap()
                self.carte= moveapi.safe(self.carte,[])
                self.drawNewMap()

        if choixbombe == 0:
            Pose=moveapi.posebombe("2",self.carte)
            self.Bomb.append([Pose[1],time.time()])
            self.drawNewMap()
            self.bombeposee=[True,time.time()]


    def getMap(self):
        try:
            self.carte=self.renderArea.getMapStatus()
        except:
            print("echec de récupération de la carte")


    def drawNewMap(self):
        self.renderArea.redrawmap(self.carte,self.Bomb)

    def setZoneJeu(self):
        self.renderArea = RenderArea(self.carte)
        self.setCentralWidget(self.renderArea)
    """
    def SpritesTab(self):
        global BombermanDown, BombermanUp, BombermanRight, BombermanLeft
        global cptBombermanDown, cptBombermanUp, cptBombermanRight, cptBombermanLeft
        cptBombermanDown = 0
        cptBombermanUp = 0
        cptBombermanRight = 0
        cptBombermanLeft = 0

        BombermanDown=['Sprites/Bomberman/Front/Front0.png',
                       'Sprites/Bomberman/Front/Front1.png',
                       'Sprites/Bomberman/Front/Front2.png',
                       'Sprites/Bomberman/Front/Front3.png',
                       'Sprites/Bomberman/Front/Front4.png']

        BombermanUp=['Sprites/Bomberman/Back/Back0.png',
                     'Sprites/Bomberman/Back/Back1.png',
                     'Sprites/Bomberman/Back/Back2.png',
                     'Sprites/Bomberman/Back/Back3.png',
                     'Sprites/Bomberman/Back/Back4.png']
        
        BombermanRight=['Sprites/Bomberman/Right/Right0.png',
                        'Sprites/Bomberman/Right/Right1.png',
                        'Sprites/Bomberman/Right/Right2.png',
                        'Sprites/Bomberman/Right/Right3.png',
                        'Sprites/Bomberman/Right/Right4.png',
                        'Sprites/Bomberman/Right/Right5.png',
                        'Sprites/Bomberman/Right/Right6.png',
                        'Sprites/Bomberman/Right/Right7.png',
                        'Sprites/Bomberman/Right/Right8.png',]
        
        BombermanLeft=['Sprites/Bomberman/Left/Left0.png',
                        'Sprites/Bomberman/Left/Left1.png',
                        'Sprites/Bomberman/Left/Left2.png',
                        'Sprites/Bomberman/Left/Left3.png',
                        'Sprites/Bomberman/Left/Left4.png',
                        'Sprites/Bomberman/Left/Left5.png',
                        'Sprites/Bomberman/Left/Left6.png',
                        'Sprites/Bomberman/Left/Left7.png',
                        'Sprites/Bomberman/Left/Left8.png',]

    def gestionSprite(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.afficheSprite)
        self.timer.start(50)
    """
class RenderArea(QWidget):
    def __init__(self,mape, parent=None):
        self.parent=parent
        super(RenderArea,self).__init__(parent)
        self.map=mape
        self.unbreakable=QImage("./Sprites/Blocks/UnbreakableWall.png")
        self.breakable=QImage("./Sprites/Blocks/Plank.png")
        self.player=QImage("./Sprites/Bomberman/Front/Front0.png")
        self.enemy=QImage("./Sprites/Enemy/Ghost1/red1.png")
        self.bg=QImage("./Sprites/bombermanfond.png")
        self.bomb=QImage("./Sprites/Bomb/300/bomb.png")
        self.explode=QImage("./Sprites/Explosion/flame1.png")
        self.bpos=[]

    def getMapStatus(self):
        return self.map

    def redrawmap(self,carte,bpos):
        self.bpos=bpos
        self.update()
        self.oldmap=carte
        self.map=carte

    def paintEvent(self, event):
        self.oldmap=self.map
        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 0))
        painter.setBrush(QBrush(QColor(255,255,255)))
        r1=QRect((self.width()-1156)/2,(self.height()-594)/2,1156,594)
        painter.drawImage(r1,self.bg)
        emplacementX=(self.width()-1156)/2
        emplacementY=(self.height()-594)/2
        painter.setPen(QColor(0,0,0,0))
        for i in range(0,len(self.map)):
            for n in range(0,len(self.map[i])):
                j=self.map[i][n]
                rect=QRect(emplacementX,emplacementY,89,54)
                if j == "X":
                    painter.setBrush(QBrush(QColor(0,0,0)))
                    painter.drawImage(rect,self.unbreakable)
                elif j ==  "o":
                    painter.setBrush(QBrush(QColor(140, 98, 0)))
                    painter.drawImage(rect,self.breakable)
                elif j == " ":
                    nope=True
                    if len(self.bpos)>0:
                        for u in self.bpos:
                            if u[0][0] == i and u[0][1]==n:
                                nope=False
                    if nope:
                        painter.setBrush(QBrush(QColor(255,255,255,0)))
                        painter.drawRect(rect)
                    else:
                        painter.setBrush(QBrush(QColor(255, 255, 0)))
                        painter.drawImage(rect,self.bomb)
                else:
                    painter.setBrush(QBrush(QColor(255,255,255,0)))
                    painter.drawImage(rect,self.player)

                emplacementX+=89
            emplacementX=(self.width()-1156)/2
            emplacementY+=54

        painter.end()
        
def createGameMap():
    carte=[]
    for i in range(0,11):
        carte.append([])
        for j in range(0,13):
            if i % 2 != 0 and j % 2 != 0:
                carte[i].append("X")
            else:
                carte[i].append(" ")
    for i in range(0,len(carte)):
        for j in range(0,len(carte[i])):
            rdm=random.randint(0,1)
            if rdm == 1 and carte[i][j] != "X":
                carte[i][j]="o"

    return carte

def prepareGame(joueurs,carte,multi):
    for i in range(0,joueurs):
        if i == 0:
            carte[0][0]=str(i+1)
            carte[0][1]=" "
            carte[1][0]=" "
        elif i == 1:
            #if not multi:
            carte[0][len(carte[0])-1]=str(i+1)
            #else:
            #    carte[0][len(carte[0])-1]=" "
            carte[0][len(carte[0])-2]=" "
            carte[1][len(carte[0])-1]=" "
        elif i == 2:
            #if not multi:
            carte[len(carte)-1][0]=str(i+1)
            #else:
            #    carte[len(carte)-1][0]=" "
            carte[len(carte)-2][0]=" "
            carte[len(carte)-1][1]=" "
        elif i == 3:
            #if not multi:
            carte[len(carte)-1][len(carte[0])-1]=str(i+1)
            #else:
            #    carte[len(carte)-1][len(carte[0])-1]=" "
            carte[len(carte)-2][len(carte[0])-1]=" "
            carte[len(carte)-1][len(carte[0])-2]=" "
    return carte

def getPos(joueur,carte):
    for i in range(0,len(carte)):
        for j in range(0,len(carte[i])):
            if carte[i][j]==joueur:
                return [i,j]
    return [-1,-1]

def explosionbombe(carte,joueur):
    positionJ=getPos(joueur,carte)

app = Application([])
win = Window()
app.exec_()
