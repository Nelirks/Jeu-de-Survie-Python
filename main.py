# coding: utf-8
import os
import entities
import pygame
import menu
import items
import engine
pygame.init()
pygame.key.set_repeat(50, 1)

# résolution du rendu :512*288
# résolution cible : 1280*720


def changeMap(mapPosition, player, modX, modY):
    mapPosition[0] += modX
    mapPosition[1] += modY
    wall = engine.Carte(os.path.join("assets", "levels", str(mapPosition)),
                        mode="load")
    #player.direction = [0, 0, 0, 0]
    if modY == -1:
        player.rect.y = wall.height - wall.tileSize
    if modY == +1:
        player.rect.y = 0
    if modX == -1:
        player.rect.x = wall.width - wall.tileSize
    if modX == +1:
        player.rect.x = 0

    return wall


def mainLoop(game):
    mapPosition = [0, 0]
    wall = engine.Carte(os.path.join("assets", "levels", str(mapPosition)),
                        mode="load")  # objet carte
    back = wall.renderSurface()  # surface carte
    # coolframe = 0
    px = wall.playerPosition[0] * wall.tileSize
    py = wall.playerPosition[1] * wall.tileSize
    ratio = game.resolution[0]/game.targetResolution[0]
    p1 = entities.Player(
        px, py, "1", ratio)  # joueur
    p1.direction = [0, 0, 0, 0]
    events = []

    p1.inventory.additem(items.Apple(12), 0)
    p1.inventory.additem(items.Apple(34), 1)
    p1.inventory.additem(items.Apple(56), 2)
    p1.inventory.additem(items.Apple(78), 3)
    p1.inventory.additem(items.Apple(90), 4)
    p1.inventory.additem(items.Apple(1), -1)
    while game.state == 1 or game.state == 2:  # en jeu ou dans le menu pause
        if game.state == 1:
            pevents = events
            """
            if p1.rect.x < 0 and p1.rect.y < 0 and p1.rect.x > wall.width and p1.rect.y > wall.height or coolframe > 0:
                coolframe -= 1
                pevents = []
            """
            rects = wall.get_rects()
            p1.update(rects, pevents)

        elif game.state == 2:
            p1.direction = [0, 0, 0, 0]

        game.screen.blit(back, (0, 0))

        p1.render(game.screen)

        game.waitFramerate()

        if p1.rect.x < -wall.tileSize*(4/8):
            wall = changeMap(mapPosition, p1, -1, 0)
            back = wall.renderSurface()

        if p1.rect.y < -wall.tileSize*(4/8):
            wall = changeMap(mapPosition, p1, 0, -1)
            back = wall.renderSurface()

        if p1.rect.x > wall.width - wall.tileSize * (4/8):
            wall = changeMap(mapPosition, p1, +1, 0)
            back = wall.renderSurface()

        if p1.rect.y > wall.height - wall.tileSize * (4/8):
            wall = changeMap(mapPosition, p1, 0, +1)
            back = wall.renderSurface()

        events = game.runEvents()  # en fin de boucle pour éviter les conflicts
        if p1.life <= 0:
            game.state = 0

        entitiesL = wall.entities
        i = 0
        for entity in entitiesL:
            if entity.life <= 0:
                del wall.entities[i]
                back = wall.renderSurface()
            i += 1
