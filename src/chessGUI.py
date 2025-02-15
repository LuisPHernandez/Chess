import pygame
from board import *

# Define global variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SQUARE_SIZE = (SCREEN_WIDTH / 8)
WHITE = (238, 238, 210)
BLACK = (118, 150, 86)

class ChessGUI:
    # Initializes the graphical interface
    def __init__(self):
        pygame.init()
        self.board = Board()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True

    # Draws board on the screen
    def draw_board(self):
        for rank in range(0, 8):
            for file in range(0, 8):    
                square = pygame.Rect((rank * SQUARE_SIZE), (file * SQUARE_SIZE), SQUARE_SIZE, SQUARE_SIZE)
                color = WHITE if (rank + file) % 2 == 0 else BLACK
                pygame.draw.rect(self.screen, color, square)

    def run(self):
        while self.running:
            self.draw_board()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            pygame.display.update()
        pygame.quit()