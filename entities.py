import pygame


PlayerFaces = {"right": 0, "down": 1, "left": 2, "up": 3}


class Entity:
    """
    Système d'entités pouvant être sauvegardé

    """
    x = 0
    y = 0

    def __init__(self, x, y, texture):
        """
        création de l'entitée
        """
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
    direction = [0, 0, 0, 0]
    # vitesse de déplacement
    speed = 5

    # assign key to directions
    keyConfig = {
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
        "down": pygame.K_DOWN,
        "up": pygame.K_UP
    }

    def __init__(self, x, y, textures, speed=5):
        """
        création de l'entitée
        """
        self.speed = speed
        self.textures = textures
        super().__init__(x, y, textures[0])

    def setFace(self, face):
        """
        définie la texture en fonction de la direction
        """
        self.texture = self.textures[face]

    def findDirection(self, direction, last):
        """
        trouve la bonne direction après un touche relachée
        """
        i = 0
        l = last
        for d in direction:
            if d == 1:
                l = i
            i += 1
        return l

    def update(self, events):
        """
        prend comme argument tous les évenements et prends les touches de mouvement
        """
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
