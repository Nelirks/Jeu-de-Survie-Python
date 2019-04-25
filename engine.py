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


def doubleArraygen(x, y):
    """
    Générateur de tableau à deux entrées rempli de base de "0"
    usage : doubleArraygen(largeur (x) , longueur (y) )
    """
    array = []
    for i in range(x):
        line = []
        for j in range(y):
            line.append("0")
        array.append(line)
    return array


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


class Carte:
    """
    Objet Carte : permet de charger une carte à partir d'un fichier, de l'afficher et d'en créer une. À faire avant tout le reste (la taille reste modifiable).
    Méthodes :
        - Carte(path, mode="load", dimensions=(10, 10),setnum="-1", tileSize=32)  : création de l'objet carte
            path : chemin d'accès ,
            mode : [load / new / edit] charger / créer / éditer
            dimensions : taille en x et y
            setNum : nom /numéro du set de textures (dossier) à charger -1 veut dire de prendre la valeur déjà existante
        - carte.save(): sauvegare de la carte à l'emplacement spécifié lors de la création
        - carte.edit(x,y,textureIndex) : self.sgrid[x][y] = textureIndex
            textureIndex : chaîne de caractères
        - carte.render(textures) : renvoi un objet surface de la librairie Pygame avec le rendu de la carte
            textures : dictionnaire des différentes textures référencés dans le fichier carte,
                il doit contenir au moins une surface pour l'index "0"
                exemple : textures =   {"0": SurfaceEau,
                                        "1": SurfaceTerre,
                                        "arbre": SurfaceArbre}
    """
    sgrid = []  # fond "solide"
    entities = []  # entitées
    width = 0  # taille prise par la carte sur x
    height = 0  # taille prise par la carte sur y
    size = []  # caractéristiques de la grille (largeur, hauteur)
    tileSize = 32  # lageur et longuer d'une texture de la carte
    path = ""  # chemin du fichier
    blockingTiles = ["0"]
    textures = dict()

    def __init__(self, path, mode="load", dimensions=(10, 10), tileSize=32, setNum="-1", playerPosition=(0, 0)):
        """
        __init__(path, mode="load", dimensions=(10, 10), tileSize=64)  : création de l'objet carte
            path : chemin d'accès ,
            mode : ["load" / "new" / "edit" ] charger / créer / éditer , charger (load) par défaut
            dimensions : taille en x et y
        """
        
        self.grid = []
        self.tileSize = tileSize
        self.path = path
        # détection du mode

        """
        les données de la carte sont stockées dans un dossier avec :
            un fichier info contenant la largeur et la longuer, le numéro du set de textures
            un fichier solid contenant la grille de la carte (arrière plan)
            un fichier entities contenant la grille des entitées (premier plan , ex : arbres, monstres)
        """
        if mode == "load":
            info = open(os.path.join(path, "info"),
                        "r")   # obtention des infos
            self.size = info.readline().split()
            self.size = [int(self.size[0]), int(self.size[1])]
            self.width = self.size[0]*self.tileSize
            self.height = self.size[1]*self.tileSize
            self.setNum = int(info.readline().split(" ")[0])
            pPosStr = info.readline()
            px = int(pPosStr.split(" ")[0])
            py = int(pPosStr.split(" ")[1])
            self.playerPosition = (px, py)
            info.close()

            solid = open(os.path.join(path, "solid"), "rb")  # grille "solide"
            self.sgrid = pickle.load(solid)
            solid.close()

            # grille des entitées
            entities = open(os.path.join(path, "entities"), "rb")
            self.entities = pickle.load(entities)

            entities.close()

            self.loadTextures()

        elif mode == "new":  # création d'une nouvelle carte
            self.sgrid = doubleArraygen(dimensions[0], dimensions[1])
            self.entities = []
            self.size = dimensions
            self.width = dimensions[0] * self.tileSize
            self.height = dimensions[1] * self.tileSize
            self.setNum = setNum
            self.playerPosition = playerPosition
            self.loadTextures()
        elif mode == "edit":
            info = open(os.path.join(path, "info"),
                        "r")   # obtention des infos
            self.size = info.readline().split()
            self.size = [int(self.size[0]), int(self.size[1])]
            self.width = self.size[0]*self.tileSize
            self.height = self.size[1]*self.tileSize
            self.setNum = int(info.readline().split(" ")[0])
            pPosStr = info.readline()
            px = int(pPosStr.split(" ")[0])
            py = int(pPosStr.split(" ")[1])
            self.playerPosition = (px, py)
            info.close()

            solid = open(os.path.join(path, "solid"), "rb")  # grille "solide"
            self.sgrid = pickle.load(solid)
            solid.close()

            # grille des entitées
            entities = open(os.path.join(path, "entities"), "rb")
            self.entities = pickle.load(entities)
            entities.close()

            if setNum != "-1":
                self.setNum = setNum

            self.loadTextures()

        else:
            raise ValueError("invalid mode")

    def get_rects(self):
        x = 0
        liste = []
        for l in self.sgrid:
            y = 0
            for s in l:
                for c in self.blockingTiles:
                    if c == s:
                        liste.append(pygame.rect.Rect(
                            x, y, self.tileSize, self.tileSize))
                y += self.tileSize
            x += self.tileSize
        for en in self.entities:
            liste.append(en.rect)
        return liste

    def loadTextures(self):
        """
        charge les textures du set
        note : il ne doit pas avoir d'autres points que le .png dans le nom de chaque image
        il doit obligatoirement avoir une texture par défaut «0.png»
        """
        path = os.path.join(os.path.curdir, "assets", "sets", str(self.setNum))
        # trouve tous les fichiers dans le dossier sans les dossiers
        textureList = [f for f in os.listdir(
            path) if os.path.isfile(os.path.join(path, f))]
        self.textures = dict()
        for f in textureList:
            # charger les textures en les optimisant
            if(f != "blockingTiles.txt"):
             self.textures[f.split(".")[0]] = pygame.image.load(
                os.path.join(path, f)).convert()
        savedEntities = self.entities
        self.entities = []
        for entity in savedEntities:
            self.entities.append(entity.transform())
        bfile = open(os.path.join(path,"blockingTiles.txt"),"r")
        self.blockingTiles = bfile.readlines()
        bfile.close()
        

    def save(self):
        """Sauvegarde de la carte à l'emplacement spécifié lors de la création"""

        """
        les données de la carte sont stockées dans un dossier avec :
            un fichier info contenant la largeur et la longuer, le numéro du set de textures
            un fichier solid contenant la grille de la carte (arrière plan)
            un fichier entities contenant la grille des entitées (premier plan , ex : arbres, monstres)
        """

        if not os.path.exists(self.path):
            os.makedirs(self.path)
        info = open(os.path.join(self.path, "info"),
                    "w")  # sauvagarder les infos
        info.write("{} {}\n".format(self.size[0], self.size[1]))
        info.write("{} \n".format(self.setNum))
        info.write("{} {} ".format(
            self.playerPosition[0], self.playerPosition[1]))
        info.close()

        solid = open(os.path.join(
            self.path, "solid"), "wb")  # sauvegarder le fond d'écran
        pickle.dump(self.sgrid, solid)
        solid.close()

        entitiesFile = open(os.path.join(
            self.path, "entities"), "wb")  # sauvegarder les entitées
        saveEntities = []
        for entity in self.entities:
            saveEntities.append(entities.SavableEntity(
                entity.name, entity.rect.x, entity.rect.y))

        pickle.dump(saveEntities, entitiesFile)
        entitiesFile.close()

    def edit(self, x, y, textureIndex):
        self.sgrid[x][y] = textureIndex

    def renderThread(self, line, surface, x):
        y = 0
        for p in line:
            # ajoute la texture à l'index p aux coordonnées x et y
            surface.blit(self.textures[p], (x, y))
            y += self.tileSize

    def render(self, surface):
        """carte.render(surface) : renvoi un objet surface de la librairie Pygame avec le rendu de la carte
        """
        x = 0
        for line in self.sgrid:

            y = 0
            for p in line:
                # ajoute la texture à l'index p aux coordonnées x et y
                surface.blit(self.textures[p], (x, y))
                y += self.tileSize
            x += self.tileSize
        for en in self.entities:
            en.render(surface)

        return surface

    def renderSurface(self):
        """carte.renderSurface() : renvoi un objet surface de la librairie Pygame avec le rendu de la carte
            textures : dictionnaire des différentes textures référencés dans le fichier carte,
                il doit contenir au moins une surface pour l'index "0"
                exemple : textures =   {"0": SurfaceEau,
                                        "1": SurfaceTerre,
                                        "arbre": SurfaceArbre}
        """
        surface = pygame.surface.Surface((self.width, self.height))
        self.render(surface)

        return surface
