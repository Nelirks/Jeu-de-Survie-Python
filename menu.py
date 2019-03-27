import pygame
import main
import os
import random
import math
import engine


class Star:

    def __init__(self, position, size, speed=(-10, 0)):
        self.speed = speed
        self.x = position[0]
        self.y = position[1]
        self.surface = pygame.surface.Surface((size*2, size))
        self.surface.fill((255, 255, 255))

    def render(self, surface):
        surface.blit(self.surface, (self.x, self.y))

    def update(self):

        self.x += self.speed[0]
        self.y += self.speed[1]


class Stars:
    """
    une nuée d'étoiles défilant
    """

    liste = []
    line = 5
    frame = 0

    def render(self, surface):
        if self.frame % 8 == 0:
            width = surface.get_width()
            height = surface.get_height()
            for i in range(self.line):
                x = width + random.randint(-10, 10)
                y = random.randint(10, height-10)
                self.liste.append(Star((x, y), random.randint(1, 5)))
        i = 0
        for s in self.liste:
            s.render(surface)
            s.update()
            if s.x < 0:
                self.liste.pop(i)
            else:
                i += 1
        self.frame += 1


game = engine.Engine((1280, 720),
                     (1280, 720), framerate=100)  # fenêtre 1:1 pour les boutons
game.state = 0

playEvent = pygame.USEREVENT + 2
creditsEvent = pygame.USEREVENT + 3


playButton = engine.Button(
    (10, 10), (130, 50),  "Jouer", playEvent, fontSize=60, focusedBackground=(100, 100, 100))
creditsButton = engine.Button(
    (10, 70), (110, 40),  "Crédits", creditsEvent, fontSize=40, focusedBackground=(100, 100, 100))
fullScreenButton = engine.Button((10, 120), (170, 40), "Plein Écran",
                                 game.fullscreenEvent, fontSize=40, focusedBackground=(100, 100, 100))
closeButton = engine.Button(
    (10, 170), (240, 40),  "Retour au bureau", pygame.QUIT, fontSize=40, focusedBackground=(100, 100, 100))


def mainMenu():
    global game
    game.state = 0
    spaceShip = pygame.image.load(os.path.join("assets", "spaceship2.png"))
    spaceShip = pygame.transform.scale2x(spaceShip)
    game.changeMode((1280, 720), (1280, 720))
    events = []
    stars = Stars()
    pygame.mixer_music.load(os.path.join("assets", "music", "main_Menu.mp3"))
    pygame.mixer_music.play(-1)
    frame = 0
    while game.state == 0:
        playButton.update(events)
        creditsButton.update(events)
        fullScreenButton.update(events)
        closeButton.update(events)
        game.screen.fill((0, 0, 0))
        stars.render(game.screen)
        frame += 1  # frame +1 pour le vaisseau
        # affichage du vaisseau
        game.screen.blit(spaceShip, (300, 260 + math.sin(frame/80)*20))
        # affichage des boutons
        game.screen.blit(playButton.render(), playButton.position)
        game.screen.blit(creditsButton.render(), creditsButton.position)
        game.screen.blit(fullScreenButton.render(), fullScreenButton.position)
        game.screen.blit(closeButton.render(), closeButton.position)
        # gestion des événements
        for event in events:
            if event.type == creditsEvent:
                game.state = 3
                credits()
                game.changeMode((1280, 720), (1280, 720))
                game.state = 0
            if event.type == playEvent:
                # lancement du jeu
                pygame.mixer_music.fadeout(1000)
                game.state = 1
                # fenêtre pour le jeu
                game.changeMode((512, 288), (1280, 720))
                main.mainLoop(game)
                game.changeMode((1280, 720), (1280, 720))
                pygame.mixer_music.load(os.path.join(
                    "assets", "music", "main_Menu.mp3"))
                pygame.mixer_music.play(-1)
                game.state = 0

        game.waitFramerate()
        events = game.runEvents()


def credits():
    global game
    game.screen.fill((162, 155, 254))
    font40 = pygame.font.Font(None, 40)
    credit = 1
    game.screen.blit(font40.render("Developpeurs :",
                                   1, (255, 255, 255)), (480, 10))
    game.screen.blit(font40.render(
        "Nils PONSARD", 1, (255, 255, 255)), (510, 40))
    game.screen.blit(font40.render("Raphaël LESBROS",
                                   1, (255, 255, 255)), (510, 70))
    game.screen.blit(font40.render("Design Visuel :",
                                   1, (255, 255, 255)), (480, 120))
    game.screen.blit(font40.render("Raphaël LESBROS",
                                   1, (255, 255, 255)), (510, 150))
    game.screen.blit(font40.render("Nils PONSARD",
                                   1, (255, 255, 255)), (510, 180))
    game.screen.blit(font40.render("Léo MOUGIN",
                                   1, (255, 255, 255)), (510, 210))

    while credit == 1:
        events = game.runEvents()
        for event in events:
            if event.type == pygame.KEYUP:
                credit = 0
        events = []
        game.waitFramerate()
