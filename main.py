# coding: utf-8
import pygame
import engine
import entities
import os

game = engine.Engine((1280, 800), framerate=100)
monitorResolution = game.initialMonitorresolution
pygame.key.set_repeat(50, 1)

wall = engine.Carte(os.path.join("assets", "levels", "test"),
                    mode="load")  # objet carte
# résolution du rendu :512*288
# résolution cible : 1024*576
game = engine.Engine((512, 288),
                     (1024, 576), framerate=50)  # fenêtre
game.initialMonitorresolution = monitorResolution
back = wall.renderSurface()  # surface carte
p1 = entities.Player(0, 0, "1")  # joueur


def mainLoop():
    events = []
    while game.state != 0:

        p1.movement(wall.get_rects(), events)

        game.screen.blit(back, (0, 0))

        p1.render(game.screen)

        game.waitFramerate(showFps=True)

        events = game.runEvents()  # en fin de boucle pour éviter les conflicts

mainLoop()
