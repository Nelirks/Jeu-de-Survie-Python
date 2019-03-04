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

                     (wall.width*2, wall.height*2), framerate=50)  # fenêtre
game.initialMonitorresolution = monitorResolution
game = engine.Engine((wall.width, wall.height),
back = wall.renderSurface()  # surface carte

p1 = entities.Player(0, 0, "1")  # joueur
events = []
while game.state != 0:

    p1.movement(wall.get_rects(), events)

    game.screen.blit(back, (0, 0))

    p1.render(game.screen)

    game.waitFramerate(showFps=True)

    events = game.runEvents()  # en fin de boucle pour éviter les conflicts
