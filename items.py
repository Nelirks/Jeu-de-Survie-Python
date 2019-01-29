# coding: utf-8
import pygame
from math import ceil

CONST_TileItemSize = 16


class Item:
    """
    Classe Item permettant de base pour tout item de l'inventaire

    """
    nom = ""
    description = ""

    def __init__(self, nom, texture, description=""):
        """
        crée un objet Item pour être utilisé dans l'inventaire,
        il est préférable d'utiliser un objet enfant du type adapté (ex: potion, arme)
        """
        self.nom = nom
        self.description = description
        self.texture = texture.convert_alpha()

    def render(self):
        """
        retourne une surface avec la l'item
        """
        surface = pygame.Surface(CONST_TileItemSize, CONST_TileItemSize)
        surface.blit(self.texture, (0, 0))
        return surface


class Weapon(Item):
    """
    Classe arme : un item avec une caratéristique de dégats
    """

    damage = 0
    portee = 1

    def __init__(self, nom, texture, damage=0, portee=1, description=''):
        self.damage = damage
        self.portee = portee
        super().__init__(nom, texture, description)

    def applyDamage(self, entity):
        """
        applique les dégats à un entitée
        """
        entity.takeDamage(self.damage)


'''
class MagicWeapon(Weapon):
    """
    arme magiqe : applique des dégats magiques d'un certain type
    pour une arme totalement magique, mettre damage = 0
    """
    mDamageType = "fire"
    magicDamage = 0

    def __init__(self, nom, texture, damage=0, magicDamage=0, mDamageType="fire", description=''):
        self.mDamageType = mDamageType
        self.magicDamage = magicDamage
        super().__init__(nom, texture, damage=damage, description=description)

    def applyDamage(self, entity):
        entity.takeMagicDamage(self.magicDamage, self.mDamageType)
        super().applyDamage(entity)
'''
class ItemContainer :
    itemtype = []
    itemquantity = []
    
    def __init__(self, size) : #Création de deux listes liste ayant une longueur size
        for n in range(size) :
            self.itemtype.append("0")
            self.itemquantity.append(0)

    def sizeincrease(self ,sizeup): #Augmentation de la longueur des listes en cas d'augmentation de l'inventaire
        for n in range (sizeup):
            self.itemtype.append("0")
            self.itemquantity.append(0)

    def additem(self, name, quantity, place): #Ajout d'un item en vérifiant que la case n'est pas vide, si elle est vide, renvoie l'item précedent et sa quantité
        if self.itemquantity[place] != 0 :
            if self.itemtype == name :
                self.itemquantity[place] += quantity
                return (1,"It worked !")
        else : 
            oldname = self.itemtype[place]
            oldquantity = self.itemquantity[place]
            self.itemtype[n] = name
            self.itemquantity = quantity
            return (oldname, oldquantity)


    def removeitem(self, place, mode) : #Permet le retrait d'item, avec trois modes, half, one et all, et renvoie le type et a quantité d'item retirés
        if mode == "all" :
            name = self.itemtype[place]
            quantity = self.itemquantity[place]
            self.itemquantity[place] = 0
            self.itemtype[place] = "0"
        if mode == "half":
            name = self.item[place]
            quantity = ceil(self.item[place]/2)
            self.itemquantity[place] -= quantity
            if self.itemquantity[place] == 0:
                self.itemtype[place] = "0"
        if mode == "one" :
            name = self.item[place]
            quantity = 1
            self.itemquantity[place] -= quantity
            if self.itemquantity[place] == 0:
                self.itemtype[place] = "0"
        return name, quantity

    def render(self, largeur) :
        itemsperline = largeur//32
        itempercolumn = ceil(len(self.itemquantity)/itemperline)
        surfacefinale = pygame.display.set_mode((itemperline,itempercolumn))
