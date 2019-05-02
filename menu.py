import pygame
import main
import os
import random
import math
import engine
import pickle


class Star:

    def __init__(self, position, size, speed=(-2, 0)):
        self.speed = [0, 0]
        self.speed[1] = speed[1]
        self.speed[0] = speed[0]*size
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
    inter = 8
    liste = []
    line = 5
    frame = 0

    def render(self, surface):
        if self.frame % self.inter == 0:
            width = surface.get_width()
            height = surface.get_height()
            for i in range(self.line):
                x = width + random.randint(-10, 10)
                y = random.randint(10, height-10)
                self.liste.append(Star((x, y), random.randint(1, 6)))
        i = 0
        out = self.liste
        for s in self.liste:
            s.render(surface)
            s.update()
            if self.liste[i].x < 0:
                out.pop(i)
            i += 1
        self.frame += 1
        self.liste = out


game = engine.Engine((1280, 720),
                     (1280, 720), framerate=100)  # fenêtre 1:1 pour les boutons
game.state = 0

playerKeyConfig = {
    "left": pygame.K_q,
    "right": pygame.K_d,
    "down": pygame.K_s,
    "up": pygame.K_z,
    "useRight": pygame.K_r,
    "useLeft": pygame.K_a,
    "openCraft": pygame.K_e
}
playerKeyConfigUnicode = {
    "left": "q",
    "right": "d",
    "down": "s",
    "up": "z",
    "useRight": "r",
    "useLeft": "a",
    "openCraft": "e"
}
if (os.path.isfile("keys") == False):
    file = open("keys", "wb")
    pickle.dump((playerKeyConfig, playerKeyConfigUnicode), file)
    file.close()
else:
    file = open("keys", "rb")
    out = pickle.load(file)
    file.close()
    playerKeyConfig = out[0]
    playerKeyConfigUnicode = out[1]

playEvent = pygame.USEREVENT + 4
creditsEvent = pygame.USEREVENT + 3
settingsEvent = pygame.USEREVENT + 2


playButton = engine.Button(
    (10, 10), (130, 50),  "Jouer", playEvent, fontSize=60, focusedBackground=(100, 100, 100))
creditsButton = engine.Button(
    (10, 70), (110, 40),  "Crédits", creditsEvent, fontSize=40, focusedBackground=(100, 100, 100))
fullScreenButton = engine.Button((10, 120), (170, 40), "Plein Écran",
                                 game.fullscreenEvent, fontSize=40, focusedBackground=(100, 100, 100))
settingsButton = engine.Button((10, 170), (170, 40), "Paramètres",
                               settingsEvent, fontSize=40, focusedBackground=(100, 100, 100))
closeButton = engine.Button(
    (10, 220), (240, 40),  "Retour au bureau", pygame.QUIT, fontSize=40, focusedBackground=(100, 100, 100))


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
        settingsButton.update(events)
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
        game.screen.blit(settingsButton.render(), settingsButton.position)
        game.screen.blit(closeButton.render(), closeButton.position)
        # gestion des événements
        for event in events:
            if event.type == creditsEvent:
                game.state = 3
                credits()
                game.changeMode((1280, 720), (1280, 720))
                game.state = 0
            if event.type == settingsEvent:
                game.state = 3
                settings()
                game.state = 0

            if event.type == playEvent:
                # lancement du jeu
                pygame.mixer_music.fadeout(1000)
                game.state = 1
                # fenêtre pour le jeu
                game.changeMode((512, 288), (1280, 720))
                main.mainLoop(game, playerKeyConfig)
                game.changeMode((1280, 720), (1280, 720))
                pygame.mixer_music.load(os.path.join(
                    "assets", "music", "main_Menu.mp3"))
                pygame.mixer_music.play(-1)
                game.state = 0

        game.waitFramerate()
        events = game.runEvents()


