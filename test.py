"""
teste les modules du jeu
"""

import os
import math
import pygame
import engine
import entities

print("init...")


show_fps = True


black = 0, 0, 0


haut = pygame.image.load(os.path.join('assets', "haut.png"))
bas = pygame.image.load(os.path.join('assets', "bas.png"))
droite = pygame.image.load(os.path.join('assets', "droite.png"))
gauche = pygame.image.load(os.path.join('assets', "gauche.png"))
terre = pygame.image.load(os.path.join('assets', "terre.png"))
eau = pygame.image.load(os.path.join('assets', "eau.png"))
foret = pygame.image.load(os.path.join(
    'assets', "Foliage_dark32.png"))

textures = {
    "0": eau,
    "1": terre,
    "2": foret
}


direction = [0, 0, 0, 0]


framerate = 50


m = engine.Carte(os.path.join("assets", "levels", "map1.mp"), textures,
                 mode="load")

size = width, height = m.width * m.tileSize, m.height*m.tileSize
g = engine.Engine(size)

myfont = pygame.font.SysFont("monospace", 15)
last = pygame.time.get_ticks()


wall = m.render(textures)


def waitf():
    global last
    while(pygame.time.get_ticks() - last < 1000/framerate):
        pass
    l = round(1000/(pygame.time.get_ticks() - last))

    last = pygame.time.get_ticks()
    return l


faces = [droite, bas, gauche, haut]  # textures

p1 = entities.Player(0, 0, faces)

w = m.tileSize

print("init done in {}ms".format(pygame.time.get_ticks()))
while g.state:
    fps = g.waitFramerate()
    events = g.runEvents()
    # Mouvements
    p1.update(events)
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x = math.floor(pos[0] / w)
            y = math.floor(pos[1] / w)
            try:
                s = int(m.grid[x][y])
                s += 1
                if s > 2:
                    s = 0
                m.grid[x][y] = str(s)
                wall = m.render()
            except:
                print("invalid place")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  # sauvegarde
                m.save()

    # affichage
    g.screen.fill(black)
    g.screen.blit(wall, (0, 0))
    p1.render(g.screen)
    if show_fps:
        label = myfont.render(str(fps), 1, (0, 255, 0))
        g.screen.blit(label, (width-40, 0))
    pygame.display.flip()


print("goodbye")
pygame.quit()  # dernière opération : décharger pygame
