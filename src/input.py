import logging

import pygame

from utils import log

controllers = {}

def register_controller(c_id):
    controller = pygame.joystick.Joystick(c_id)
    controller.init()
    controllers[c_id] = controller

    log.logger.send(f"Connected {controller.get_name()}")

def unregister_controller(joy_id):
    controllers.pop(joy_id, None)
    log.logger.send(f"Removed controller id {joy_id}")

def init():
    log.logger.send("Initializing input", logging.DEBUG)
    pygame.joystick.init()

    joystick_count = pygame.joystick.get_count()
    log.logger.send(f"Number of controllers connected: {joystick_count}", logging.DEBUG)

    for i in range(joystick_count-1):
        register_controller(i)


def handle_events(event):
    if event.type == pygame.JOYDEVICEADDED:
        register_controller(event.device_index)
    if event.type == pygame.JOYDEVICEREMOVED:
        unregister_controller(event.instance_id)

    handle_inputs(event)

def handle_inputs(event):
    if event.type == pygame.KEYDOWN:
        # Player 1 controls
        if event.key == pygame.K_LEFT:
            pass
        if event.key == pygame.K_RIGHT:
            pass
        if event.key == pygame.K_UP:
            pass
        if event.key == pygame.K_DOWN:
            pass
        if event.key == pygame.K_e:
            pass

        # Player 2 controls
        if event.key == pygame.K_q:
            pass
        if event.key == pygame.K_d:
            pass
        if event.key == pygame.K_z:
            pass
        if event.key == pygame.K_s:
            pass
        if event.key == pygame.K_RSHIFT:
            pass
        if event.key == pygame.K_EXCLAIM:
            pass

    # Controller controls
    if event.type == pygame.JOYBUTTONDOWN:
        print("Button pressed:", event.button)

    if event.type == pygame.JOYAXISMOTION:
        print("Axis moved:", event.axis, event.value)

    if event.type == pygame.JOYHATMOTION:
        print("D-pad:", event.value)