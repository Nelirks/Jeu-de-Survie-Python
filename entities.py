import pygame


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
        ts = []
        for t in textures:
            # optimisations de pygame, besoin de transparence
            ts.append(t.convert_alpha())
        self.textures = textures
        super().__init__(x, y, textures[0])

    def setFace(self, face):
        """
        définie la texture en fonction de la direction
        """
        self.texture = self.textures[face]

# Récupère ton code si je veux, moi je mets le mien
    """def findDirection(self, direction, last):
        #trouve la bonne direction après un touche relachée
        i = 0
        l = last
        for d in direction:
            if d == 1:
                l = i
            i += 1
        return l

    def update(self, events):
        #prend comme argument tous les évenements et prends les touches de mouvement
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


def movement(self, wallrects):
    # Création d'une liste de déplacements en pixels en fonction de la direction
    move = [(-self.speed, 0), (0, -self.speed),
            (self.speed, 0), (0, self.speed)]
    # Création d'une liste des touches
    keys = [self.keyConfig["left"], self.keyConfig["up"],
            self.keyConfig["right"], self.keyConfig["down"]]
    for event in pygame.event.get():
        for n in range(4):  # (pour chaque direction)
            if event.type == pygame.KEYDOWN:
                if event.key == keys[n]:
                    # met la direction à 1 -> peut bouger
                    self.direction[n] = 1
            if event.type == pygame.KEYUP:
                if event.key == keys[n]:
                    # met la direction à 0 -> ne veut pas bouger
                    self.direction[n] = 0
        for n in range(4):
            # permet de dire si le personnage est bloqué s'il veut bouger (qu'il aie été bloqué ou pas précedemment)
            if self.direction[n] != 0:
                nbCollisions = len(wallrects)
                for m in range(len(wallrects)):
                    # vérifie que le rectangle du personnage de va pas rentrer en collision avec un bloc
                    if self.chrrect.move(move[n]).colliderect(wallrects[m]):
                        # Si oui, met la direction à 2 -> veut bouger mais est bloqué
                        self.direction[n] = 2
                    else:
                        nbCollisions -= 1
                if nbCollisions == 0:
                    # permet le déplacement si aucune collision n'est possible
                    self.direction[n] = 1
                if self.direction[n] == 1:
                    # déplace le personnage si il le veut et le peut
                    self.chrrect = self.chrrect.move(move[n])
