import pygame
import constants as con
import player
import button


class Game:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()

        self.running = True
        self.player = player.Player()
        self.tiles = self.player.tiles
        self.preview_tiles = self.player.preview_tiles
        self.start = False

        self.tickValue = 30
        self.window = pygame.display
        self.window.set_caption(con.CAPTION)
        self.window.set_icon(pygame.image.load(con.WUMPUS_ICON))

        self.surface = self.window.set_mode((self.tiles.width +500, self.tiles.height))
        self.print_obstacle()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.on_left_key_pressed()
                elif event.key == pygame.K_RIGHT:
                    self.player.on_right_key_pressed()
                elif event.key == pygame.K_UP:
                    self.player.on_up_key_pressed()
                elif event.key == pygame.K_DOWN:
                    self.player.on_down_key_pressed()

    def run(self):
        while self.running:
            self.event()
            self.surface.fill(con.WHITE)
            self.tiles.background(self.surface)
            self.tiles.text_view(self.surface)
          #  self.preview_tiles.background(self.surface)

            #self.clock.tick(2)
            prespecifiedbutton = button.Button(690, 250, 'Prespecified', self.surface)
            randombutton = button.Button(690, 300, 'Random', self.surface)
            if prespecifiedbutton.draw_button():
                self.tickValue = 1
                self.start = True
                self.prespecified()

            if randombutton.draw_button():
                self.tickValue = 1
                self.start = True

            self.player.draw_player(self.surface)

            if self.start:
                self.player.think_bro_think()

            self.update_window()

    def print_obstacle(self):
        print('....................................................')
        for i in range(10):
            print(self.tiles.obstacle[i])

    def update_window(self):
        self.clock.tick(self.tickValue)
        self.window.update()

    def prespecified(self):
        text_file = open("input.txt", "r")
        temp = []
        while True:
            line = text_file.readline()
            line = line[:-1]
            if len(line) == 0:
                break
            else:
                tempLine = line.split(' ')
                # print('hi',tempLine)
                temp.append(tempLine)
        # print(temp)
        for i in range(10):
            for j in range(10):
                self.tiles.obstacle[i][j] = temp[i][j]


if __name__ == "__main__":
    game = Game()
    game.run()
