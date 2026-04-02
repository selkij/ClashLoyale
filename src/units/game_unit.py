

class GameUnit:
    def __init__(self, unit):
        self.unit = unit # Toutes les stats sont dedans
        self.id=id_creator()   
    def deplacement():
        if self.y > 0:
            bestID=redId[0]
            for i in range(3):
                if sqrt((self.x-redCoordinates[i][0])**2+(self.y-redCoordinates[i][1])**2) < sqrt((self.x-redCoordinates[id.index[bestID]][0])**2+(self.y-redCoordinates[id.index[bestID]][1])**2):
                    if redType[id.index[bestID]] == "tower":# Ce i in range sert à identifier l'ID de la tour courronnée la plus proche
                        bestID=redId[i]

        else:
            bestID=200 #si l'ennemi ne trouve aucun ennemi à portée et est en dessous du pont, on apllique la valeur 200 qui va dire qu'on s'oriente vers le pont le plus proche

        for i in range(len(redId)):
            if sqrt((self.x-redCoordinates[i][0])**2+(self.y-redCoordinates[i][1])**2) < sqrt((self.x-redCoordinates[id.index[bestID]][0])**2+(self.y-redCoordinates[id.index[bestID]][1])**2):
                if redType[id.index[bestID]] != "tower":# Ce i in range sert à identifier l'ID de l'unité ennemie la plus proche
                    if sqrt((self.x-redCoordinates[id.index[bestID]][0])**2+(self.y-redCoordinates[id.index[bestID]][1])**2) < 200: #portée de reconnaissance , au dela de 200 de distance l'unité est ignorée
                        if self.y >0: #ingore l'unité si elle est de l'autre coté du pont
                            if redCoordinates[id.index[bestID]][1]>0:
                                bestID=redId[i]
                        else:
                            if redCoordinates[id.index[bestID]][1]<0:
                                bestID=redId[i]

        target = bestID # le hit target est une variable fixe(sauf ici) ou elle donne l'ID de l'unité à cogner

        if bestID == 200:
            pass
            # >>> ici une fonction qui s'oriente vers le pont le plus proche
        else:
            pass
            # >>> ici fonction qui oriente vers l'ennemi
            # ALEXIS !! à parit du bestID (l'ID de l'unité la plus proche) et du jeu de coordonnées REDcoordonnée=[[REDx,REDy]] , fais en sorte que l'unité s'oriente vers les coordonnées de l'ennemi qui possede l'ID bestID




identification = 0
def id_creator():
    global identification
    identification+=1
    return identification










