import pygame
import main
import engine
game = engine.Engine((1280, 720),
                     (1280, 720), framerate=50)  # fenêtre 1:1 pour les boutons
game.state = 0

playEvent = pygame.USEREVENT + 2
creditsEvent = pygame.USEREVENT + 3


playButton = engine.Button(
    (10, 10), (200, 50),  "Jouer", playEvent, fontSize=60)
creditsButton = engine.Button(
    (10, 70), (110, 40),  "Crédits", creditsEvent, fontSize=40)
closeButton = engine.Button(
    (10, 120), (250, 40),  "Retour au bureau", pygame.QUIT, fontSize=40)


def mainMenu():
    global game
    game.state = 0
    game.changeMode((1280, 720), (1280, 720))
    events = []
    while game.state == 0:
        playButton.update(events)
        creditsButton.update(events)
        closeButton.update(events)
        game.screen.fill((50, 50, 0))
        game.screen.blit(playButton.render(), playButton.position)
        game.screen.blit(creditsButton.render(), creditsButton.position)
        game.screen.blit(closeButton.render(), closeButton.position)
        for event in events:
            if event.type == creditsEvent:
                game.state = 3
                credits()
                game.changeMode((1280, 720), (1280, 720))
                game.state = 0
            if event.type == playEvent:
                game.state = 1
                # fenêtre pour le jeu
                game.changeMode((512, 288), (1280, 720))
                main.mainLoop(game)
                game.changeMode((1280, 720), (1280, 720))
                game.state = 0

        game.waitFramerate(showFps=True)
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
