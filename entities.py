# coding: utf-8
import pygame
import os
import items
import random


PlayerFaces = {"right": 0, "down": 1, "left": 2, "up": 3}


class Entity:
    """
    Système d'entités pouvant être sauvegardé

    """

    life = 0
    effects = []

    def __init__(self, x, y, texture, life=0):
        """
        création de l'entitée
        """
        self.texture = texture.convert_alpha()
        self.rect = pygame.rect.Rect(
            x, y, texture.get_rect().width, texture.get_rect().height)
        self.life = life
        self.maxlife = life

    def render(self, surface):
        """
        affichage de l'entitée avec la texture sur screen
        """
        surface.blit(self.texture, (self.rect.x, self.rect.y))

    def takeDamage(self, damage):
        self.life -= damage  # Todo : ajouter du random
        if self.life >= self.maxlife :
            self.life = self.maxlife
        elif self.life <=0:
            self.life = 0
                        

    def takeMagicDamage(self, magicDamage, mDamageType):
        # à faire : résistance / faiblesse éléments
        ratio = 1  # à changer en fonction des faiblesses et résistances
        self.life -= magicDamage*ratio
        if mDamageType == "fire":
            # à faire : classe effet et appliquation des effets
            self.effects.append("fire")


class Player(Entity):
    """
    Entité joueur avec textures une liste contenant des textures [droite,bas,gauche,haut]
    """
    direction = [0, 0, 0, 0]

    # assign key to directions
    keyConfig = {
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
        "down": pygame.K_DOWN,
        "up": pygame.K_UP
    }

    def __init__(self, x, y, setNum, scaleratio = 1, hunger = 100, thirst = 100, life = 100, speed=2, inventoryweight=204, inventorysize=12):
        """
        création de l'entitée joueur :
        le nom du set (setNum) correspond à un dossier dans les assets avec le nom du set et à l'intérieur les textures
        "front.png","back.png","backRight.png","backLeft.png","right.png","left.png"
        """
        path = os.path.join("assets", "playersets", setNum)
        self.speed = speed
        txname = ["front", "back", "backRight",
                  "backLeft", "right", "left"]

        self.inventory = items.ItemContainer(inventorysize)
        self.inventoryweight = inventoryweight
        self.level = 0

        self.lefthand = items.ItemContainer(1)
        self.righthand = items.ItemContainer(1)

        self.cursorinventory = items.ItemContainer(1)

        self.hunger = hunger
        self.thirst = thirst
        self.maxhunger = hunger
        self.maxthirst = thirst

        self.levelColor = (100, 100, 100)
        self.hud = pygame.image.load(os.path.join(
            "assets", "hud", "HudBorders.png")).convert_alpha()
        self.hudbackground = pygame.image.load(os.path.join("assets", "hud", "HudBackground.png")).convert_alpha()
        self.lifebar = pygame.image.load(os.path.join("assets", "hud", "PV.png")).convert_alpha()
        self.hungerbar = pygame.image.load(os.path.join("assets", "hud", "Hunger.png")).convert_alpha()
        self.thirstbar = pygame.image.load(os.path.join("assets", "hud", "Thirst.png")).convert_alpha()

        self.textures = dict()
        for a in txname:
            self.textures[a] = pygame.image.load(
                os.path.join(path, a+".png")).convert_alpha()

        super().__init__(x, y, self.textures["front"],life)

    def setFace(self, face):
        """
        définie la texture en fonction de la direction
        """
        self.texture = self.textures[face]

    # Récupère ton code si je veux, moi je mets le mien
    def findDirection(self):
        # trouve la bonne direction après un touche relachée
        """i = 0
        l = last
        for d in direction:
            if d >= 1:
                l = i
            i += 1

        """

        if self.direction[3]:  # vers le haut
            if self.direction[0]:  # droite et haut
                self.texture = self.textures["backRight"]
            elif self.direction[2]:  # gauche et haut
                self.texture = self.textures["backLeft"]
            else:  # juste le haut
                self.texture = self.textures["back"]
        else:  # vers le bas ou bas-gauche/bas-droit
            if self.direction[0]:  # droite
                self.texture = self.textures["right"]
            elif self.direction[2]:  # gauche
                self.texture = self.textures["left"]
            else:
                self.texture = self.textures["front"]

    def render(self, surface):
        """
        affichage de l'entité avec la texture sur screen
        """
        surface.blit(self.texture, (self.rect.x, self.rect.y)) #Affichage du personnage

        surface.blit(self.hudbackground,(0,192)) #Affichage de background du hud
        surface.blit(self.hud, (0, 192)) #affichage du hud vide

        #Affichage des barres de vie, faim et soif en fonction de leurs valeurs
        surface.blit(self.lifebar.subsurface(pygame.rect.Rect((111-111*self.life//self.maxlife,0),(111*self.life//self.maxlife,67))),(111-111*self.life//self.maxlife, 207))
        surface.blit(self.hungerbar.subsurface(pygame.rect.Rect((0,0),(111*self.hunger//self.maxhunger,57))),(401, 207))
        surface.blit(self.thirstbar.subsurface(pygame.rect.Rect((0,0),(111*self.thirst//self.maxthirst,34))),(401, 240))

        inventorysurface = self.inventory.render(self.inventoryweight) #Création de l'image du contenu de l'inventaire
        surface.blit(inventorysurface, (154, 206)) #Affichage de cette surface

        #Meme chose pour les contenus de chaque main
        righthandsurface = self.righthand.render(34)
        lefthandsurface = self.lefthand.render(34)
        surface.blit(righthandsurface, (362, 223))
        surface.blit(lefthandsurface, (116, 223))

        cursorinventorysurface = self.cursorinventory.render(34)
        surface.blit(cursorinventorysurface, pygame.mouse.get_pos())

    def changehunger(self, change) :
        self.hunger += change
        if self.hunger >= self.maxhunger :
            self.hunger = self.maxhunger
        elif self.hunger <=0:
            self.hunger = 0
            self.life -= 0.1

    def changethirst(self, change) :
        self.thirst += change
        if self.thirst >= self.maxthirst :
            self.thirst = self.maxthirst
        elif self.thirst <=0:
            self.thirst = 0
            self.life -= 0.1

    def update(self, wallrects, events):
        # Création d'une liste de déplacements en pixels en fonction de la direction
        move = [(self.speed, 0),
                (0, self.speed), (-self.speed, 0), (0, -self.speed)]
        # Création d'une liste des touches
        keys = [self.keyConfig["right"],
                self.keyConfig["down"], self.keyConfig["left"], self.keyConfig["up"]]
        for event in events:
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:  # optimisation
                for n in range(4):  # (pour chaque direction)
                    if event.type == pygame.KEYDOWN:
                        if event.key == keys[n]:
                            # met la direction à 1 -> peut bouger
                            self.direction[n] = 1

                    if event.type == pygame.KEYUP:
                        if event.key == keys[n]:
                            # met la direction à 0 -> ne veut pas bouger
                            self.direction[n] = 0
                self.findDirection()

        for n in range(4):
            # permet de dire si le personnage est bloqué s'il veut bouger (qu'il aie été bloqué ou pas précedemment)
            if self.direction[n] != 0:
                # vérifie que le rectangle du personnage de va pas rentrer en collision avec les blocs
                if self.rect.move(move[n]).collidelist(wallrects) != -1:
                    # Si oui, met la direction à 2 -> veut bouger mais est bloqué
                    self.direction[n] = 2
                else:
                    # permet le déplacement si aucune collision n'est possible
                    # déplace le personnage si il le veut et le peut
                    self.rect = self.rect.move(move[n])
        
        #Diminution de la nourriture et de la soif
        self.changehunger(-0.01)
        self.changethirst(-0.02)


class Collectable(Entity):
    loot = []
    name = ""

    def __init__(self, x, y, texture, life=0, loot=[], name=""):
        """
        loot : liste [[item,p],[item,p]]
        """
        self.loot = loot
        self.name = name
        super().__init__(x, y, texture, life=life)

    def Loot(self):
        r = []
        for l in self.loot:
            if l[1] < random.random():
                r.append(l[0])
        return l


class Tree(Collectable):
    def __init__(self, x, y, life=0, loot=[], name="tree"):
        texture = pygame.image.load(
            os.path.join("assets", "entities", "tree.png"))
        super().__init__(x, y, texture, life=life, loot=loot, name=name)


class SavableEntity:
    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.name = name

    def transform(self):
        return entitiesList[self.name](self.x, self.y)


# liste des entitées disponibles
entitiesList = {"tree": Tree}