def settings():
    global game

    font40 = pygame.font.Font(None, 40)
    game.screen.fill((0, 0, 0))
    font30 = pygame.font.Font(None, 30)
    setting = 1
    # configuration du bouton retour
    backEvent = pygame.USEREVENT + 5
    backButton = engine.Button(
        (0, 690), (100, 30), "Retour", backEvent, fontSize=30)

    # configuration des configurateurs de touches
    # mouvements
    editUpButton = engine.KeyCustomizerButton(
        (490, 40), (100, 50), playerKeyConfig["up"], playerKeyConfigUnicode["up"], fontSize=50, background=(100, 100, 100))
    editDownButton = engine.KeyCustomizerButton(
        (490, 100), (100, 50), playerKeyConfig["down"], playerKeyConfigUnicode["down"], fontSize=50, background=(100, 100, 100))
    editLeftButton = engine.KeyCustomizerButton(
        (490, 160), (100, 50), playerKeyConfig["left"], playerKeyConfigUnicode["left"], fontSize=50, background=(100, 100, 100))
    editRightButton = engine.KeyCustomizerButton(
        (490, 220), (100, 50), playerKeyConfig["right"], playerKeyConfigUnicode["right"], fontSize=50, background=(100, 100, 100))
    # objets
    editORightButton = engine.KeyCustomizerButton(
        (490, 280), (100, 50), playerKeyConfig["useRight"], playerKeyConfigUnicode["useRight"], fontSize=50, background=(100, 100, 100))
    editOLeftButton = engine.KeyCustomizerButton(
        (490, 340), (100, 50), playerKeyConfig["useLeft"], playerKeyConfigUnicode["useLeft"], fontSize=50, background=(100, 100, 100))
    editCraftButton = engine.KeyCustomizerButton(
        (490, 400), (100, 50), playerKeyConfig["openCraft"], playerKeyConfigUnicode["openCraft"], fontSize=50, background=(100, 100, 100))
    while setting == 1:
        events = game.runEvents()
        game.screen.fill((0, 0, 0))  # effacer l'écran
        game.screen.blit(font40.render(
            "Touches :", 1, (255, 255, 255)), (480, 10))
        game.screen.blit(font30.render(
            "Haut :", 1, (255, 255, 255)), (400, 50))
        game.screen.blit(font30.render(
            "Bas :", 1, (255, 255, 255)), (400, 110))
        game.screen.blit(font30.render(
            "Gauche :", 1, (255, 255, 255)), (400, 170))
        game.screen.blit(font30.render(
            "Droite :", 1, (255, 255, 255)), (400, 230))
        game.screen.blit(font30.render(
            "Objet droite :", 1, (255, 255, 255)), (350, 290))
        game.screen.blit(font30.render(
            "Objet gauche :", 1, (255, 255, 255)), (350, 350))
        game.screen.blit(font30.render(
            "Menu Craft :", 1, (255, 255, 255)), (350, 410))
        # bouton retour
        game.screen.blit(backButton.render(), backButton.position)
        backButton.update(events)
        # affichage des configurateurs des touches
        game.screen.blit(editUpButton.render(), editUpButton.position)
        game.screen.blit(editLeftButton.render(), editLeftButton.position)
        game.screen.blit(editRightButton.render(), editRightButton.position)
        game.screen.blit(editDownButton.render(), editDownButton.position)
        game.screen.blit(editORightButton.render(), editORightButton.position)
        game.screen.blit(editOLeftButton.render(), editOLeftButton.position)
        game.screen.blit(editCraftButton.render(), editCraftButton.position)
        # actualisation des configurateurs des touches
        playerKeyConfig["left"] = editLeftButton.update(events)
        playerKeyConfig["down"] = editDownButton.update(events)
        playerKeyConfig["right"] = editRightButton.update(events)
        playerKeyConfig["up"] = editUpButton.update(events)
        playerKeyConfig["useRight"] = editORightButton.update(events)
        playerKeyConfig["useLeft"] = editOLeftButton.update(events)
        playerKeyConfig["openCraft"] = editCraftButton.update(events)
        for event in events:

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    events = []
                    setting = 0
            if event.type == backEvent:
                events = []
                setting = 0
        events = []
        game.waitFramerate()
    playerKeyConfigUnicode["left"] = editLeftButton.text
    playerKeyConfigUnicode["right"] = editRightButton.text
    playerKeyConfigUnicode["up"] = editUpButton.text
    playerKeyConfigUnicode["down"] = editDownButton.text
    playerKeyConfigUnicode["useLeft"] = editOLeftButton.text
    playerKeyConfigUnicode["useRight"] = editORightButton.text
    playerKeyConfigUnicode["openCraft"] = editCraftButton.text
    file = open("keys", "wb")
    pickle.dump((playerKeyConfig, playerKeyConfigUnicode), file)
    file.close()


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
    game.screen.blit(font40.render("Son :",
                                   1, (255, 255, 255)), (480, 260))
    game.screen.blit(font40.render("Nicolas PASSINI",
                                   1, (255, 255, 255)), (510, 290))
    while credit == 1:
        events = game.runEvents()
        for event in events:
            if event.type == pygame.KEYUP:
                credit = 0
        events = []
        game.waitFramerate()
