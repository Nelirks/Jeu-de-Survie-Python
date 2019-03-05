# coding: utf-8
import engine
import entities
import pygame
import os
import sys
import math


"""
Map editor : edit map
usage : python mapEditor.py
"""


def mapEditor(carte):
    e = engine.Engine((10, 10))

    ws = carte.tileSize  # réserve solide
    we = carte.tileSize*2  # réserve entités
    y = 0
    height = carte.height
    if carte.height < carte.tileSize * 5:
        height = carte.tileSize * 5

    for t in carte.textures:  # déterminer le nombre de colonnes
        if y >= height:
            ws += carte.tileSize
            y = 0
        y += carte.tileSize

    # déterminer le nombre de colonnes (entités)
    for t in entities.entitiesList:
        if y >= height:
            we += carte.tileSize*2
            y = 0
        y += carte.tileSize*2
    e = engine.Engine((carte.width+ws + we, height),
                      ((carte.width+ws + we)*2, height*2))
    textures = carte.textures
    entites = entities.entitiesList
    Selected = 0
    entitySelected = 0
    tindex = []
    entityIndex = []
    maxSindex = len(textures)
    maxEindex = len(entities.entitiesList)

    for t in carte.textures:
        tindex.append(t)
    for en in entities.entitiesList:
        entityIndex.append(en)
    cs = pygame.surface.Surface((carte.width, carte.height))
    carte.render(cs)
    e.screen.blit(cs, (0, 0))
    etextures = dict()
    for en in entites:
        etextures[en] = pygame.image.load(
            os.path.join("assets", "entities", en+".png"))

    while e.state != 0:
        events = e.runEvents()
        for ev in events:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_s:
                    carte.save()
                    print("saved {}".format(carte.path))
                if ev.key == pygame.K_TAB:
                    Selected += 1
                    if Selected >= maxSindex:
                        Selected = 0
                if ev.key == pygame.K_CAPSLOCK:
                    entitySelected += 1
                    if entitySelected >= maxEindex:
                        entitySelected = 0
            if ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                p = pygame.mouse.get_pressed()
                if p[0]:
                    y = math.floor(pos[1] / (carte.tileSize*2))
                    x = math.floor(pos[0] / (carte.tileSize*2))
                    try:
                        carte.edit(x, y, tindex[Selected])
                    except:
                        print("invalid location")
                    carte.render(cs)
                if p[1]:
                    y = pos[1] // 2
                    x = pos[0] // 2
                    listeEntites = carte.entities
                    rectSouris = pygame.rect.Rect(x, y, 1, 1)
                    i = 0
                    for entity in listeEntites:
                        if rectSouris.colliderect(entity.rect):
                            del carte.entities[i]
                        i += 1
                    carte.render(cs)

                if p[2]:
                    carte.entities.append(
                        entities.entitiesList[entityIndex[entitySelected]](pos[0]//2, pos[1]//2))
                    carte.render(cs)
                e.screen.blit(cs, (0, 0))
        y = 0
        x = carte.width

        for t in textures:
            if y >= height:
                y = 0
                x += carte.tileSize
            e.screen.blit(textures[t], (x, y))
            if tindex[Selected] == t:
                pygame.draw.rect(e.screen, (255, 0, 0), pygame.Rect(
                    x, y, carte.tileSize, carte.tileSize), 1)

            y += carte.tileSize
        y = 0
        x += carte.tileSize
        for en in entites:
            if y >= height:
                y = 0
                x += carte.tileSize*2
            e.screen.blit(etextures[en], (x, y))
            if entityIndex[entitySelected] == en:
                pygame.draw.rect(e.screen, (255, 225, 0), pygame.Rect(
                    x, y, carte.tileSize*2, carte.tileSize*2), 1)

        e.waitFramerate()


carte = 0
valide = 0
path = os.path.join("assets", "levels")
mode = ""
setNum = -1
tileset = []
dimensions = [1, 1]

print("Éditeur de cartes, entrez le nom de la carte.")
valide = 0
while valide != 1:
    choix = input("nom : ")
    valide = 1
path = os.path.join(path, choix)
valide = 0

print("Entrez le mode : \n  edit : charger une carte existante et la modifier \n  new: créer une nouvelle carte vide")
while valide != 1:

    mode = input("mode : ")
    if mode == "new" or mode == "edit":
        valide = 1
if mode == "new":

    valide = 0
    while valide == 0:
        try:
            dimensions = input("dimensions (ex : 10 10) : ")
            dimensions = dimensions.split()
            dimensions = [int(dimensions[0]), int(dimensions[1])]
            valide = 1
        except:
            print("entrée invalide")
            valide = 0
    valide = 0
    while valide == 0:
        setNum = input("nom du set : ")
        if setNum == "-1":
            print("ce numéro de set est interdit")
        else:
            valide = 1
    e = engine.Engine((10, 10))
    carte = engine.Carte(
        path, mode="new", dimensions=dimensions, setNum=setNum)
    mapEditor(carte)
elif mode == "edit":
    setNum = input("nom du set (-1 pour garder l'ancien) : ")
    e = engine.Engine((10, 10))
    carte = engine.Carte(
        path, mode="edit", setNum=setNum)
    mapEditor(carte)

valide = 0
pygame.quit()
choix = ""
while valide == 0:
    choix = input("Sauvegarder ? (o/n) : ").capitalize()
    if choix == "O" or choix == "N":
        valide = 1
        if choix == "O":
            carte.save()


"""
old code

wall = 1
size = (1, 1)
tileset = []
setNum = -1


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


def load(argv):
    global wall
    global size
    path = argv[2]
    print("editing {} ".format(sys.argv[2]))
    wall = engine.Carte(path, mode="edit")
    size = (wall.width, wall.height)


mode = {"edit": edit, "new": new, "load": load}
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
"""
