import pygame


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
        affichage de l'entitée avec la texture
        """
        screen.blit(self.texture, (self.x, self.y))


class Player(Entity):
    """
    Entité joueur avec textures un dictionnaire contenant des textures "droite","gauche","haut","bas"
    """

    def __init__(self, x, y, textures):
        self.textures = textures
        super().__init__(x, y, textures["droite"])
