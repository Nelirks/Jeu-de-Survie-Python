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
# résolution cible : 1024*576


def mainLoop(game):
    wall = engine.Carte(os.path.join("assets", "levels", "test"),
                        mode="load")  # objet carte
    back = wall.renderSurface()  # surface carte
    print(wall.playerPosition)
    px = wall.playerPosition[0] * wall.tileSize
    py = wall.playerPosition[1] * wall.tileSize
    print(px, py)
    p1 = entities.Player(
        px, py, "1")  # joueur
    p1.direction = [0,0,0,0]
    events = []
    p1.cursorinventory.additem(items.Apple(5), 0)
    while game.state == 1 or game.state == 2:  # en jeu ou dans le menu pause
        if game.state == 1 :
            p1.update(wall.get_rects(), events)
        elif game.state == 2:
            p1.direction = [0,0,0,0]
            

        game.screen.blit(back, (0, 0))

        p1.render(game.screen)

        game.waitFramerate()

        events = game.runEvents()  # en fin de boucle pour éviter les conflicts
        if p1.life <= 0 :
            game.state = 0

        entitiesL = wall.entities
        i = 0
        for entity in entitiesL:
            if entity.life <= 0:
                del wall.entities[i]
            i+=1


