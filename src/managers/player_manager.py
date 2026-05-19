import logging

from constant import DECK_LENGTH, MAX_PLAYER_COUNT
from managers.player import Player
from utils import log

players: list[Player] = []


def add_player(camp, deck, elixir_start):
    if len(players) >= MAX_PLAYER_COUNT:
        log.logger.send("Cannot add player, reached max player count.", logging.ERROR)
        return

    for plr in players:
        if plr.camp == camp:
            log.logger.send(f"Cannot add player, side {camp} is already taken.", logging.ERROR)
            return

    if len(deck) < DECK_LENGTH:
        log.logger.send(f"Cannot add player, deck doesn't meet required length.", logging.ERROR)

    player = Player(camp, deck, elixir_start)
    players.append(player)
    log.logger.send(f"Registered player {camp}.", logging.DEBUG)

    return player


def get_player(camp) -> Player | None:
    for plr in players:
        if plr.camp == camp:
            return plr
    return None


def reset():
    global players
    players = []

    log.logger.send("Reset card decks.", logging.DEBUG)
