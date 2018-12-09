import pygame


class Engine:
    width = 0
    height = 0
    state = 0
    renderList = []
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

    def waitFramerate(self):

        while(pygame.time.get_ticks() - self.last < 1000/self.framerate):
            pass
        self.fps = round(1000/(pygame.time.get_ticks() - self.last))

        self.last = pygame.time.get_ticks()
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
    Objet Carte : permet de charger une carte à partir d'un fichier, de l'afficher et d'en créer une.
    Méthodes :
        - Carte(path, mode="load", dimensions=(10, 10), tileSize=64)  : création de l'objet carte
            path : chemin d'accès ,
            mode : [load / new / edit] charger / créer / éditer
            dimensions : taille en x et y
        - carte.save(): sauvegare de la carte à l'emplacement spécifié lors de la création
        - carte.edit(x,y,textureIndex) : self.grid[x][y] = textureIndex
            textureIndex : chaîne de caractères
        - carte.render(textures) : renvoi un objet surface de la librairie Pygame avec le rendu de la carte
            textures : dictionnaire des différentes textures référencés dans le fichier carte,
                il doit contenir au moins une surface pour l'index "0" 
                exemple : textures =   {"0": SurfaceEau,
                                        "1": SurfaceTerre, 
                                        "arbre": SurfaceArbre} 
    """
    grid = []
    width = 0  # taille suivant x
    height = 0  # taille suivant y
    tileSize = 64  # lageur et longuer d'une texture de la carte
    path = ""  # chemin du fichier

    def __init__(self, path, mode="load", dimensions=(10, 10), tileSize=64):
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
        if mode == "load":
            with open(path, "r") as file:  # ouverture du fichier
                self.grid = []
                line = file.readline()
                (self.width, self.height) = line.split()
                self.width = int(self.width)
                self.height = int(self.height)
                line = file.readline()
                while line != "":
                    self.grid.append(line.split())
                    line = file.readline()
        elif mode == "new":  # création d'une nouvelle carte
            self.grid = doubleArraygen(dimensions[0], dimensions[1])
            self.width = dimensions[0]
            self.height = dimensions[1]
        elif mode == "edit":
            with open(path, "r") as file:  # ouverture du fichier
                self.grid = []
                line = file.readline()
                (self.width, self.height) = line.split()
                self.width = int(self.width)
                self.height = int(self.height)
                line = file.readline()
                while line != "":
                    self.grid.append(line.split())
                    line = file.readline()

        else:
            raise ValueError("invalid mode")

    def save(self):
        """Sauvegare de la carte à l'emplacement spécifié lors de la création"""
        with open(self.path, "w") as file:  # sauvegarder à l'emplacement défini dans path
            file.write("{} {}\n".format(self.width, self.height))
            for line in self.grid:
                for c in line:
                    file.write("{} ".format(c))
                file.write("\n")

    def edit(self, x, y, textureIndex):
        self.grid[x][y] = textureIndex

    def render(self, textures):
        """carte.render(textures) : renvoi un objet surface de la librairie Pygame avec le rendu de la carte
            textures : dictionnaire des différentes textures référencés dans le fichier carte,
                il doit contenir au moins une surface pour l'index "0" 
                exemple : textures =   {"0": SurfaceEau,
                                        "1": SurfaceTerre, 
                                        "arbre": SurfaceArbre} 
        """
        surface = pygame.Surface(
            (self.width*self.tileSize, self.height*self.tileSize))  # surface où va être rendu la carte
        x = 0
        for l in self.grid:
            y = 0
            for p in l:
                # ajoute la texture à l'index p aux coordonnées x et y
                surface.blit(textures[p], (x, y))
                y += self.tileSize
            x += self.tileSize
        return surface
