import pygame

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
