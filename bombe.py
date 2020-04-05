import constantes as const
import joueur 

class Bombe():
    def __init__(self,Joueur):
        self.range = const.RANGE
        self.pos_X = Joueur.get_pos_x()
        self.pos_Y = Joueur.get_pos_y()

    def explosion(self):
        #affiche les sprites d'expolsion
        x=self.pos_X
        y=self.pos_Y
        Map.plateau[x][y] = const.EXPLOSION_CENTER
        for i in range (self.range):
            #horizontal
            Map.plateau[x+i][y] = const.EXPLOSION_H
            Map.plateau[x-i][y] = const.
            
            #vertical
            Map.plateau[x][y+i] = const.EXPLOSION_V
            Map.plateau[x][y-i] = const.EXPLOSION_V


