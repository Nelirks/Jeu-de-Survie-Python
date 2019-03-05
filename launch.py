import pygame
import main
import engine
game = engine.Engine((1280, 720),
                     (1280, 720), framerate=50)  # fenêtre 1:1
game.state = 0

playEvent = pygame.USEREVENT + 2

playButton = engine.Button(
    (200, 50), (10, 10), "jouer", playEvent, fontSize=60)

events = []
while game.state == 0:
    playButton.update(events)
    game.screen.blit(playButton.render(), playButton.position)
    for event in events:
        if event.type == playEvent:
            game.state = 1
            game = engine.Engine((512, 288),
                                 (1280, 720), framerate=50)  # fenêtre
            main.mainLoop(game)
    game.waitFramerate()
    events = game.runEvents()
