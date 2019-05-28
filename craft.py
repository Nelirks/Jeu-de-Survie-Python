import pygame
import items
import os
import engine
import copy
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
        "input": (["Apple", 4], ["Wood", 1]),
        "output": ["Wood", 2]
    },
    {
        "input": [["Apple", 3]],
        "output":["Pompot", 1]
    },
    {
        "input": [["Coconut", 1]],
        "output":["HalfCoconut", 2]
    }
]
craftTableImage = 0
itemsTextureIndex = dict()
ratio = 1
width = 0
height = 0


def initCrafts(scaleRatio, carte):
    global craftTableImage
    global ratio
    global width
    global height

    width = carte.width
    height = carte.height

    ratio = scaleRatio

    craftTableImage = pygame.image.load(os.path.join(
        "assets", "hud", "crafting.png")).convert_alpha()
    for i in items.itemsList:
        itemsTextureIndex[i] = items.itemsList[i](1).texture
    createCrafts()


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
        self.basicfont = pygame.font.SysFont("Source Code Pro", 12)
        self.rect = pygame.Rect(position, (32, 32))
        self.playeInventory = []
        self.craftPossible = 0
        self.focusedOut = 0
        self.outRect = pygame.Rect((377, 105), (34, 34))
        self.impossibleSurface = pygame.Surface(
            (34, 34), pygame.SRCALPHA, 32).convert_alpha()
        self.impossibleSurface.fill(pygame.Color(100, 100, 100, 150))

    def update(self, events, playerInventory):

        for event in events:
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                mX = pos[0]*ratio
                mY = pos[1]*ratio
                if self.rect.collidepoint(mX, mY):
                    self.focused = 1
                else:
                    self.focused = 0

                if self.outRect.collidepoint(mX, mY) and self.selected:
                    self.focusedOut = 1
                else:
                    self.focusedOut = 0
            if event.type == pygame.MOUSEBUTTONUP:

                if self.focusedOut == 1 and self.craftPossible == 1:
                    self.playeInventory.additem(copy.copy(self.itemOut), -1)
                    for i in self.itemsIn:
                        e = copy.copy(i)
                        e.quantity *= -1
                        self.playeInventory.additem(e, -1)
                if self.focused == 1:
                    self.selected = 1
                else:
                    if self.focusedOut == 1:
                        self.selected = 1
                    else:
                        self.selected = 0
        self.playeInventory = playerInventory
        self.craftPossible = 1
        for i in self.itemsIn:
            if playerInventory.haveItem(i.nom, i.quantity) == 0:
                self.craftPossible = 0

    def render(self, screen):
        screen.blit(self.texture, self.position)

        if self.focused:
            pygame.draw.rect(screen, (255, 255, 0),
                             pygame.Rect(self.position, (32, 32)), 1)  # carré jaune qui entoure
        if self.selected:
            pygame.draw.rect(screen, (255, 255, 255),
                             pygame.Rect(self.position, (32, 32)), 1)  # carré blanc qui entoure
            compteur = 0

            screen.blit(self.itemOut.texture, (378, 106))
            outQuantity = self.basicfont.render(
                str(self.itemOut.quantity), False, (255, 255, 255))
            screen.blit(
                outQuantity, (378+20, 106+18))
            if self.craftPossible == 0:
                screen.blit(self.impossibleSurface, (377, 105))
            x = 59
            y = 106
            for e in self.itemsIn:
                if compteur >= 1:
                    x += 5
                    # afficher le plus
                    pygame.draw.line(screen, (255, 255, 255),
                                     (x+5, y+10), (x+5, y+20))
                    pygame.draw.line(screen, (255, 255, 255),
                                     (x+0, y+15), (x+10, y+15))
                    x += 15
                compteur += 1
                screen.blit(e.texture, (x, y))
                color = (255, 255, 255)
                if self.playeInventory.haveItem(e.nom, e.quantity) == 0:
                    color = (255, 0, 0)
                itemquantity = self.basicfont.render(
                    str(e.quantity), False, color)
                screen.blit(itemquantity, (x+20, y+18))
                x += self.rect.width


craftsButtonList = []


def createCrafts():
    global craftsButtonList
    x = 2
    y = 2
    craftsButtonList = []
    for c in crafts:

        craftsButtonList.append(Craft((x, y), c["output"], c["input"]))
        x += 32


def showCrafts(screen):
    screen.blit(craftTableImage, (0, 0))
    for c in craftsButtonList:
        c.render(screen)
    # compteur = 0
    # for c in crafts:
    #    screen.blit(itemsTextureIndex[c["output"][0]], (x, y))
    #    compteur += 1


def update(events, playerInventory):
    for c in craftsButtonList:
        c.update(events, playerInventory)
