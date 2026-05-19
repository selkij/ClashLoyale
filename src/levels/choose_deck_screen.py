import constant
import pygame
import os
import logging

from core.state import GameState
from utils import tracked_surface
from core import asset
from utils import log
from levels.widgets.button_widget import ButtonWidget
from levels.scene import Scene
current=0 #  0 = au joueur bleu de choisir , 1 = au joueur rouge de choisir

deck_blue_selection=[]
deck_red_selection=[]

class ChooseDeckScreen(Scene):
    def __init__(self, modules):
        super().__init__(modules) # Initializes the scene

        self.modules = modules
        self.ui = self.modules["ui"]
        self.state_manager = self.modules["state"]
        self.screen = self.ui.screen
        self.cartes=[]

        self.ready_image = asset.get_image(constant.GUI_PATH / "ready.png").convert_alpha()
        self.ready_image = pygame.transform.scale(self.ready_image, (constant.SCREEN_WIDTH / 5.7, constant.SCREEN_HEIGHT / 13))


        for file in os.listdir(constant.CARDS_PATH):
            if file.endswith(".png"):
                image = asset.get_image(constant.CARDS_PATH / file).convert_alpha()
                image = pygame.transform.scale(image, (constant.SCREEN_WIDTH / 10.5, constant.SCREEN_HEIGHT / 9))
                self.cartes.append(tracked_surface.TrackedSurface(file,image))
    

    def start(self):
        super().start()

        x=80
        y=200
        
        components = [
            ButtonWidget(
                self.modules,
                (self.screen.get_width() / 1.5, self.screen.get_width() / 1.2),
                self.ready_image,
                lambda _: self.state_manager.set_state(GameState.GAME)
            )
        ]

        for carte in self.cartes:
            if x > self.screen.get_width() - 150:
                x=80
                y+=130
            
            components.append(ButtonWidget(
                self.modules,
                (x,y),
                carte.surface,
                lambda widget: self.ajout_carte(widget),
                id=carte.name
            ))

            x+=120
            
        for component in components:
            self.ui.add_component(component)
        

        self.screen.blit(self.ready_image, (self.screen.get_width() / 1.5, self.screen.get_width() / 1.2))

        self.blue_choose_deck = asset.get_image(constant.GUI_PATH / "blue_choose_deck.png").convert_alpha()
        self.blue_choose_deck = pygame.transform.scale(self.blue_choose_deck, (constant.SCREEN_WIDTH/1.6, constant.SCREEN_HEIGHT/28))
        self.ui.screen.blit(self.blue_choose_deck,(85,80))

    def full_deck():
        return len(deck_blue_selection) == 8


    def run(self):  
        super().run()


    def ajout_carte(self, widget):
        if current==0:
            if widget.id in deck_blue_selection:
                print("carte pop")
                del deck_blue_selection[deck_blue_selection.index(widget.id)]
            else :
                if len(deck_blue_selection) < 8:
                    print("carte add")
                    deck_blue_selection.append(widget.id)
                else:
                    print("deck full")
            print(deck_blue_selection)
        else:
            if widget.id in deck_red_selection:
                print("carte pop")
                del deck_red_selection[deck_red_selection.index(widget.id)]
            else :
                if len(deck_red_selection) < 8:
                    print("carte add")
                    deck_red_selection.append(widget.id)
                else:
                    print("deck full")
            print(deck_red_selection)
    

