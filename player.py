from audioop import reverse
from importlib.util import set_loader
from collections import deque as queue
import time
from tkinter import TRUE
from turtle import position
import pygame
import constants as con
import tiles
import preview_tiles
import button
import main
import sys

class Player:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.tiles = tiles.Tiles()
        self.preview_tiles = preview_tiles.Preview_Tiles(self.tiles)
        self.player_image = pygame.image.load(con.PLAYER_DOWN)
        self.position = [0, 0]
        self.track = [[[0, 0], 'root']]
        self.score = 0
        self.map = tiles.array_construct('u')
        self.pit_prob = tiles.array_construct(0)
        self.wumpus_prob = tiles.array_construct(0)
        self.sensor_op(self.position[0], self.position[1])
        self.chosen_path = [0, 0]
        self.check = 0
        self.vis = [[False for i in range(10)] for i in range(10)]
        self.wumpus_killed = False
        self.alive = True
        self.running = True
        self.window = pygame.display
        self.window.set_caption(con.CAPTION)
        self.window.set_icon(pygame.image.load(con.WUMPUS_ICON))

        self.surface = self.window.set_mode((400,300))
    def draw_player(self, surface):
        font = pygame.font.SysFont('Helvetica', 30)
        Score = font.render("Score :" + str(self.score),
                            False, con.BLACK, con.WHITE)
        surface.blit(Score, (self.tiles.width + 200, 330))
        surface.blit(
            self.player_image, (self.position[1] * con.TILE_SIZE, self.position[0] * con.TILE_SIZE))

    def tile_state_change(self):
        x = self.position[0]
        y = self.position[1]
        if self.tiles.tiles_con[x][y] == 'h':
            self.tiles.tiles_con[x][y] = 'v'

        self.sensor_op(x, y)

        if 'l' in self.map[x][y]:

            if self.tiles.get_gold(x, y):
                self.score += 100

        if self.tiles.obstacle[x][y] == 'p':
            self.alive = False
            while(self.running):
                self.surface.fill(con.WHITE)
                exitButton = button.Button(300, 300, 'Exit', self.surface)
                font = pygame.font.SysFont('Helvetica', 30)
                Score = font.render("Game over. You fell into a pit" ,False, con.BLACK, con.WHITE)
                self.surface.blit(Score, ( 420, 310))
                if exitButton.draw_button():
                    break
                self.window.update()           
            pygame.quit()
            sys.exit() 
           
        elif self.tiles.obstacle[x][y] == 'w':
            self.alive = False
            print(
                "............YOU ARE DEAD...........\n............EATEN BY WUMPUS............")
            pygame.quit()
            sys.exit()  


    def on_right_key_pressed(self):
        self.player_image = pygame.image.load(con.PLAYER_RIGHT)
        if ((self.position[1] + 1) * con.TILE_SIZE) < self.tiles.width:
            self.position[1] += 1
            self.tile_state_change()

    def on_left_key_pressed(self):
        self.player_image = pygame.image.load(con.PLAYER_LEFT)
        if ((self.position[1] - 1) * con.TILE_SIZE) >= 0:
            self.position[1] -= 1
            self.tile_state_change()

    def on_up_key_pressed(self):
        self.player_image = pygame.image.load(con.PLAYER_UP)
        if ((self.position[0] - 1) * con.TILE_SIZE) >= 0:
            self.position[0] -= 1
            self.tile_state_change()

    def on_down_key_pressed(self):
        self.player_image = pygame.image.load(con.PLAYER_DOWN)
        if ((self.position[0] + 1) * con.TILE_SIZE) < self.tiles.height:
            self.position[0] += 1
            self.tile_state_change()

    def add_knowledge(self, x, y, char):
        if isinstance(self.map[x][y], str):
            if self.map[x][y] == 'u':
                self.map[x][y] = char
            else:
                if char not in self.map[x][y]:
                    temp = [self.map[x][y], char]
                    self.map[x][y] = temp
        elif isinstance(self.map[x][y], list):
            if char not in self.map[x][y]:
                self.map[x][y].append(char)

    def think(self):
        flag = self.move_player()
        if self.position == [0, 0] and 'v' in self.map[0][1] and 'v' in self.map[1][0]:
            paths = self.get_Path()
            w_path = self.wumpus_prob_paths(paths)

            if not self.wumpus_killed and w_path:                  
                self.kill_wumpus(w_path)
                self.wumpus_killed = True
                tempPos = w_path[0][1]
            else:
                tempPos = paths[0][1]
            self.position = tempPos
            self.chosen_path = tempPos
            self.tile_state_change()
            flag = self.move_player()
            if self.score == 500:
                sys.exit
        self.return_player(flag)

    def wumpus_prob_paths(self, paths):
        # print(paths)
        paths.sort(reverse=True)
        w_path = []
        for p in paths:
            if p[2] == 'w':
                w_path.append(p)
        return w_path

    def return_player(self, flag):
        if not flag:
            if self.track[len(self.track) - 1][1] == 'up':
                del self.track[len(self.track) - 1]
                self.on_down_key_pressed()
            elif self.track[len(self.track) - 1][1] == 'down':
                del self.track[len(self.track) - 1]
                self.on_up_key_pressed()
            elif self.track[len(self.track) - 1][1] == 'right':
                del self.track[len(self.track) - 1]
                self.on_left_key_pressed()
            elif self.track[len(self.track) - 1][1] == 'left':
                del self.track[len(self.track) - 1]
                self.on_right_key_pressed()
            else:
                paths = self.get_Path()
                self.position = paths[0][1]
                self.chosen_path = paths[0][1]
                self.tile_state_change()
                flag = self.move_player()

    def move_player(self):
        valid_path = self.get_valid_path()
        unvisited_path = self.get_unvisited(valid_path)
        flag = False
        for i in range(len(unvisited_path)):
            if self.isSafe(unvisited_path[i][0], unvisited_path[i][1]):
                flag = True
                if unvisited_path[i][2] == 'up':
                    self.track.append([unvisited_path[i], 'up'])
                    self.on_up_key_pressed()

                elif unvisited_path[i][2] == 'left':
                    self.track.append([unvisited_path[i], 'left'])
                    self.on_left_key_pressed()

                elif unvisited_path[i][2] == 'right':
                    self.track.append([unvisited_path[i], 'right'])
                    self.on_right_key_pressed()

                elif unvisited_path[i][2] == 'down':
                    self.track.append([unvisited_path[i], 'down'])
                    self.on_down_key_pressed()

            if flag:
                break
        return flag

    def get_valid_path(self):
        temp = []
        if self.position[0] - 1 >= 0:
            temp.append([self.position[0] - 1, self.position[1], 'up'])
        if self.position[1] + 1 < con.COL_COUNT:
            temp.append([self.position[0], self.position[1] + 1, 'right'])
        if self.position[1] - 1 >= 0:
            temp.append([self.position[0], self.position[1] - 1, 'left'])
        if self.position[0] + 1 < con.ROW_COUNT:
            temp.append([self.position[0] + 1, self.position[1], 'down'])

        return temp

    def sensor_op(self, x, y):
        self.add_knowledge(x, y, 'v')

        sensors = self.tiles.get_map(x, y)

        for i in range(len(sensors)):
            self.add_knowledge(x, y, sensors[i])
            if sensors[i] == 's':
                self.Set_value(x, y, self.wumpus_prob, 1)

            if sensors[i] == 'b':
                self.Set_value(x, y, self.pit_prob, 1)
        if len(sensors) == 0:
            self.Set_value(x, y, self.wumpus_prob, -10)
            self.Set_value(x, y, self.pit_prob, -10)

    def kill_wumpus(self, w_path):
        if w_path:
            x = w_path[0][1][0]
            y = w_path[0][1][1]
            self.tiles.obstacle[x][y] = "n"
            self.map[x][y] = "v"
        # self.wumpus_prob.sort(reverse=True)
        # del self.wumpus_prob[0]
        # self.Set_value(x, y, self.wumpus_prob, 0)

    def Set_value(self, x, y, prob, value):
        if x + 1 < 10 and 'v' not in self.map[x + 1][y]:
            prob[x + 1][y] += value
        if x - 1 >= 0 and 'v' not in self.map[x - 1][y]:
            prob[x - 1][y] += value
        if y + 1 < 10 and 'v' not in self.map[x][y + 1]:
            prob[x][y + 1] += value
        if y - 1 > 0 and 'v' not in self.map[x][y - 1]:
            prob[x][y - 1] += value

    def isSafe(self, x, y):
        a = self.position[0]
        b = self.position[1]
        flag = False
        if 's' in self.map[a][b] or 'b' in self.map[a][b]:
            if x + 1 < 10 and 'v' in self.map[x + 1][y] and 's' not in self.map[x + 1][y] and 'b' not in self.map[x + 1][y]:
                flag = True
            if x - 1 >= 0 and 'v' in self.map[x - 1][y] and 's' not in self.map[x - 1][y] and 'b' not in self.map[x - 1][y]:
                flag = True
            if y + 1 < 10 and 'v' in self.map[x][y + 1] and 's' not in self.map[x][y + 1] and 'b' not in self.map[x][y + 1]:
                flag = True
            if y - 1 >= 0 and 'v' in self.map[x][y - 1] and 's' not in self.map[x][y - 1] and 'b' not in self.map[x][y - 1]:
                flag = True

        else:
            flag = True
        return flag

    def get_unvisited(self, valid_path):
        temp = []
        for i in range(len(valid_path)):
            x = valid_path[i][0]
            y = valid_path[i][1]

            if 'u' in self.map[x][y]:
                temp.append(valid_path[i])
        return temp

    def get_visited(self, valid_path):
        temp = []
        for i in range(len(valid_path)):
            x = valid_path[i][0]
            y = valid_path[i][1]

            if 'v' in self.map[x][y]:
                temp.append(valid_path[i])
        return temp

    def get_Path(self):
        temp = []
        if len(self.pit_prob) == 0 or len(self.wumpus_prob) == 0:
            return temp
        for i in range(10):
            for j in range(10):
                if self.pit_prob[i][j] > 0:
                    temp.append([self.pit_prob[i][j], [i, j], 'p'])
        for i in range(10):
            for j in range(10):
                if self.wumpus_prob[i][j] > 0:
                    temp.append([self.wumpus_prob[i][j], [i, j], 'w'])
        temp.sort()
        return temp
