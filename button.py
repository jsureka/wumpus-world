import numpy
import pygame
from pygame.locals import *

# define colours
BLUE = (135, 206, 235)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
bg_color = (178, 190, 181)

row_number = 6
column_number = 7
board = numpy.zeros((row_number, column_number))
userPiece = 1
AIPiece = -1
EMPTY = 0
WINNING_LENGTH = 4

pygame.init()
# font for button
font = pygame.font.SysFont('Helvetica', 14,bold=True)

# define global variable
clicked = False


class Button:
    # colours for button and text
    button_col = (93, 190, 163)
    hover_col = (75, 225, 255)
    click_col = (50, 150, 255)
    text_col = WHITE
    width = 90
    height = 50

    def __init__(self, x, y, text, screen):
        self.x = x
        self.y = y
        self.text = text
        self.screen = screen

    def draw_button(self):

        global clicked
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # create pygame Rect object for the button
        button_rect = Rect(self.x, self.y, self.width, self.height)

        # check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(self.screen, self.click_col, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(self.screen, self.hover_col, button_rect)
        else:
            pygame.draw.rect(self.screen, self.button_col, button_rect)

        # add shading to button
        pygame.draw.line(self.screen, WHITE, (self.x, self.y), (self.x + self.width, self.y), 2)
        pygame.draw.line(self.screen, WHITE, (self.x, self.y), (self.x, self.y + self.height), 2)
        pygame.draw.line(self.screen, BLACK, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(self.screen, BLACK, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

        # add text to button
        text_img = font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        self.screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 18))
        return action


