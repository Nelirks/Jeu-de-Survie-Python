import engine
import entities
import pygame
import os
import sys
import math
pygame.init()


"""
Map editor : edit map
usage : python mapEditor.py <new-edit> <path> <width> <height>
"""

wall = 1
size = (1, 1)

terre = pygame.image.load(os.path.join('assets', "terre.png"))
eau = pygame.image.load(os.path.join('assets', "eau.png"))
foret = pygame.image.load(os.path.join('assets', "Foliage_dark32.png"))

textures = {
    "0": eau,
    "1": terre,
    "2": foret
}


def edit(argv):
    global wall
    global size
    path = argv[2]
    print("editing {} ".format(sys.argv[2]))
    wall = engine.Carte(path, mode="edit")
    size = (wall.width, wall.height)


def new(argv):
    global wall
    global size
    path = argv[2]
    size = (int(argv[3]), int(argv[4]))
    print("creating {} ".format(sys.argv[2]))
    wall = engine.Carte(path, mode="new", dimensions=size)


mode = {"edit": edit, "new": new}
mode[sys.argv[1]](sys.argv)
e = engine.Engine(
    (size[0]*wall.tileSize + wall.tileSize+2, size[1]*wall.tileSize))
pygame.display.set_caption("map editor", "ha")

r = wall.render(textures)
iTextures = 0
tindex = []
for i in textures:
    tindex.append(i)

imax = len(tindex)

w = wall.tileSize

while e.state:
    events = e.runEvents()
    for ev in events:
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x = math.floor(pos[0] / w)
            y = math.floor(pos[1] / w)
            print(x, y, iTextures, tindex[iTextures])
            wall.edit(x, y, tindex[iTextures])
            r = wall.render(textures)
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_s:
                wall.save()
                print("saved {}".format(wall.path))
            if ev.key == pygame.K_TAB:
                iTextures += 1
                if iTextures >= imax:
                    iTextures = 0
    e.screen.fill((0, 0, 0))
    e.screen.blit(r, (0, 0))

    y = 0
    for t in textures:
        e.screen.blit(textures[t], (e.width - wall.tileSize - 1, y))
        if y == iTextures * wall.tileSize:
            pygame.draw.rect(e.screen, (255, 255, 0), pygame.Rect(
                e.width-wall.tileSize - 1, y, wall.tileSize, wall.tileSize), 1)
        y += wall.tileSize

    e.waitFramerate(showFps=True)
    pygame.display.flip()
