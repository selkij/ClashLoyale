import logging

import pygame
from pygame.event import Event

from utils import log


def pass_f():  # Placeholder function
    pass


def pass_f_c(device):  # Placeholder controller function
    print(f"Controller {device.get_name()} pressed smth")


keymap_p1 = {
    pygame.K_q: pass_f,
    pygame.K_d: pass_f,
    pygame.K_z: pass_f,
    pygame.K_s: pass_f,
    pygame.K_SPACE: pass_f,  # Use
    pygame.K_e: pass_f,  # Taunt
}

keymap_p2 = {
    pygame.K_LEFT: pass_f,
    pygame.K_RIGHT: pass_f,
    pygame.K_UP: pass_f,
    pygame.K_DOWN: pass_f,
    pygame.K_RSHIFT: pass_f,  # Use
    pygame.K_EXCLAIM: pass_f,  # Taunt
}

controller_keymap = {
    13: pass_f_c,  # Left
    14: pass_f_c,  # Right
    11: pass_f_c,  # Up
    12: pass_f_c,  # Down
    0: pass_f_c,  # Use
    3: pass_f_c  # Taunt
}


class Input:
    def __init__(self):
        self.controllers = {}

        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()

        log.logger.send("Initialized input")
        log.logger.send(f"Got {joystick_count} controllers", logging.DEBUG)

        for i in range(joystick_count - 1):
            self.register_controller(i)

    def register_controller(self, c_id):
        controller = pygame.joystick.Joystick(c_id)
        controller.init()
        self.controllers[c_id] = controller

        log.logger.send(f"Connected {controller.get_name()}")

    def unregister_controller(self, joy_id):
        self.controllers.pop(joy_id, pass_f)
        log.logger.send(f"Removed controller id {joy_id}")

    def handle_input_events(self, event: pygame.event.Event):
        match event.type:
            case pygame.JOYDEVICEADDED:
                self.register_controller(event.device_index)
            case pygame.JOYDEVICEREMOVED:
                self.unregister_controller(event.instance_id)

        if event.type == pygame.KEYDOWN:
            action = keymap_p1.get(event.key) or keymap_p2.get(event.key)
            if action:
                action()

        # Controller controls
        if event.type == pygame.JOYBUTTONDOWN:
            action = controller_keymap.get(event.button)
            if action:
                action(self.controllers[event.instance_id])

    def process(self, events: list[Event]):
        for event in events:
            pass

# See https://github.com/DaFluffyPotato/notquiteparadise/blob/758d8310413316abbee8e7e644ac7dd005b05cf8/scripts/nqp/processors/input.py#L18
