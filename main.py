# coding: utf-8
import pygame
import engine
import entities
import os

game = engine.Engine((1280, 800), framerate=100)

pygame.key.set_repeat(50, 1)

wall = engine.Carte(os.path.join("assets", "levels", "test"),
                    mode="load")  # objet carte

game = engine.Engine((wall.width, wall.height), framerate=50)  # fenêtre

back = wall.renderSurface()  # surface carte

p1 = entities.Player(0, 0, "1")  # joueur

while game.state != 0:
    events = game.runEvents()

    p1.movement(wall.get_rects(), events)

    game.screen.blit(back, (0, 0))

    p1.render(game.screen)

    game.waitFramerate(showFps=True)
