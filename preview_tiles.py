import pygame
import constants as con
import random as rand


class Preview_Tiles:
    def __init__(self, tiles):
        self.height = con.PREVIEW_TILE_SIZE * con.ROW_COUNT
        self.width = con.PREVIEW_TILE_SIZE * con.COL_COUNT

        self.visible_floor = pygame.image.load(con.PREVIEW_VISIBLE_FLOOR)
        self.wumpus = pygame.image.load(con.PREVIEW_WUMPUS)
        self.pit = pygame.image.load(con.PREVIEW_PIT)
        self.gold = pygame.image.load(con.PREVIEW_GOLD)
        self.floor_gold = pygame.image.load(con.PREVIEW_GOLD_FLOOR)

        self.flag = False
        self.obstacle = tiles.obstacle

    def background(self, surface):
        for i in range(con.ROW_COUNT):
            for j in range(con.COL_COUNT):
                surface.blit(self.visible_floor, (690 + j * con.PREVIEW_TILE_SIZE, i * con.PREVIEW_TILE_SIZE))
                if self.obstacle[i][j] == 'p':
                    surface.blit(self.pit, (690 + j * con.PREVIEW_TILE_SIZE, i * con.PREVIEW_TILE_SIZE))
                elif self.obstacle[i][j] == 'w':
                    surface.blit(self.wumpus, (690 + j * con.PREVIEW_TILE_SIZE, i * con.PREVIEW_TILE_SIZE))
                elif self.obstacle[i][j] == 'g':
                    surface.blit(self.floor_gold, (690+ j * con.PREVIEW_TILE_SIZE, i * con.PREVIEW_TILE_SIZE))
                    surface.blit(self.gold, (690+j * con.PREVIEW_TILE_SIZE, i * con.PREVIEW_TILE_SIZE))

        for i in range(con.ROW_COUNT):
            pygame.draw.line(surface, con.WHITE, (690, i * con.PREVIEW_TILE_SIZE), (690+self.width, i * con.PREVIEW_TILE_SIZE))
        pygame.draw.line(surface, con.WHITE, (690, self.height - 1), (690+self.width, self.height - 1))

        for i in range(con.COL_COUNT):
            pygame.draw.line(surface, con.WHITE, (690+i * con.PREVIEW_TILE_SIZE, 0), (690+i * con.PREVIEW_TILE_SIZE, self.height))
        pygame.draw.line(surface, con.WHITE, (690+self.width - 1, 0), (690+self.width - 1, self.height))
