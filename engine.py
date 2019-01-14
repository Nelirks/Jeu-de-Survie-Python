import pygame
import threading
import time
import os


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

    def __init__(self, resolution, framerate=50):
        """
        création de la fenêtre du jeu
        """
        self.width, self.height = resolution
        pygame.init()
        self.screen = pygame.display.set_mode(resolution)
        self.state = 1
        self.fpsfont = pygame.font.SysFont("monospace", 15)
        self.framerate = 50
        self.last = pygame.time.get_ticks()

    def runEvents(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.state = 0
        return events

    """
    test de trucs
    def removeOfRender(self, objet):
        '''
        enlève l'objet de la liste de rendu
        '''
        i = 0
        for ob in self.renderList:
            if ob == objet:
                self.renderList.pop(i)
                break

            i += 1

    def addToRender(self, objet, priority):
        i = 0
        max = 0
        for o in self.renderList:
            if o[0] > priority:
                break
            i += 1

        self.renderList.insert(i, [priority, objet])

    def render(self, showFps=False, waitFrame=True):
        for o in self.renderList:
            o[1].render()
        if showFps:
            label = self.fpsfont.render(str(self.fps), 1, (0, 255, 0))
            self.screen.blit(label, (self.width-40, 0))
        if waitFrame:
            self.waitFramerate()
    """

    def waitFramerate(self, showFps=False):
        pygame.display.flip()

        pygame.time.wait(int(1000/self.framerate -
                             (pygame.time.get_ticks() - self.last)))
        """
        while(pygame.time.get_ticks() - self.last < 1000/self.framerate):
            pass
            """
        self.fps = round(1000/(pygame.time.get_ticks() - self.last))

        self.last = pygame.time.get_ticks()
        if showFps:
            label = self.fpsfont.render(str(self.fps), 1, (0, 255, 0))
            self.screen.blit(label, (self.width-40, 0))
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
    egrid = []  # entitées
    width = 0  # taille prise par la carte sur x
    height = 0  # taille prise par la carte sur y
    size = []  # caractéristiques de la grille (largeur, hauteur)
    tileSize = 32  # lageur et longuer d'une texture de la carte
    path = ""  # chemin du fichier
    blockingTiles = ["0"]
    textures = dict()

    def __init__(self, path, mode="load", dimensions=(10, 10), tileSize=32, setNum="-1"):
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
            self.setNum = info.readline()
            info.close()

            solid = open(os.path.join(path, "solid"))  # grille "solide"
            line = solid.readline()
            while line != "":
                self.sgrid.append(line.split())
                line = solid.readline()
            solid.close()

            # grille des entitées
            entities = open(os.path.join(path, "entities"))
            line = entities.readline()
            while line != "":
                self.egrid.append(line.split())
                line = entities.readline()
            entities.close()

            self.loadTextures()

        elif mode == "new":  # création d'une nouvelle carte
            self.sgrid = doubleArraygen(dimensions[0], dimensions[1])
            self.egrid = doubleArraygen(dimensions[0], dimensions[1])
            self.size = dimensions
            self.width = dimensions[0] * self.tileSize
            self.height = dimensions[1] * self.tileSize
            self.setNum = setNum
            self.loadTextures()
        elif mode == "edit":
            info = open(os.path.join(path, "info"),
                        "r")   # obtention des infos
            self.size = info.readline().split()
            self.size = [int(self.size[0]), int(self.size[1])]
            self.width = self.size[0]*self.tileSize
            self.height = self.size[1]*self.tileSize
            self.setNum = info.readline()
            info.close()

            solid = open(os.path.join(path, "solid"))  # grille "solide"
            line = solid.readline()
            while line != "":
                self.sgrid.append(line.split())
                line = solid.readline()
            solid.close()

            # grille des entitées
            entities = open(os.path.join(path, "entities"))
            line = entities.readline()
            while line != "":
                self.egrid.append(line.split())
                line = entities.readline()
            entities.close()

            if setNum != "-1":
                self.setNum = setNum
            self.loadTextures()

        else:
            raise ValueError("invalid mode")

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
            self.textures[f.split(".")[0]] = pygame.image.load(
                os.path.join(path, f)).convert()

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
        info.write(self.setNum)
        info.close()

        solid = open(os.path.join(
            self.path, "solid"), "w")  # sauvegarder le fond d'écran
        for line in self.sgrid:
            for c in line:
                solid.write("{} ".format(c))
            solid.write("\n")
        solid.close()

        entities = open(os.path.join(
            self.path, "entities"), "w")  # sauvegarder les entitées
        for line in self.egrid:
            for c in line:
                entities.write("{} ".format(c))
            entities.write("\n")
        entities.close()

    def edit(self, x, y, textureIndex):
        self.sgrid[x][y] = textureIndex

    def collide(self, x, y, w):
        # cassé
        pass

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
        x = 0
        for line in self.sgrid:

            y = 0
            for p in line:
                # ajoute la texture à l'index p aux coordonnées x et y
                surface.blit(self.textures[p], (x, y))
                y += self.tileSize
            x += self.tileSize

        return surface
