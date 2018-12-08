"""
teste les modules du jeu
"""

import os
import math
import pygame
import engine
import entities

pygame.init()
print("init...")


show_fps = True
w = 64


myfont = pygame.font.SysFont("monospace", 15)


size = width, height = 1280, 960


black = 0, 0, 0

screen = pygame.display.set_mode(size)


haut = pygame.image.load(os.path.join('assets', "haut.png"))
bas = pygame.image.load(os.path.join('assets', "bas.png"))
droite = pygame.image.load(os.path.join('assets', "droite.png"))
gauche = pygame.image.load(os.path.join('assets', "gauche.png"))
terre = pygame.image.load(os.path.join('assets', "terre.png"))
eau = pygame.image.load(os.path.join('assets', "eau.png"))
foret = pygame.image.load(os.path.join('assets', "foret.png"))

textures = {
    "0": eau,
    "1": terre,
    "2": foret
}


direction = [0, 0, 0, 0]


framerate = 50

m = engine.Carte(os.path.join("assets", "levels", "map1.mp"),
                 mode="edit", dimensions=(int(width//w), int(height//w)))

state = 1

last = pygame.time.get_ticks()


wall = m.render(textures)


def waitf():
    global last
    while(pygame.time.get_ticks() - last < 1000/framerate):
        pass
    l = round(1000/(pygame.time.get_ticks() - last))

    last = pygame.time.get_ticks()
    return l


Pspeed = 5

faces = [droite, bas, gauche, haut]  # textures

p1 = entities.Player(0, 0, faces)


def findDirection(direction, last):
    i = 0
    l = last
    for d in direction:
        if d == 1:
            l = i
        i += 1
    return l


print("init done in {}ms".format(pygame.time.get_ticks()))
while state:
    fps = waitf()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x = math.floor(pos[0] / w)
            y = math.floor(pos[1] / w)
            s = int(m.grid[x][y])
            s += 1
            if s > 2:
                s = 0
            m.grid[x][y] = str(s)
            wall = m.render(textures)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  # sauvegarde
                m.save()
            # Mouvements
            if event.key == pygame.K_LEFT:
                p1.setFace(entities.PlayerFaces["left"])
                direction[2] = 1
            if event.key == pygame.K_UP:
                p1.setFace(entities.PlayerFaces["up"])
                direction[3] = 1
            if event.key == pygame.K_DOWN:
                p1.setFace(entities.PlayerFaces["down"])
                direction[1] = 1
            if event.key == pygame.K_RIGHT:
                p1.setFace(entities.PlayerFaces["right"])
                direction[0] = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                direction[2] = 0
                p1.setFace(findDirection(direction, 2))
            if event.key == pygame.K_UP:
                direction[3] = 0
                p1.setFace(findDirection(direction, 3))
            if event.key == pygame.K_DOWN:
                direction[1] = 0
                p1.setFace(findDirection(direction, 1))
            if event.key == pygame.K_RIGHT:
                direction[0] = 0
                p1.setFace(findDirection(direction, 0))
        if event.type == pygame.QUIT:  # quitter quand on ferme la fenêtre
            state = 0

    # applique les mouvements
    if direction[0] == 1:
        p1.x += Pspeed
    if direction[2] == 1:
        p1.x -= Pspeed
    if direction[1] == 1:
        p1.y += Pspeed
    if direction[3] == 1:
        p1.y -= Pspeed
    # affichage
    screen.fill(black)
    screen.blit(wall, (0, 0))
    p1.render(screen)
    if show_fps:
        label = myfont.render(str(fps), 1, (0, 255, 0))
        screen.blit(label, (width-40, 0))
    pygame.display.flip()
