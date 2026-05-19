import pygame

from constant import BLUE_COLOR, ELIXIR_COLOR, GUI_PATH, RED_COLOR, SCREEN_HEIGHT, SCREEN_WIDTH, SPRITES_PATH
from core import asset
from core.state import GameState
from levels.scene import Scene
from levels.choose_deck_screen import deck_blue_selection, deck_red_selection
from managers import player_manager
from managers.unit_manager import UnitManager
from mechanics.systeme_elixir import ElixirSystem, START_ELIXIR


CAMP_TO_UNIT_CAMP = {
    "bleu": "blue",
    "rouge": "red",
}


def draw_player_bars(screen, bar_width):
    pygame.draw.rect(screen, BLUE_COLOR, pygame.Rect(0, 0, bar_width, SCREEN_HEIGHT))
    pygame.draw.rect(screen, RED_COLOR, pygame.Rect(SCREEN_WIDTH - bar_width, 0, bar_width, SCREEN_HEIGHT))


def draw_decks(screen, blue_player, red_player, start_y, y_offset, selected_cards):
    y = start_y
    card_rects = []

    for i in range(4):
        if i >= len(blue_player.hand_img) or i >= len(red_player.hand_img):
            break

        card_blue = blue_player.hand_img[i]
        card_red = red_player.hand_img[i]
        blue_rect = card_blue.get_rect(topleft=(50, y))
        red_rect = card_red.get_rect(topleft=(SCREEN_WIDTH - 175, y))

        screen.blit(card_blue, blue_rect)
        screen.blit(card_red, red_rect)

        if selected_cards.get("bleu") == i:
            pygame.draw.rect(screen, BLUE_COLOR, blue_rect.inflate(8, 8), width=4, border_radius=8)
        if selected_cards.get("rouge") == i:
            pygame.draw.rect(screen, RED_COLOR, red_rect.inflate(8, 8), width=4, border_radius=8)

        card_rects.append(("bleu", i, blue_rect))
        card_rects.append(("rouge", i, red_rect))

        y += y_offset

    return card_rects


def draw_elixir_bars(screen, elixir_bar, font, blue_x, red_x, y_offset):
    blue_elixir = player_manager.get_player("bleu").elixir
    red_elixir = player_manager.get_player("rouge").elixir

    bar_size = elixir_bar.get_size()

    blue_fill = pygame.Rect(blue_x, y_offset, bar_size[0], bar_size[1] / 10 * blue_elixir)
    red_fill = pygame.Rect(red_x, y_offset, bar_size[0], bar_size[1] / 10 * red_elixir)
    blue_fill.bottom = y_offset + bar_size[1]
    red_fill.bottom = y_offset + bar_size[1]

    pygame.draw.rect(screen, ELIXIR_COLOR, blue_fill)
    pygame.draw.rect(screen, ELIXIR_COLOR, red_fill)

    screen.blit(elixir_bar, (blue_x, y_offset))  # Blue elixir bar
    screen.blit(elixir_bar, (red_x, y_offset))  # Red elixir bar

    blue_text = font.render(str(int(blue_elixir)), True, "#FFFFFF")
    red_text = font.render(str(int(red_elixir)), True, "#FFFFFF")
    screen.blit(blue_text, blue_text.get_rect(center=(blue_x + bar_size[0] / 2, y_offset + bar_size[1] + 26)))
    screen.blit(red_text, red_text.get_rect(center=(red_x + bar_size[0] / 2, y_offset + bar_size[1] + 26)))


