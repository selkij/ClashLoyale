import os
import json

class Unit:
    def __init__(self,name):
        list_files=os.listdir("definitions")
        for file in list_files:
            if file.startswith(name):
                self.fichier=file
        with open(self.fichier, 'r', encoding='utf-8'):
            donnees = json.load(str(self.fichier))

        # Afficher les données pour vérifier le contenu
        print(donnees)

test1=Unit("pekka")
test2=Unit("esprit_de_glace")
print(test1.fichier)
print(test2.fichier)