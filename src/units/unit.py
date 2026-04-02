import json
import logging
import os

from constant import DEFINITIONS_PATH
from utils import log


class Unit:
    def __init__(self,name):
        self.name = name
        list_files=os.listdir(DEFINITIONS_PATH)
        self.file=None

        for file in list_files:
            if file.startswith(name):
                self.file = file
        self.verif()

        self.data=json.load(open(DEFINITIONS_PATH / self.file))
    def verif(self):
        if self.file is None:
            log.logger.send(f"Could not load unit {self.name}, file not found.", logging.ERROR)
            return
        else:
            log.logger.send(f"Loaded unit {self.name}", logging.DEBUG)


def load_units():#-> list[Unit]
    list_Units=[]
    for file in os.listdir(DEFINITIONS_PATH):
        if file.endswith(".json"):
            pass

