import powerup as power
import mapB 
import bombe

class Joueur(object):
    def __init__(self, name, x, y):
        self.name = name
        self.pos_x = x
        self.pos_y = y
        self.bombs = 1
        #self.range_bombe = 1
        #range a mettre dans la classe bombe
        self.isSad = False
        self.isDead = False

    def move(self, x, y):
        #un joueur peut se déplacer sur deux dimensions
        self.pos_x = x
        self.pos_y = y

    def get_pos_x(self):
        #permet de retourner l'abscisse du joueur
        return self.pos_x

    def get_pos_y(self):
        #permet de retourner l'abscisse du joueur        
        return self.pos_y

    def place_bomb(self):
        #place une bombe où le joueur se situe
        if self.bombs >= 1:
            self.bombs -= 1
            return self.pos_x, self.pos_y
        else:
            return 0, 0

    def give_bomb(self):
        #Donne une bombe
        self.bombs += 1
    
    def boost(self):
        x=self.pos_x
        y=self.pos_y
        if Map.plateau_boost[x][y] != power.NUL:
            #nombre de bombe du joueur
            if Map.plateau_boost[x][y] == power.BOMB_UP:
                self.bombs += 1
            elif Map.plateau_boost[x][y] == power.BOMB_DOWN:
                if self.bombs > 1:
                    self.bombs-=1

            #nombre de cases concernés dans la déflagration
            elif Map.plateau_boost[x][y] == power.RANGE_UP:
                bombe.range += 1
            elif Map.plateau_boost[x][y] == power.RANGE_DOWN:
                if bombe.range > 1:
                    bombe.range -= 1
            

            #le joueur est devient malade
            elif Map.plateau_boost[x][y] == power.SAD:
                self.isSad = True
            
            
            
            


