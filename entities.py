# coding: utf-8
import pygame
import os
import items

PlayerFaces = {"right": 0, "down": 1, "left": 2, "up": 3}


class Entity:
    """
    Système d'entités pouvant être sauvegardé

    """
    x = 0
    y = 0
    life = 0
    effects = []

    def __init__(self, x, y, texture, life=0):
        """
        création de l'entitée
        """
        self.texture = texture.convert_alpha()
        self.rect = pygame.rect.Rect(
            x, y, texture.get_rect().width, texture.get_rect().height)

    def render(self, surface):
        """
        affichage de l'entitée avec la texture sur screen
        """
        surface.blit(self.texture, (self.rect.x, self.rect.y))

    def takeDamage(self, damage):
        self.life -= damage  # Todo : ajouter du random

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
    # vitesse de déplacement
    speed = 1
    

    # assign key to directions
    keyConfig = {
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
        "down": pygame.K_DOWN,
        "up": pygame.K_UP
    }

    def __init__(self, x, y, setNum, speed=2):
        """
        création de l'entitée joueur :
        le nom du set (setNum) correspond à un dossier dans les assets avec le nom du set et à l'intérieur les textures
        "front.png","back.png","backRight.png","backLeft.png","right.png","left.png"
        """
        path = os.path.join("assets", "playersets", setNum)
        self.speed = speed
        txname = ["front", "back", "backRight",
                  "backLeft", "right", "left"]

        self.textures = dict()
        for a in txname:
            self.textures[a] = pygame.image.load(
                os.path.join(path, a+".png")).convert_alpha()
        self.inventory = items.ItemContainer(1)



        super().__init__(x, y, self.textures["front"])

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

    def movement(self, wallrects, events):
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
                nbCollisions = len(wallrects)
                for m in range(len(wallrects)):
                            # vérifie que le rectangle du personnage de va pas rentrer en collision avec un bloc
                    if self.rect.move(move[n]).colliderect(wallrects[m]):
                            # Si oui, met la direction à 2 -> veut bouger mais est bloqué
                        self.direction[n] = 2
                    else:
                        nbCollisions -= 1
                if nbCollisions == 0:
                    # permet le déplacement si aucune collision n'est possible
                    self.direction[n] = 1
                if self.direction[n] == 1:
                    # déplace le personnage si il le veut et le peut
                    self.rect = self.rect.move(move[n])

    """ 
    def update(self, events):
        # prend comme argument tous les évenements et prends les touches de mouvement
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == self.keyConfig["left"]:
                    self.setFace(PlayerFaces["left"])
                    self.direction[2] = 1
                if event.key == self.keyConfig["up"]:
                    self.setFace(PlayerFaces["up"])
                    self.direction[3] = 1
                if event.key == self.keyConfig["down"]:
                    self.setFace(PlayerFaces["down"])
                    self.direction[1] = 1
                if event.key == self.keyConfig["right"]:
                    self.setFace(PlayerFaces["right"])
                    self.direction[0] = 1
            if event.type == pygame.KEYUP:
                if event.key == self.keyConfig["left"]:
                    self.direction[2] = 0
                    self.setFace(self.findDirection(self.direction, 2))
                if event.key == self.keyConfig["up"]:
                    self.direction[3] = 0
                    self.setFace(self.findDirection(self.direction, 3))
                if event.key == self.keyConfig["down"]:
                    self.direction[1] = 0
                    self.setFace(self.findDirection(self.direction, 1))
                if event.key == self.keyConfig["right"]:
                    self.direction[0] = 0
                    self.setFace(self.findDirection(self.direction, 0))
        # applique les mouvements
        if self.direction[0] == 1:
            self.x += self.speed
        if self.direction[2] == 1:
            self.x -= self.speed
        if self.direction[1] == 1:
            self.y += self.speed
        if self.direction[3] == 1:
            self.y -= self.speed
    """
