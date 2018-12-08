import pygame


PlayerFaces = {"right": 0, "down": 1, "left": 2, "up": 3}


class Entity:
    """
    Système d'entités pouvant être sauvegardé

    """
    x = 0
    y = 0

    def __init__(self, x, y, texture):
        self.x = x
        self.y = y
        self.texture = texture

    def render(self, screen):
        """
        affichage de l'entitée avec la texture sur screen
        """
        screen.blit(self.texture, (self.x, self.y))


class Player(Entity):
    """
    Entité joueur avec textures une liste contenant des textures [droite,bas,gauche,haut]
    """

    def __init__(self, x, y, textures):
        self.textures = textures
        super().__init__(x, y, textures[0])

    def setFace(self, face):
        self.texture = self.textures[face]
