import numpy as np



import joueur
import constantes as const
import random
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import powerup as power

class Map(object):
    def __init__(self):
        #nombre max de joueur et ennemie sur la map
        self.nbrT = 4

        #création d'une matrice de zéros qui représenteront le sol vide auquel on ajoutera des éléments
        self.width = const.MAP_WIDTH
        self.height = const.MAP_HEIGHT
        self.plateau = np.zeros((self.width, self.height),dtype=int)

        #matrice non affichée permettant d'avoir des boosts
        self.plateau_boost = np.zeros((self.width, self.height),dtype=int)

        #Créer le premier joueur
        self.joueur_1 = joueur.Joueur('Joueur 1',1,1)
        nbrJ = 1
        nbrE = nbrT - nbrJ

        #demander cb de joueur

        self.create_map(3,1)
        #self.create_map(3,n)

        self.show()
        #self.map = []
        """
        """

    def nbJoueur(a:int):
        """
        Attention
        """
       self.nbrJ = a
       self.nbrE = nbrT - self.nbrJ 
        #Définir nbJoueur entre 1 et 4
        #nbEnnenmie = 4 - nbJoueur

    def create_map(self,nbrJ:int):
        #matrice remplie de mur
        for i in range(self.width):
            for j in range(self.height):
                self.plateau[i,j] = const.MUR

        #remplir de case et d'herbe dans la matrice 
        for i in range(1,self.width):
            for j in range(1,self.height):
                self.plateau[i,j] = random.randint(const.SOL, const.CASE)

        self.plateau[2::2, ::2] = const.MUR

        #joueur
        if self.nbrJ == 2:
            self.joueur_2 = joueur.Joueur('Joueur 2',self.width,self.height)
        
        elif self.nbrJ == 3:
            self.joueur_2 = joueur.Joueur('Joueur 2',self.width,1)
            self.joueur_3 = joueur.Joueur('Joueur 3',self.width,self.height)

        elif self.nbrJ == 4:
            self.joueur_2 = joueur.Joueur('Joueur 2',self.width,1)
            self.joueur_3 = joueur.Joueur('Joueur 3',1,self.height)
            self.joueur_4 = joueur.Joueur('Joueur 4',self.width,self.height)

        #casser les blocs a 1 pas de chaque joueur et ennemie
        #remplacer CASE par SOL

        #haut gauche
        self.plateau[2,1] = const.SOL
        self.plateau[1,2] = const.SOL

        #haut droite
        self.plateau[self.width-1,1] = const.SOL
        self.plateau[self.width,2] = const.SOL

        #bas gauche
        self.plateau[1,self.height-1] = const.SOL
        self.plateau[2,self.height] = const.SOL

        #bas droite
        self.plateau[self.width-1,self.height] = const.SOL
        self.plateau[self.width,self.height-1] = const.SOL 
    
    def create_boost(self):
        #remplir aléatoirement les boost dans la matrice 
        for i in range(2,self.width-1):
            for j in range(2,self.height-1):
                #proba: 1 case sur 5 contient un boost
                if random.randint(1,5) == 4:
                    self.plateau_boost[i,j] = random.randint(power.RANGE_UP, power.RANGE_DOWN, power.SPEED_UP, power.SPEED_DOWN, power.BOMB_UP, power.BOMB_DOWN)

        self.plateau_boost[2::2, ::2] = power.NUL



