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
        if self.life >= self.maxlife:
            self.life = self.maxlife
        elif self.life <= 0:
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
    useleftitem = 0
    userightitem = 0
    # assign key to directions
    keyConfig = {
        "left": pygame.K_d,
        "right": pygame.K_q,
        "down": pygame.K_s,
        "up": pygame.K_z,
        "useRight": pygame.K_r,
        "useLeft": pygame.K_a
    }
    mousepos = [0, 0]

    def __init__(self, x, y, setNum, scaleratio=1, hunger=100, thirst=100, life=100, speed=2, inventoryweight=204, inventorysize=12):
        """
        création de l'entitée joueur :
        le nom du set (setNum) correspond à un dossier dans les assets avec le nom du set et à l'intérieur les textures
        "front.png","back.png","backRight.png","backLeft.png","right.png","left.png"
        """
        path = os.path.join("assets", "playersets", setNum)
        self.speed = speed
        txname = ["front", "back", "backRight",
                  "backLeft", "right", "left"]

        self.scaleratio = scaleratio

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
        self.hudbackground = pygame.image.load(os.path.join(
            "assets", "hud", "HudBackground.png")).convert_alpha()
        self.lifebar = pygame.image.load(os.path.join(
            "assets", "hud", "PV.png")).convert_alpha()
        self.hungerbar = pygame.image.load(os.path.join(
            "assets", "hud", "Hunger.png")).convert_alpha()
        self.thirstbar = pygame.image.load(os.path.join(
            "assets", "hud", "Thirst.png")).convert_alpha()

        self.textures = dict()
        for a in txname:
            self.textures[a] = pygame.image.load(
                os.path.join(path, a+".png")).convert_alpha()

        super().__init__(x, y, self.textures["front"], life)

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
        if self.direction != [0,0,0,0] :
            if self.direction[3]:  # vers le haut
                self.facing = (0,-1)
                if self.direction[0]:  # droite et haut
                    self.texture = self.textures["backRight"]
                elif self.direction[2]:  # gauche et haut
                    self.texture = self.textures["backLeft"]
                else:  # juste le haut
                    self.texture = self.textures["back"]
            else:  # vers le bas ou bas-gauche/bas-droit
                if self.direction[0]:  # droite
                    self.texture = self.textures["right"]
                    self.facing = (0,1)
                elif self.direction[2]:  # gauche
                    self.texture = self.textures["left"]
                    self.facing = (0,-1)
                else:
                    self.texture = self.textures["front"]
                    self.facing = (1,0)

    def render(self, surface):
        """
        affichage de l'entité avec la texture sur screen
        """
        surface.blit(self.texture, (self.rect.x, self.rect.y)
                     )  # Affichage du personnage

        # Affichage de background du hud
        surface.blit(self.hudbackground, (0, 192))
        surface.blit(self.hud, (0, 192))  # affichage du hud vide

        if self.life > self.maxlife:
            self.life = self.maxlife
        if self.hunger > self.maxhunger:
            self.hunger = self.maxhunger
        if self.thirst > self.maxthirst:
            self.thirst = self.maxthirst
        # Affichage des barres de vie, faim et soif en fonction de leurs valeurs
        surface.blit(self.lifebar.subsurface(pygame.rect.Rect((111-111*self.life//self.maxlife, 0),
                                                              (111*self.life//self.maxlife, 67))), (111-111*self.life//self.maxlife, 207))
        surface.blit(self.hungerbar.subsurface(pygame.rect.Rect(
            (0, 0), (111*self.hunger//self.maxhunger, 57))), (401, 207))
        surface.blit(self.thirstbar.subsurface(pygame.rect.Rect(
            (0, 0), (111*self.thirst//self.maxthirst, 34))), (401, 240))

        # Création de l'image du contenu de l'inventaire
        inventorysurface = self.inventory.render(self.inventoryweight)
        # Affichage de cette surface
        surface.blit(inventorysurface, (154, 206))

        # Meme chose pour les contenus de chaque main
        righthandsurface = self.righthand.render(34)
        lefthandsurface = self.lefthand.render(34)
        surface.blit(righthandsurface, (362, 223))
        surface.blit(lefthandsurface, (116, 223))

        # Affichage de l'item tenu avec le curseur
        cursorinventorysurface = self.cursorinventory.render(34)
        surface.blit(cursorinventorysurface,
                     (self.mousepos[0] - 16, self.mousepos[1]-16))

    def changehunger(self, change):
        self.hunger += change
        if self.hunger >= self.maxhunger:
            self.hunger = self.maxhunger
        elif self.hunger <= 0:
            self.hunger = 0
            self.life -= 0.1

    def changethirst(self, change):
        self.thirst += change
        if self.thirst >= self.maxthirst:
            self.thirst = self.maxthirst
        elif self.thirst <= 0:
            self.thirst = 0
            self.life -= 0.1

    def clickinventory(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Verification du bouton pour prendre tout ou une partie des items
                if event.button == 1:
                    mode = "all"
                if event.button == 2:
                    mode = "one"
                if event.button == 3:
                    mode = "half"

                # Modification de l'inventaire principal
                if event.button == 1 or event.button == 2 or event.button == 3:
                    if self.mousepos[0] >= 154 and self.mousepos[1] >= 206 and self.mousepos[0] <= 357 and self.mousepos[1] <= 273:
                        invtile = int(
                            (self.mousepos[0]-154)//34 + (self.mousepos[1]-206)//34 * 6)
                        self.cursorinventory.items[0] = self.inventory.additem(
                            self.cursorinventory.items[0], invtile, mode)
                    # Modification de la main gauche
                    elif self.mousepos[0] >= 116 and self.mousepos[1] >= 223 and self.mousepos[0] <= 150 and self.mousepos[1] <= 257:
                        self.cursorinventory.items[0] = self.lefthand.additem(
                            self.cursorinventory.items[0], 0, mode)
                    # Modification de la main droite
                    elif self.mousepos[0] >= 362 and self.mousepos[1] >= 223 and self.mousepos[0] <= 396 and self.mousepos[1] <= 257:
                        self.cursorinventory.items[0] = self.righthand.additem(
                            self.cursorinventory.items[0], 0, mode)

    def update(self, wallrects, events):

        # Création d'une liste de déplacements en pixels en fonction de la direction
        move = [(self.speed, 0),
                (0, self.speed), (-self.speed, 0), (0, -self.speed)]
        # Création d'une liste des touches
        keys = [self.keyConfig["right"],
                self.keyConfig["down"], self.keyConfig["left"], self.keyConfig["up"]]
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.mousepos = [pygame.mouse.get_pos(
                )[0]*self.scaleratio, pygame.mouse.get_pos()[1]*self.scaleratio]
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

                # Utilisation de l'item de la main gauche
                if event.type == pygame.KEYDOWN:
                    if event.key == self.keyConfig["useRight"]:
                        if self.useleftitem == 0:
                            if self.lefthand.items[0] != "0":
                                self.lefthand.items[0] = self.lefthand.items[0].use(
                                    self)[0]
                        self.useleftitem = 1
                if event.type == pygame.KEYUP:
                    if event.key == self.keyConfig["useRight"]:
                        self.useleftitem = 0

                # Utilisation de l'item de la main droite
                if event.type == pygame.KEYDOWN:
                    if event.key == self.keyConfig["useLeft"]:
                        if self.userightitem == 0:
                            if self.righthand.items[0] != "0":
                                self.righthand.items[0] = self.righthand.items[0].use(
                                    self)[0]
                        self.userightitem = 1
                if event.type == pygame.KEYUP:
                    if event.key == self.keyConfig["useLeft"]:
                        self.userightitem = 0

        self.clickinventory(events)

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

        # Diminution de la nourriture et de la soif
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
    def __init__(self, x, y, life=10, loot=[], name="tree"):
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