class Arena(Scene):
    def __init__(self, modules: dict):
        super().__init__(modules)  # Initializes the scene

        self.modules = modules
        self.state_manager = modules["state"]
        self.input = modules["input"]
        self.ui = modules["ui"]
        self.sound = modules["sound"]

        self.arena = asset.get_image(SPRITES_PATH / "arena.png")
        self.arena_size = self.arena.get_size()
        self.arena_ratio = SCREEN_HEIGHT / self.arena_size[1]
        self.arena = pygame.transform.scale(self.arena, (int(self.arena_size[0] * self.arena_ratio), SCREEN_HEIGHT))
        self.arena_size = self.arena.get_size()  # Gets new scaled size.
        self.arena_pos = (SCREEN_WIDTH / 2 - self.arena_size[0] / 2, 0)
        self.arena_rect = self.arena.get_rect(topleft=self.arena_pos)

        self.elixir_bar = asset.get_image(GUI_PATH / "elixir_bar.png")
        self.elixir_bar_size = self.elixir_bar.get_size()

        self.blue_plr = None
        self.red_plr = None
        self.unit_manager = None
        self.elixir_system = ElixirSystem()
        self.selected_cards = {"bleu": 0, "rouge": 0}
        self.cursors = {}
        self.card_rects = []
        self.mouse_was_pressed = False
        self.key_edges = set()
        self.controller_button_edges = {}
        self.last_update_ms = pygame.time.get_ticks()

    def start(self):
        super().start()

        player_manager.reset()

        test_red = ['tasty_crousty', 'x_bow', 'knight', 'pekka', 'prince', 'sapeur', 'zap', 'zappy']
        test_blue = ['canon', 'mini_pekka', 'rage', 'fireball', 'dart_goblin', 'giant', 'hogrider', 'log']
        red_deck = deck_red_selection if len(deck_red_selection) >= 8 else test_red
        blue_deck = deck_blue_selection if len(deck_blue_selection) >= 8 else test_blue

        self.red_plr = player_manager.add_player("rouge", red_deck, START_ELIXIR)
        self.blue_plr = player_manager.add_player("bleu", blue_deck, START_ELIXIR)
        self.unit_manager = UnitManager(self.arena_rect)
        self.unit_manager.set_players(self.blue_plr, self.red_plr)
        self.unit_manager.spawn_default_towers()
        self.elixir_system.reset()
        self.selected_cards = {"bleu": 0, "rouge": 0}
        self.cursors = {
            "bleu": pygame.Vector2(self.arena_rect.centerx - 90, self.arena_rect.centery + 160),
            "rouge": pygame.Vector2(self.arena_rect.centerx + 90, self.arena_rect.centery - 160),
        }
        self.mouse_was_pressed = False
        self.key_edges = set()
        self.controller_button_edges = {}
        self.last_update_ms = pygame.time.get_ticks()

        bar_width = 15

        self.sound.clear_sounds()
        self.sound.play_sound("combat.mp3", 2500, True)

    def run(self):
        super().run()

        now = pygame.time.get_ticks()
        dt = (now - self.last_update_ms) / 1000
        self.last_update_ms = now

        self._handle_keyboard_input(dt)
        self._handle_controller_input(dt)
        self.elixir_system.update(dt, [self.blue_plr, self.red_plr])

        self.ui.screen.blit(self.arena, self.arena_pos)
        self.unit_manager.update(dt)
        self.unit_manager.draw(self.ui.screen)
        self._check_game_over()

        draw_player_bars(self.ui.screen, 15)
        self.card_rects = draw_decks(
            self.ui.screen,
            self.blue_plr,
            self.red_plr,
            150,
            175,
            self.selected_cards
        )
        draw_elixir_bars(self.ui.screen,
                         self.elixir_bar,
                         self.ui.font_small,
                         SCREEN_WIDTH / 2 - self.arena_size[0] / 2 - 40,
                         SCREEN_WIDTH / 2 + self.arena_size[0] / 2 + 20,
                         SCREEN_HEIGHT / 2 - self.elixir_bar_size[1] / 2
                         )
        self._handle_placement_input()
        self._draw_cursors()
        self._draw_placement_preview()
        self._draw_elixir_multiplier()

    def _handle_placement_input(self):
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if not mouse_pressed or self.mouse_was_pressed:
            self.mouse_was_pressed = mouse_pressed
            return

        mouse_pos = self.ui.get_mouse_pos()
        for camp, card_index, rect in self.card_rects:
            if rect.collidepoint(mouse_pos):
                self.selected_cards[camp] = card_index
                self.mouse_was_pressed = mouse_pressed
                return

        if self.arena_rect.collidepoint(mouse_pos):
            camp = "bleu" if mouse_pos[1] >= self.arena_rect.centery else "rouge"
            self._place_selected_card(camp, mouse_pos)

        self.mouse_was_pressed = mouse_pressed

    def _handle_keyboard_input(self, dt):
        keys = pygame.key.get_pressed()
        speed = 420 * dt

        self._move_cursor_from_vector("bleu", self._keyboard_vector(keys, pygame.K_q, pygame.K_d, pygame.K_z, pygame.K_s), speed)
        self._move_cursor_from_vector("rouge", self._keyboard_vector(keys, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN), speed)

        self._select_card_on_key(keys, pygame.K_1, "bleu", 0)
        self._select_card_on_key(keys, pygame.K_2, "bleu", 1)
        self._select_card_on_key(keys, pygame.K_3, "bleu", 2)
        self._select_card_on_key(keys, pygame.K_4, "bleu", 3)
        self._select_card_on_key(keys, pygame.K_KP1, "rouge", 0)
        self._select_card_on_key(keys, pygame.K_KP2, "rouge", 1)
        self._select_card_on_key(keys, pygame.K_KP3, "rouge", 2)
        self._select_card_on_key(keys, pygame.K_KP4, "rouge", 3)

        if self._key_pressed_once(keys, pygame.K_SPACE):
            self._place_selected_card("bleu", self.cursors["bleu"])
        if self._key_pressed_once(keys, pygame.K_RSHIFT):
            self._place_selected_card("rouge", self.cursors["rouge"])

        self.key_edges = {index for index, pressed in enumerate(keys) if pressed}

    def _handle_controller_input(self, dt):
        speed = 460 * dt
        controllers = list(self.input.controllers.values())

        for index, controller in enumerate(controllers[:2]):
            camp = "bleu" if index == 0 else "rouge"
            vector = pygame.Vector2(0, 0)

            if controller.get_numaxes() >= 2:
                axis_x = controller.get_axis(0)
                axis_y = controller.get_axis(1)
                if abs(axis_x) > 0.18:
                    vector.x += axis_x
                if abs(axis_y) > 0.18:
                    vector.y += axis_y

            if controller.get_numhats() > 0:
                hat_x, hat_y = controller.get_hat(0)
                vector.x += hat_x
                vector.y -= hat_y

            self._move_cursor_from_vector(camp, vector, speed)
            self._handle_controller_buttons(controller, camp)

    def _handle_controller_buttons(self, controller, camp):
        instance_id = controller.get_instance_id()
        pressed_buttons = {
            button for button in range(controller.get_numbuttons())
            if controller.get_button(button)
        }
        previous_buttons = self.controller_button_edges.get(instance_id, set())
        new_buttons = pressed_buttons - previous_buttons

        for card_index in range(4):
            if card_index in new_buttons:
                self.selected_cards[camp] = card_index

        if 4 in new_buttons:
            self._cycle_selected_card(camp, -1)
        if 5 in new_buttons:
            self._cycle_selected_card(camp, 1)
        if 0 in new_buttons:
            self._place_selected_card(camp, self.cursors[camp])

        self.controller_button_edges[instance_id] = pressed_buttons

    def _place_selected_card(self, camp, position):
        card_index = self.selected_cards[camp]
        player = self._get_player(camp)
        unit_name = player.get_hand_card(card_index)
        if unit_name is None:
            return
        definition = self.unit_manager.get_definition(unit_name)
        if definition is None:
            return

        if not self._can_place(camp, definition, position):
            return

        elixir_cost = definition.get("elixir_cost", 0)
        if player.elixir < elixir_cost:
            return

        player.modify_elixir(-elixir_cost)
        self.unit_manager.play_card(unit_name, CAMP_TO_UNIT_CAMP[camp], position)
        player.cycle_played_card(card_index)
        self.selected_cards[camp] = min(self.selected_cards[camp], len(player.hand_cards) - 1)

    def _can_place(self, camp, definition, position):
        if not self.arena_rect.collidepoint(position):
            return False

        if definition.get("type") == "spell":
            return True

        if camp == "bleu":
            return position[1] >= self.arena_rect.centery
        return position[1] <= self.arena_rect.centery

    def _draw_placement_preview(self):
        mouse_pos = self.ui.get_mouse_pos()
        if not self.arena_rect.collidepoint(mouse_pos):
            return

        camp = "bleu" if mouse_pos[1] >= self.arena_rect.centery else "rouge"
        card_index = self.selected_cards[camp]
        player = self._get_player(camp)
        unit_name = player.get_hand_card(card_index)
        if unit_name is None:
            return
        definition = self.unit_manager.get_definition(unit_name)
        if definition is None:
            return

        valid = self._can_place(camp, definition, mouse_pos) and player.elixir >= definition.get("elixir_cost", 0)
        color = (90, 230, 120) if valid else (240, 75, 65)
        pygame.draw.circle(self.ui.screen, color, mouse_pos, 18, width=3)

        label = self.ui.font_small.render(
            f"{unit_name} - {definition.get('elixir_cost', 0)}",
            True,
            color
        )
        self.ui.screen.blit(label, (mouse_pos[0] + 22, mouse_pos[1] - 16))

    def _draw_cursors(self):
        for camp, cursor in self.cursors.items():
            player = self._get_player(camp)
            card_index = self.selected_cards[camp]

            unit_name = player.get_hand_card(card_index)
            if unit_name is None:
                continue
            definition = self.unit_manager.get_definition(unit_name)
            if definition is None:
                continue

            valid = self._can_place(camp, definition, cursor) and player.elixir >= definition.get("elixir_cost", 0)
            color = BLUE_COLOR if camp == "bleu" else RED_COLOR
            if not valid:
                color = (240, 75, 65)

            pygame.draw.circle(self.ui.screen, color, cursor, 22, width=3)
            pygame.draw.line(self.ui.screen, color, (cursor.x - 12, cursor.y), (cursor.x + 12, cursor.y), width=2)
            pygame.draw.line(self.ui.screen, color, (cursor.x, cursor.y - 12), (cursor.x, cursor.y + 12), width=2)

    def _draw_elixir_multiplier(self):
        label = self.ui.font_small.render(f"x{self.elixir_system.multiplier}", True, ELIXIR_COLOR)
        self.ui.screen.blit(label, label.get_rect(center=(SCREEN_WIDTH / 2, 32)))

    def _keyboard_vector(self, keys, left, right, up, down):
        vector = pygame.Vector2(0, 0)
        if keys[left]:
            vector.x -= 1
        if keys[right]:
            vector.x += 1
        if keys[up]:
            vector.y -= 1
        if keys[down]:
            vector.y += 1
        return vector

    def _move_cursor_from_vector(self, camp, vector, speed):
        if vector.length_squared() == 0:
            return

        self.cursors[camp] += vector.normalize() * speed
        self.cursors[camp].x = max(self.arena_rect.left + 20, min(self.arena_rect.right - 20, self.cursors[camp].x))
        self.cursors[camp].y = max(self.arena_rect.top + 20, min(self.arena_rect.bottom - 20, self.cursors[camp].y))

    def _select_card_on_key(self, keys, key, camp, card_index):
        if self._key_pressed_once(keys, key):
            self.selected_cards[camp] = card_index

    def _key_pressed_once(self, keys, key):
        return keys[key] and key not in self.key_edges

    def _cycle_selected_card(self, camp, offset):
        player = self._get_player(camp)
        visible_cards = min(4, len(player.hand_cards))
        if visible_cards == 0:
            return
        self.selected_cards[camp] = (self.selected_cards[camp] + offset) % visible_cards

    def _check_game_over(self):
        winner = self.unit_manager.get_winner()
        if winner is None:
            return

        self.state_manager.winner = winner
        self.state_manager.set_state(GameState.END_GAME)

    def _get_player(self, camp):
        if camp == "bleu":
            return self.blue_plr
        return self.red_plr
