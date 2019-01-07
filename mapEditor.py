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

r = pygame.Surface(
    (wall.width*wall.tileSize, wall.height*wall.tileSize))
wall.render(r)
iTextures = 0
tindex = []
for i in wall.textures:
    tindex.append(i)

imax = len(tindex)

w = wall.tileSize
e.screen.blit(r, (0, 0))


def show():
    wall.render(r)
    e.screen.blit(r, (0, 0))
    y = 0
    for t in wall.textures:
        e.screen.blit(wall.textures[t], (e.width - wall.tileSize - 1, y))
        if y == iTextures * wall.tileSize:
            pygame.draw.rect(e.screen, (255, 255, 0), pygame.Rect(
                e.width-wall.tileSize - 1, y, wall.tileSize, wall.tileSize), 1)
        y += wall.tileSize
    pygame.display.flip()


show()

while e.state:
    events = e.runEvents()
    for ev in events:
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x = math.floor(pos[0] / w)
            y = math.floor(pos[1] / w)
            print(x, y, iTextures, tindex[iTextures])
            try:
                wall.edit(x, y, tindex[iTextures])
            except:
                print("invalid location")
            show()

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_s:
                wall.save()
                print("saved {}".format(wall.path))
            if ev.key == pygame.K_TAB:
                iTextures += 1
                if iTextures >= imax:
                    iTextures = 0
                show()

    e.waitFramerate(showFps=False)
