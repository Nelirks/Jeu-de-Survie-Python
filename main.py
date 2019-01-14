import pygame
import engine
import entities
import os

game = engine.Engine((1280, 800))

haut = pygame.image.load(os.path.join("assets", "haut.png"))
bas = pygame.image.load(os.path.join("assets", "bas.png"))
droite = pygame.image.load(os.path.join("assets", "droite.png"))
gauche = pygame.image.load(os.path.join("assets", "gauche.png"))

ptextures = [droite, bas, gauche, haut]


wall = engine.Carte(os.path.join("assets", "levels", "test"), mode="load")


game = engine.Engine((wall.width, wall.height))

back = wall.renderSurface()


p1 = entities.Player(0, 0, ptextures)

while game.state != 0:
    events = game.runEvents()
    game.screen.blit(back, (0, 0))

    game.waitFramerate()
