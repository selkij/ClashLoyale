import json
import os


class Unit:
    def __init__(self,name):
        list_files=os.listdir("definitions")
        self.file=None
        for file in list_files:
            if file.startswith(name):
                self.file = file
        if self.file==None:
            raise ValueError("File not found:",name)
        else:
            print("File found success:",name)
        data=json.load(open("definitions/"+self.file))
        print(data)



            # Afficher les données pour vérifier le contenu

test1=Unit("pekka")
test2=Unit("mini_pekka")