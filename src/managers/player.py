import logging

from constant import CARDS_PATH, TRACE
from core import asset
from utils import log
from utils.scale_card import scale_card


class Player:
    def __init__(self, camp, deck, elixir_start) -> None:
        self.camp = camp
        self.deck = [self._normalize_card_name(card) for card in deck]
        self.elixir = elixir_start
        self.deck_img = self._get_cards_img()
        self.hand = list(range(min(4, len(self.deck))))
        self.next_card_index = len(self.hand)

    @property
    def hand_cards(self):
        return [self.deck[index] for index in self.hand]

    @property
    def hand_img(self):
        return [self.deck_img[index] for index in self.hand]

    def _get_cards_img(self):
        cards = []
        for carte in self.deck:
            card = asset.get_image(CARDS_PATH / f"{carte}.png")
            if card:
                card = scale_card(card, 8, 6.5)
                cards.append(card)

        log.logger.send(f"Populated card images for player {self.camp}.", logging.DEBUG)
        return cards

    def modify_elixir(self, amount, log_change=True):
        self.elixir = max(0, min(10, self.elixir + amount))
        if log_change:
            log.logger.send(f"Modified elixir for player {self.camp} to {self.elixir:.2f}.", TRACE)

    def get_hand_card(self, hand_index):
        if hand_index >= len(self.hand):
            return None
        return self.deck[self.hand[hand_index]]

    def cycle_played_card(self, hand_index):
        if len(self.deck) <= len(self.hand) or hand_index >= len(self.hand):
            return

        self.hand[hand_index] = self.next_card_index
        self.next_card_index = (self.next_card_index + 1) % len(self.deck)

        while self.next_card_index in self.hand:
            self.next_card_index = (self.next_card_index + 1) % len(self.deck)

    @staticmethod
    def _normalize_card_name(card):
        if card.endswith(".png"):
            return card[:-4]
        return card
