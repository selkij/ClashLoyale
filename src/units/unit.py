import json
import os


class Unit:
    def __init__(self,name):
        list_files=os.listdir("definitions")
        for file in list_files:
            if file.startswith(name):
                self.file = file
        with open(self.file, 'r', encoding='utf-8'):
            data = json.load(self.file)

            # Afficher les données pour vérifier le contenu
            print(data)

test1=Unit("pekka")
test2=Unit("esprit_de_glace")
print(test1.file)
print(test2.file)
