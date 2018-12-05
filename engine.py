import pygame


def doubleArraygen(x, y):
    array = []
    for i in range(x):
        line = []
        for j in range(y):
            line.append("0")
        array.append(line)
    return array


class Map:
    grid = []
    width = 0
    height = 0
    tileSize = 64
    path = ""

    def __init__(self, path, mode="load", dimensions=(10, 10), tileSize=64):
        self.grid = []
        self.tileSize = tileSize
        self.path = path
        if mode == "load":
            with open(path, "r") as file:
                self.grid = []
                line = file.readline()
                (self.width, self.height) = line.split()
                self.width = int(self.width)
                self.height = int(self.height)
                line = file.readline()
                while line != "":
                    self.grid.append(line.split())
                    line = file.readline()
        elif mode == "new":
            self.grid = doubleArraygen(dimensions[0], dimensions[1])
            self.width = dimensions[0]
            self.height = dimensions[1]
        elif mode == "edit":
            with open(path, "r") as file:
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
        with open(self.path, "w") as file:
            file.write("{} {}\n".format(self.width, self.height))
            for line in self.grid:
                for c in line:
                    file.write("{} ".format(c))
                file.write("\n")

    def edit(self, x, y, textureIndex):
        self.grid[x][y] = textureIndex

    def render(self, textures):
        surface = pygame.Surface(
            (self.width*self.tileSize, self.height*self.tileSize))
        x = 0
        for l in self.grid:
            y = 0
            for p in l:
                surface.blit(textures[p], (x, y))
                y += self.tileSize
            x += self.tileSize
        return surface
