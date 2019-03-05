import pygame
import main
import engine
game = engine.Engine((512, 288),
                     (1024, 576), framerate=50)  # fenêtre
game.state = 0

events = []
while game.state == 0:
    game.runEvents()
