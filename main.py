# coding: utf-8
import pygame
import engine
import entities
import os

game = engine.Engine((1280, 800), framerate=100)

haut = pygame.image.load(os.path.join("assets", "haut.png"))
bas = pygame.image.load(os.path.join("assets", "bas.png"))
droite = pygame.image.load(os.path.join("assets", "droite.png"))
gauche = pygame.image.load(os.path.join("assets", "gauche.png"))

ptextures = [droite, bas, gauche, haut]

pygame.key.set_repeat(50, 1)

wall = engine.Carte(os.path.join("assets", "levels", "test"), mode="load")


game = engine.Engine((wall.width, wall.height), framerate=50)

back = wall.renderSurface()

p1 = entities.Player(0, 0, "1")

while game.state != 0:
    events = game.runEvents()

    p1.movement(wall.get_rects(), events)

    game.screen.blit(back, (0, 0))

    p1.render(game.screen)

    game.waitFramerate(showFps=True)
