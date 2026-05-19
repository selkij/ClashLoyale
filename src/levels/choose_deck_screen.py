import os

import pygame

import constant
from core import asset
from core.state import GameState
from levels.scene import Scene
from levels.widgets.button_widget import ButtonWidget
from utils import tracked_surface


current = 0
deck_blue_selection = []
deck_red_selection = []


class ChooseDeckScreen(Scene):
    def __init__(self, modules):
        super().__init__(modules)

        self.modules = modules
        self.ui = self.modules["ui"]
        self.state_manager = self.modules["state"]
        self.screen = self.ui.screen
        self.cartes = []

        self.ready_image = asset.get_image(constant.GUI_PATH / "ready.png").convert_alpha()
        self.ready_image = pygame.transform.scale(
            self.ready_image,
            (constant.SCREEN_WIDTH / 5.7, constant.SCREEN_HEIGHT / 13)
        )

        for file in sorted(os.listdir(constant.CARDS_PATH)):
            if file.endswith(".png"):
                image = asset.get_image(constant.CARDS_PATH / file).convert_alpha()
                image = pygame.transform.scale(image, (constant.SCREEN_WIDTH / 10.5, constant.SCREEN_HEIGHT / 9))
                self.cartes.append(tracked_surface.TrackedSurface(file, image))

    def start(self):
        super().start()

        global current
        current = 0
        deck_blue_selection.clear()
        deck_red_selection.clear()

        components = [
            ButtonWidget(
                self.modules,
                (self.screen.get_width() / 1.5, self.screen.get_width() / 1.2),
                self.ready_image,
                lambda _: self.ready()
            )
        ]

        x = 80
        y = 200
        for carte in self.cartes:
            if x > self.screen.get_width() - 150:
                x = 80
                y += 130

            components.append(ButtonWidget(
                self.modules,
                (x, y),
                carte.surface,
                lambda widget: self.ajout_carte(widget),
                id=carte.name
            ))

            x += 120

        for component in components:
            self.ui.add_component(component)

    def run(self):
        super().run()
        self._draw_status()
        self._draw_selected_cards()

    def ready(self):
        global current

        if current == 0:
            if len(deck_blue_selection) == constant.DECK_LENGTH:
                current = 1
            return

        if len(deck_red_selection) == constant.DECK_LENGTH:
            self.state_manager.set_state(GameState.GAME)

    def ajout_carte(self, widget):
        selected_deck = deck_blue_selection if current == 0 else deck_red_selection
        card_name = self._normalize_card_name(widget.id)

        if card_name in selected_deck:
            selected_deck.remove(card_name)
            return

        if len(selected_deck) < constant.DECK_LENGTH:
            selected_deck.append(card_name)

    def _draw_status(self):
        camp_name = "BLEU" if current == 0 else "ROUGE"
        selected_deck = deck_blue_selection if current == 0 else deck_red_selection
        color = constant.BLUE_COLOR if current == 0 else constant.RED_COLOR
        status = self.ui.font_medium.render(
            f"{camp_name} - {len(selected_deck)}/{constant.DECK_LENGTH}",
            True,
            color
        )
        self.ui.screen.blit(status, (85, 78))

        ready_text = "JOUEUR SUIVANT" if current == 0 else "COMMENCER"
        if len(selected_deck) < constant.DECK_LENGTH:
            ready_text = "DECK INCOMPLET"
        label = self.ui.font_small.render(ready_text, True, constant.TEXT_COLOR)
        self.ui.screen.blit(label, (self.screen.get_width() / 1.5, self.screen.get_width() / 1.2 - 34))

    def _draw_selected_cards(self):
        selected_deck = deck_blue_selection if current == 0 else deck_red_selection
        color = constant.BLUE_COLOR if current == 0 else constant.RED_COLOR

        for component in self.ui.components:
            if not isinstance(component, ButtonWidget) or component.id is None:
                continue

            if self._normalize_card_name(component.id) in selected_deck:
                pygame.draw.rect(
                    self.ui.screen,
                    color,
                    component.button_rect.inflate(8, 8),
                    width=4,
                    border_radius=8
                )

    @staticmethod
    def _normalize_card_name(card_name):
        if card_name.endswith(".png"):
            return card_name[:-4]
        return card_name
