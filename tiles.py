from importlib.util import set_loader
import pygame
import constants as con
import random as rand


def array_construct(char):
    res = []
    for i in range(con.ROW_COUNT):
        temp = []
        for j in range(con.COL_COUNT):
            temp.append(char)
        res.append(temp)
    return res


class Tiles:
    def __init__(self):
        self.height = con.TILE_SIZE * con.ROW_COUNT
        self.width = con.TILE_SIZE * con.COL_COUNT

        self.visible_floor = pygame.image.load(con.VISIBLE_FLOOR)
        self.hidden_floor = pygame.image.load(con.HIDDEN_FLOOR)
        self.wumpus = pygame.image.load(con.WUMPUS)
        self.pit = pygame.image.load(con.PIT)
        self.gold = pygame.image.load(con.GOLD)

        self.flag = False

        self.tiles_con = array_construct('h')
        self.tiles_con[0][0] = 'v'
        self.obstacle = array_construct('n')
        self.set_obstacle()

    def set_obstacle(self):

        self.set_value(con.WUMPUS_COUNT, "w")
        self.set_value(con.GOLD_COUNT, "g")
        self.set_value(con.PIT_COUNT, "p")

    def set_value(self, count, cls):
        for i in range(count):
            if cls == 'w':
                x = 1
            else:
                x = rand.randint(1, 9)
            y = rand.randint(1, 9)
            self.obstacle[x][y] = cls

    def text_view(self, surface):
        font = pygame.font.SysFont('arial', 10)
        breeze = font.render("BREEZE", False, con.BLACK, con.WHITE)
        stench = font.render("STENCH", False, con.BLACK, con.WHITE)
        lit = font.render("LIT", False, con.BLACK, con.WHITE)

        for i in range(con.ROW_COUNT):
            for j in range(con.COL_COUNT):
                if self.tiles_con[i][j] == 'h':
                    continue
                elif self.tiles_con[i][j] == 'v':
                    if i + 1 < 10 and self.obstacle[i + 1][j] == 'p':
                        surface.blit(breeze, (j * con.TILE_SIZE, i * con.TILE_SIZE))
                    elif j + 1 < 10 and self.obstacle[i][j + 1] == 'p':
                        surface.blit(breeze, (j * con.TILE_SIZE, i * con.TILE_SIZE))
                    elif i - 1 >= 0 and self.obstacle[i - 1][j] == 'p':
                        surface.blit(breeze, (j * con.TILE_SIZE, i * con.TILE_SIZE))
                    elif j - 1 >= 0 and self.obstacle[i][j - 1] == 'p':
                        surface.blit(breeze, (j * con.TILE_SIZE, i * con.TILE_SIZE))

                    if i + 1 < 10 and self.obstacle[i + 1][j] == 'w':
                        surface.blit(stench, (j * con.TILE_SIZE, i * con.TILE_SIZE + 52))
                    elif j + 1 < 10 and self.obstacle[i][j + 1] == 'w':
                        surface.blit(stench, (j * con.TILE_SIZE, i * con.TILE_SIZE + 52))
                    elif i - 1 >= 0 and self.obstacle[i - 1][j] == 'w':
                        surface.blit(stench, (j * con.TILE_SIZE, i * con.TILE_SIZE))
                    elif j - 1 >= 0 and self.obstacle[i][j - 1] == 'w':
                        surface.blit(stench, (j * con.TILE_SIZE, i * con.TILE_SIZE))

                    if self.obstacle[i][j] == 'g':
                        surface.blit(lit, (j * con.TILE_SIZE, i * con.TILE_SIZE + 26))

    def get_map(self, i, j):
        temp = []
        if i + 1 < con.ROW_COUNT and self.obstacle[i + 1][j] == 'p':
            temp.append('b')
        if i - 1 >= 0 and self.obstacle[i - 1][j] == 'p':
            temp.append('b')
        if j + 1 < con.COL_COUNT and self.obstacle[i][j + 1] == 'p':
            temp.append('b')
        if j - 1 >= 0 and self.obstacle[i][j - 1] == 'p':
            temp.append('b')

        if i + 1 < con.ROW_COUNT:
            if self.obstacle[i + 1][j] == 'w':
                temp.append('s')
        if i - 1 >= 0:
            if self.obstacle[i - 1][j] == 'w':
                temp.append('s')
        if j + 1 < con.COL_COUNT:
            if self.obstacle[i][j + 1] == 'w':
                temp.append('s')
        if j - 1 >= 0:
            if self.obstacle[i][j - 1] == 'w':
                temp.append('s')

        if self.obstacle[i][j] == 'g':
            temp.append('l')

        return temp

    def background(self, surface):
        for i in range(con.ROW_COUNT):
            for j in range(con.COL_COUNT):
                if self.tiles_con[i][j] == 'h':
                    surface.blit(self.hidden_floor, (j * con.TILE_SIZE, i * con.TILE_SIZE))
                    continue
                elif self.tiles_con[i][j] == 'v':
                    surface.blit(self.visible_floor, (j * con.TILE_SIZE, i * con.TILE_SIZE))
                    if self.obstacle[i][j] == 'p':
                        surface.blit(self.pit, (j * con.TILE_SIZE, i * con.TILE_SIZE))
                    elif self.obstacle[i][j] == 'w':
                        surface.blit(self.wumpus, (j * con.TILE_SIZE, i * con.TILE_SIZE))
                    elif self.obstacle[i][j] == 'g':
                        gold_back = pygame.image.load('./res/floor_gold.png')
                        surface.blit(gold_back, (j * con.TILE_SIZE, i * con.TILE_SIZE))
                        surface.blit(self.gold, (j * con.TILE_SIZE, i * con.TILE_SIZE))

        for i in range(con.ROW_COUNT):
            pygame.draw.line(surface, con.WHITE, (0, i * con.TILE_SIZE), (self.width, i * con.TILE_SIZE))
        pygame.draw.line(surface, con.WHITE, (0, self.height - 1), (self.width, self.height - 1))

        for i in range(con.COL_COUNT):
            pygame.draw.line(surface, con.WHITE, (i * con.TILE_SIZE, 0), (i * con.TILE_SIZE, self.height))
        pygame.draw.line(surface, con.WHITE, (self.width - 1, 0), (self.width - 1, self.height))

    def get_obstacles(self):
        return self.obstacle

    def get_gold(self, x, y):
        if self.obstacle[x][y] == 'g':
            self.obstacle[x][y] = 'n'
            return True

        else:
            return False