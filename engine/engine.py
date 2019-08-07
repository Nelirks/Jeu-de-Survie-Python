# coding: utf-8

import pygame
import threading
import time
import os
import pickle
import entities


class Engine:
    """
    classe de gestion de la fenêtre du jeu
    """
    width = 0
    height = 0
    state = 0
    # renderList = []
    fps = 0
    framerate = 50
    last = 0

    def __init__(self, resolution, targetResolution=(800, 600), framerate=50):
        """
        création de la fenêtre du jeu
        resolution : résolution de l'écran virtuel de rendu «Engine.screen» qui sera adapté à la résoltion cible : targetResolution
        """
        self.menuState = 0
        self.width, self.height = resolution
        self.fullscreenResolution = targetResolution
        self.resolution = resolution
        self.targetResolution = targetResolution
        self.fullscreen = 0
        pygame.init()
        self.initialMonitorresolution = (
            pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.realScreen = pygame.display.set_mode(
            targetResolution, pygame.NOFRAME)
        self.screen = pygame.surface.Surface(resolution)
        self.state = 1
        self.fpsfont = pygame.font.SysFont("monospace", 15)
        self.framerate = framerate
        self.last = pygame.time.get_ticks()
        self.initMenu()

    def initMenu(self):
        self.fullscreenEvent = pygame.USEREVENT + 1
        self.mainMenuEvent = pygame.USEREVENT + 4  # voir menu.py pour le +4
        self.fullscreenButton = Button(
            (490, 20), (300, 40),  "Plein Écran", self.fullscreenEvent, fontSize=30, background=(44, 62, 80, 255), focusedBackground=(84, 102, 80, 255))
        self.quitButton = Button(
            (490, 70), (300, 40),  "Retour au menu principal", self.mainMenuEvent, fontSize=30, background=(44, 62, 80, 255), focusedBackground=(84, 102, 80, 255))
        self.menu = Menu((480, 10), (320, 110),
                         (self.fullscreenButton, self.quitButton))

    def changeMode(self, renderResolution, targetResolution):
        if self.fullscreen == 1:
            self.realScreen = pygame.display.set_mode(
                targetResolution, pygame.FULLSCREEN)
        else:
            self.realScreen = pygame.display.set_mode(
                targetResolution, pygame.NOFRAME)
        self.resolution = renderResolution
        self.targetResolution = targetResolution
        self.screen = pygame.surface.Surface(renderResolution)

    def runEvents(self):
        events = pygame.event.get()
        if self.state == 2:
            self.menu.update(events)
        for event in events:
            if event.type == self.mainMenuEvent:
                self.state = 0
            elif event.type == self.fullscreenEvent:
                if self.fullscreen == 0:
                    pygame.display.set_mode(
                        self.fullscreenResolution, pygame.FULLSCREEN)
                    self.fullscreen = 1
                else:
                    pygame.display.set_mode(
                        self.targetResolution, pygame.NOFRAME)
                    self.fullscreen = 0
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_F11:
                    if self.fullscreen == 0:
                        pygame.display.set_mode(
                            self.fullscreenResolution, pygame.FULLSCREEN)
                        self.fullscreen = 1
                    else:
                        pygame.display.set_mode(
                            self.targetResolution, pygame.NOFRAME)
                        self.fullscreen = 0

                if event.key == pygame.K_ESCAPE:
                    if self.state == 1:
                        self.state = 2  # pause
                        self.menuState = 1
                    elif self.state == 0:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
                    elif self.state == 2:
                        if self.menuState == 1:
                            self.state = 1
                            self.menuState = 0
                        else:
                            self.menuState -= 1
                if event.key == pygame.K_F12:
                    self.state = -1
            elif event.type == pygame.QUIT:
                self.state = -1
        # if self.state == 2:  # si le jeu est en pause
        #    return []
        # else:
        return events

    def waitFramerate(self, showFps=False):

        pygame.time.wait(int(1000/self.framerate -
                             (pygame.time.get_ticks() - self.last)))
        """
        while(pygame.time.get_ticks() - self.last < 1000/self.framerate):
            pass
            """
        # if self.menuState == 1:

        self.fps = round(1000/(pygame.time.get_ticks() - self.last))

        self.last = pygame.time.get_ticks()
        if showFps:
            label = self.fpsfont.render(str(self.fps), 1, (0, 255, 0))
            self.screen.blit(label, (0, 0))
        pygame.transform.scale(
            self.screen, self.targetResolution, self.realScreen)
        if self.state == 2 and self.menuState == 1:
            self.menu.render(self.realScreen)
        pygame.display.flip()
        return self.fps


class Menu:
    def __init__(self, position, size, elements=[], background=(0, 0, 0, 255)):
        self.elements = elements
        self.size = size
        self.position = position
        self.background = background
        self.rect = pygame.rect.Rect(position, size)

    def update(self, events):
        for element in self.elements:
            element.update(events)

    def render(self, surface):
        pygame.draw.rect(surface, self.background, self.rect)
        for element in self.elements:
            surface.blit(element.render(), element.position)


class GUIElement:
    """classe de base pour les éléments interactifs (boutons et compagnie)
    """

    def __init__(self, position, size, text, background=(0, 0, 0, 0), focusedBackground=(100, 100, 100, 50), font=None, fontSize=10, fontColor=(255, 255, 255, 255)):  # position is for mouse hitbox
        self.size = size
        self.focused = 0
        self.position = position
        self.text = text
        self.background = background
        self.focusedBackground = focusedBackground

        self.surface = pygame.surface.Surface(
            size, pygame.SRCALPHA, 32).convert_alpha()
        self.font = pygame.font.Font(font, fontSize)
        self.fontColor = fontColor
        self.rect = pygame.rect.Rect(position, size)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                mouse = pygame.rect.Rect(pygame.mouse.get_pos(), (1, 1))

                if mouse.colliderect(self.rect):
                    self.focused = 1
                else:
                    self.focused = 0

    def render(self):
        background = self.background
        if self.focused == 1:
            background = self.focusedBackground
        self.surface.fill(background)

        # TO DO : center text
        color = pygame.color.Color(
            self.fontColor[0], self.fontColor[1], self.fontColor[2], self.fontColor[3])
        font = self.font.render(self.text, 1, color).convert_alpha()
        self.surface.blit(font, (2, 2))
        return self.surface


class Button(GUIElement):
    def __init__(self, position, size, text, eventOnClicked, background=(0, 0, 0, 0), focusedBackground=(100, 100, 100, 50), font=None, fontSize=20, fontColor=(255, 255, 255, 255)):
        self.eventOnClicked = pygame.event.Event(eventOnClicked)

        super().__init__(position, size, text, background=background,
                         focusedBackground=focusedBackground, font=font, fontSize=fontSize, fontColor=fontColor)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                mouse = pygame.rect.Rect(pygame.mouse.get_pos(), (1, 1))

                if mouse.colliderect(self.rect):
                    self.focused = 1
                else:
                    self.focused = 0
            if event.type == pygame.MOUSEBUTTONDOWN:

                if self.focused == 1:
                    pygame.event.post(self.eventOnClicked)


class KeyCustomizerButton(Button):
    def __init__(self, position, size, defaultKey, defaultKeyUnicode, background=(0, 0, 0, 0), focusedBackground=(100, 100, 100, 50), font=None, fontSize=20, fontColor=(255, 255, 255, 255)):
        self.key = defaultKey
        self.editMode = 0
        super().__init__(position, size, defaultKeyUnicode, 0, background=background,
                         focusedBackground=focusedBackground, font=font, fontSize=fontSize, fontColor=fontColor)

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.editMode:
                    self.key = event.key
                    self.editMode = 0
                    self.text = event.unicode
                    if event.key == pygame.K_UP:
                        self.text = "up"
                    if event.key == pygame.K_DOWN:
                        self.text = "down"
                    if event.key == pygame.K_RIGHT:
                        self.text = "right"
                    if event.key == pygame.K_LEFT:
                        self.text = "left"
            if event.type == pygame.MOUSEMOTION:
                mouse = pygame.rect.Rect(pygame.mouse.get_pos(), (1, 1))
                if mouse.colliderect(self.rect):
                    self.focused = 1
                else:
                    self.focused = 0
            if event.type == pygame.MOUSEBUTTONDOWN:

                if self.focused == 1:
                    self.editMode = 1
                    self.text = "..."
                else:
                    self.editMode = 0

        return self.key
