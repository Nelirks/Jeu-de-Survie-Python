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

    def update(self, events, playerInventory):
        if self.selected:
            playerInventory.additem(items.Apple(1), -1)

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
                else:
                    self.selected = 0

    def render(self, screen):
        screen.blit(self.texture, self.position)
        outQuantity = self.basicfont.render(
            str(self.itemOut.quantity), False, (255, 255, 255))
        screen.blit(outQuantity, (self.position[0]+18, self.position[1]+21))
        if self.focused:
            pygame.draw.rect(screen, (255, 255, 0),
                             pygame.Rect(self.position, (32, 32)), 1)  # carré jaune qui entoure
        if self.selected:
            pygame.draw.rect(screen, (255, 255, 255),
                             pygame.Rect(self.position, (32, 32)), 1)  # carré blanc qui entoure
            compteur = 0
            x = 50
            y = 100
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
                itemquantity = self.basicfont.render(
                    str(e.quantity), False, (255, 255, 255))
                screen.blit(itemquantity, (x+18, y+21))
                x += self.rect.width


craftsButtonList = []


def createCrafts():
    x = 2
    y = 2
    for c in crafts:
        craftsButtonList.append(Craft((x, y), c["output"], c["input"]))
        x += 32


def showCrafts(screen):
    screen.blit(craftTableImage, (0, 0))
    for c in craftsButtonList:
        c.render(screen)
    #compteur = 0
    # for c in crafts:
    #    screen.blit(itemsTextureIndex[c["output"][0]], (x, y))
    #    compteur += 1


def update(events, playerInventory):
    for c in craftsButtonList:
        c.update(events, playerInventory)
