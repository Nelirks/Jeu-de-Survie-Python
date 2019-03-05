# coding: utf-8
import pygame
from math import ceil
import os

CONST_TileItemSize = 16


class Item:
    """
    Classe Item permettant de base pour tout item de l'inventaire

    """
    nom = ""
    description = ""
    quantity = 0

    def __init__(self, nom, quantity, texturedir, description=""):
        """
        crée un objet Item pour être utilisé dans l'inventaire,
        il est préférable d'utiliser un objet enfant du type adapté (ex: potion, arme)
        """
        self.nom = nom
        self.description = description
        self.texture = pygame.image.load(texturedir).convert_alpha()
        self.quantity = quantity

    def render(self):
        """
        retourne une surface avec l'item
        """
        surface = pygame.Surface(CONST_TileItemSize, CONST_TileItemSize)
        surface.blit(self.texture, (0, 0))
        return surface

class Consommable(Item) :
    #Classe consommmable : Item avec des effets quand il est consommé
    def __init__(self, nom, texture, lifegain = 0, hungergain = 0, thirstgain = 0, buff = "", description = "") :
        self.lifegain = lifegain
        self.hungergain = hungergain
        self.thirstgain = thirstgain
        self.buff = buff
        super().__init__(nom, texture, description)

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
    
    def __init__(self, size) : #Création de deux listes liste ayant une longueur size
        self.items = []
        for n in range(size) :
            self.items.append("0")

    def sizeincrease(self ,sizeup): #Augmentation de la longueur des listes en cas d'augmentation de l'inventaire
        for n in range (sizeup):
            self.items.append("0")

    def additem(self, itemadded, place): #Ajout d'un item en vérifiant que la case n'est pas vide, si elle est vide, renvoie l'item précedent et sa quantité
        if self.items[place] != "0":
            if self.items[place].quantity != 0 :
                if self.items[place].nom == itemadded.nom :
                    self.items[place].quantity += itemadded.quantity
                    return ("It worked !")
                else : 
                    olditem = self.items[place]
                    self.items[place] = itemadded
                    return (olditem)
        else :
            self.items[place] = itemadded
            return ("It worked !")


    def removeitem(self, place, mode) : #Permet le retrait d'item, avec trois modes, half, one et all, et renvoie le type et a quantité d'item retirés
        if self.items[place] != "0" :
            itemremoved = "0"
        else :    
            if mode == "all" :
                itemremoved = self.items[place]
                self.items[place] ="0"
            if mode == "half" :
                itemremoved = self.items[place]
                itemremoved.quantity = ceil(itemremoved.quantity /2)
                self.items[place].quantity -= itemremoved.quantity
                if self.items[place].quantity == 0:
                    self.items[place] = "0"
            if mode == "one" :
                itemremoved = self.items[place]
                itemremoved.quantity = 1
                self.items[place].quantity -= itemremoved.quantity
                if self.items[place].quantity == 0:
                    self.items[place] = "0"
        return itemremoved



    def render(self, largeur) : #Crée une surface avec tous les items dans un rectangle de largeur donnée en pixel
        itemperline = (largeur)//34
        itempercolumn = ceil(len(self.items)/itemperline)
        surfacefinale = pygame.Surface((itemperline*34, itempercolumn*34),pygame.SRCALPHA, 32).convert_alpha()
        for n in range (len(self.items)) :
            x = n%itemperline
            y = n//itemperline
            if self.items[n] != "0" :
                surfacefinale.blit(self.items[n].texture,(x*34+1,y*34+1))
        return surfacefinale
