# coding: utf-8

import pygame
import threading
import time
import os
import pickle
import entities
import math


def simplify(list):
    """
    renvoi une liste avec aucun élément identique
    """
    out = tuple
    for i in list:
        added = False
        for j in out:
            if i == j:
                added = True
        if added == False:
            out.append(i)
    return out


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


    doc dans /assets/chuncks/readme.md


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

    def __init__(self, zone, mode="load", dimensions=(10, 10), setNum="-1", playerPosition=(0, 0)):
        """
        __init__(path, mode="load", dimensions=(10, 10), )  : création de l'objet carte
            path : chemin d'accès ,
            mode : ["load" / "new" / "edit" ] charger / créer / éditer , charger (load) par défaut
            dimensions : taille en x et y
        """

        self.grid = []
        self.tileSize = tileSize = 32
        self.zone = zone
        path = os.path.join("assets", "chuncks", zone)
        # détection du mode

        """
        les données de la carte sont stockées dans un dossier avec :
            un fichier info contenant la largeur et la longuer, le numéro du set de textures
            un fichier solid contenant la grille de la carte (arrière plan)
            un fichier entities contenant la grille des entitées (premier plan , ex : arbres, monstres)
        """
        if mode == "load":
            info = open(os.path.join(path, "info"),
                        "rb")   # obtention des infos
            inf = pickle.load(info)  # nombre de chuncks
            self.size = inf[0:1]
            # nombre de tuiles
            self.width = self.size[0]*16
            self.height = self.size[1]*16
            self.setNum = inf[3]
            self.playerPosition = playerPosition
            info.close()

            self.loadChuncks()

            self.loadTextures()

            self.renderChuncksSolid()

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

    def loadChuncks(self):
        # charger les infos des chuncks
        path = os.path.join("assets", "chuncks", self.zone)
        self.chuncks = []
        for y in range(0, self.size[1]):
            line = []
            for x in range(0, self.size[0]):
                file = open(os.path.join(
                    path, "{}.{}.chunck".format(x, y)), "rb")
                line.append(pickle.load(file))
            self.chuncks.append(line)

    def get_rects(self, playerPosition):
        """
        renvoi les hitboxs du chunck dans une ligne 
        playerPosition : [x,y]
        """
        # déterminer le chunck en question
        cx = math.floor(playerPosition[0]/(16*self.tileSize))
        cy = math.floor(playerPosition[1]/(16*self.tileSize))
        # récupérer le chunck
        chunck = self.chuncks[cy][cx]
        solid = chunck["solid"]

        # trouver les colisions
        x = 0
        liste = []
        for l in solid:
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
        bfile = open(os.path.join(path, "blockingTiles.txt"), "r")
        line = bfile.readline()
        allStr = ""
        while line != "":
            allStr += line
            line = bfile.readline()
        self.blockingTiles = allStr.split("\n")
        bfile.close()

    def renderChuncksSolid(self):
        self.renderedChuncks = []
        for line in self.chuncks:
            RenderedLine = []
            for c in line:
                solid = c["solid"]
                surface = pygame.surface.Surface(
                    (self.tileSize*16, self.tileSize*16))
                x = 0
                for l in solid:
                    y = 0
                    for p in l:
                        # ajoute la texture à l'index p aux coordonnées x et y
                        surface.blit(self.textures[p], (x, y))
                        y += self.tileSize
                    x += self.tileSize
                RenderedLine.append(surface)
            self.renderedChuncks.append(RenderedLine)

    def save(self):
        pass

    def render(self, playerPosition, screenSize=[16, 6]):
        """
        gère l'affichage autour du personnage
        playerPosition est la position du personnage dans la zone (au centre de l'écran)
        """
        # chercher les chuncks à afficher
        x = playerPosition[0]
        y = playerPosition[1]

        xmin = math.floor(x - screenSize[0]/2 * 32)
        ymin = math.floor(y - screenSize[1]/2 * 32)
        xmax = math.floor(x + screenSize[0]/2 * 32)
        ymax = math.floor(y + screenSize[1]/2 * 32)

        xmin = math.floor(max(0, xmin)/(16*32))
        ymin = math.floor(max(0, ymin)/(16*32))
        xmax = math.floor(min(ymax, self.size[0]*16*32)/(16*32))
        ymin = math.floor(min(ymin, self.size[1]*16*32)/(16*32))

        # liste des chuncks à rendre (4 max pour 4 coins: haut gauche, bas gauche, haut droite,bas droite)
        chuncks = [self.chuncks[xmin][ymin],
                   self.chuncks[xmin][ymax], self.chuncks[xmax][ymin], self.chuncks[xmax][ymax]]
        chuncks = simplify(chuncks)  # enlever les doubles
        organised = [["", ""], ["", ""]]
