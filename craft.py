import pygame
import items
import os
import engine
"""
enregistrement des crafts: 
crafts dans une liste dans la forme :
    [(liste d'items nécessaires avec leur quantité ),(item de sortie,quantité) ]
    cette liste d'items nécessaires est de la forme:
        [(nom de l'item,qantité)]
"""
craftClickEvent = pygame.USEREVENT + 2


# initialisation des crafts
crafts = [
    {
        "input": (["Apple", 1], ["Wood", 1]),
        "output": ["Wood", 2]
    }
]
craftTableImage = 0
itemsTextureIndex = dict()
ratio = 1


def initCrafts(scaleRatio):
    global craftTableImage
    global ratio
    ratio = scaleRatio
    craftTableImage = pygame.image.load(os.path.join(
        "assets", "hud", "crafting.png")).convert_alpha()

    for i in items.itemsList:
        itemsTextureIndex[i] = items.itemsList[i](1).texture


class Craft():
    def __init__(self, position, itemOut, itemsIn, size=(32, 32)):
        """
        Classe pour gérer les crafts :
            itemOut : ["nomItem", quantité]
            itemIn :  liste de ["nomItem", quantité]
        """

        self.position = position
        self.texture = itemsTextureIndex[itemOut[0]]
        self.position = position
        self.itemOut = items.itemsList[itemOut[0]](itemOut[1])
        self.itemsIn = []
        self.screenRatio = ratio
        for i in itemsIn:
            self.itemsIn.append(items.itemsList[i[0]](i[1]))
        self.selected = 0
        self.focused = 0
        self.rect = pygame.Rect(position, (32, 32))

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                mX = pos[0]*ratio
                mY = pos[1]*ratio
                if self.rect.collidepoint(mX, mY):
                    self.focused = 1
                else:
                    self.focused = 0
            if event.type == pygame.MOUSEBUTTONUP:
                if self.focused == 1:
                    self.selected = 1


def showCrafts(screen):
    screen.blit(craftTableImage, (0, 0))
    x = 2
    y = 2
    compteur = 0
    for c in crafts:
        screen.blit(itemsTextureIndex[c["output"][0]], (x, y))
        compteur += 1
