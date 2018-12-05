
import os
import sys
import math
import pygame
import engine
pygame.init()
print("init...")


show_fps = True
w = 64
x = 0
y = 0

myfont = pygame.font.SysFont("monospace", 15)


size = width, height = 1280, 960


black = 0, 0, 0

screen = pygame.display.set_mode(size)


haut = pygame.image.load(os.path.join('assets', "haut.png"))
bas = pygame.image.load(os.path.join('assets', "bas.png"))
droite = pygame.image.load(os.path.join('assets', "droite.png"))
gauche = pygame.image.load(os.path.join('assets', "gauche.png"))
terre = pygame.image.load(os.path.join('assets', "terre.png"))
eau = pygame.image.load(os.path.join('assets', "eau.png"))
foret = pygame.image.load(os.path.join('assets', "foret.png"))

textures = {
    "0": eau,
    "1": terre,
    "2": foret
}

playeRect = pygame.Rect(x, y, w, w)

direction = [0, 0, 0, 0]
current = gauche


framerate = 50

m = engine.Carte(os.path.join("assets", "levels", "map1.mp"),
               mode="edit", dimensions=(int(width//w), int(height//w)))

state = 1

last = pygame.time.get_ticks()

"""
def loadMap(carte):
    wall = pygame.Surface((width, height))

    x = 0
    for l in carte:
        y = 0
        for p in l:
            if (p == 0):
                wall.blit(eau, (x, y))
            if (p == 1):
                wall.blit(terre, (x, y))
            if (p == 2):
                wall.blit(foret, (x, y))

            y += w
        x += w
    return wall
"""

wall = m.render(textures)


def waitf():
    global last
    while(pygame.time.get_ticks() - last < 1000/framerate):
        pass
    l = round(1000/(pygame.time.get_ticks() - last))

    last = pygame.time.get_ticks()
    return l


Pspeed = 5

faces = [droite, bas, gauche, haut]

print("init done in {}ms".format(pygame.time.get_ticks()))
while state:
    fps = waitf()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x = math.floor(pos[0] / w)
            y = math.floor(pos[1] / w)
            s = int(m.grid[x][y])
            s += 1
            if s > 2:
                s = 0
            m.grid[x][y] = str(s)
            wall = m.render(textures)
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_s:
                m.save()
            if event.key == pygame.K_LEFT:
                current = gauche
                direction[2] = 1
            if event.key == pygame.K_UP:
                current = haut
                direction[3] = 1
            if event.key == pygame.K_DOWN:
                current = bas
                direction[1] = 1
            if event.key == pygame.K_RIGHT:
                current = droite
                direction[0] = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                direction[2] = 0
                i = 0
                for d in direction:
                    if d == 1:
                        current = faces[i]
                    i += 1
            if event.key == pygame.K_UP:
                direction[3] = 0
                i = 0
                for d in direction:
                    if d == 1:
                        current = faces[i]
                    i += 1
            if event.key == pygame.K_DOWN:
                direction[1] = 0
                i = 0
                for d in direction:
                    if d == 1:
                        current = faces[i]
                    i += 1
            if event.key == pygame.K_RIGHT:
                direction[0] = 0
                i = 0
                for d in direction:
                    if d == 1:
                        current = faces[i]
                    i += 1
        if event.type == pygame.QUIT:
            state = 0
    if direction[0] == 1:
        playeRect.x += Pspeed
    if direction[2] == 1:
        playeRect.x -= Pspeed
    if direction[1] == 1:
        playeRect.y += Pspeed
    if direction[3] == 1:
        playeRect.y -= Pspeed
    screen.fill(black)
    screen.blit(wall, (0, 0))
    screen.blit(current, playeRect)
    if show_fps:
        label = myfont.render(str(fps), 1, (0, 255, 0))
        screen.blit(label, (width-40, 0))
    pygame.display.flip()
"""
    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]
"""
# screen.blit(ball, ballrect)
