import pygame
import os
from board import *

# Define global variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SQUARE_SIZE = (SCREEN_WIDTH / 8)
WHITE = (238, 238, 210)
BLACK = (118, 150, 86)

PIECE_IMAGES = {
    "P": "white-pawn.png",
    "p": "black-pawn.png",
    "R": "white-rook.png",
    "r": "black-rook.png",
    "N": "white-knight.png",
    "n": "black-knight.png",
    "B": "white-bishop.png",
    "b": "black-bishop.png",
    "Q": "white-queen.png",
    "q": "black-queen.png",
    "K": "white-king.png",
    "k": "black-king.png"
}

class ChessGUI:
    # Initializes the graphical interface
    def __init__(self):
        pygame.init()
        self.board = Board()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.load_images()
        self.running = True

    # Loads images for chess pieces
    def load_images(self):
        self.images = {}
        images_dir = os.path.join("static", "images") 

        for piece, file in PIECE_IMAGES.items():
            path = os.path.join(images_dir, file)
            self.images[piece] = pygame.transform.scale(pygame.image.load(path), (SQUARE_SIZE, SQUARE_SIZE))

    # Draws board on the screen
    def draw_board(self):
        for rank in range(0, 8):
            for file in range(0, 8):    
                square = pygame.Rect((rank * SQUARE_SIZE), (file * SQUARE_SIZE), SQUARE_SIZE, SQUARE_SIZE)
                color = WHITE if (rank + file) % 2 == 0 else BLACK
                pygame.draw.rect(self.screen, color, square)

    # Draws pieces onto board
    def draw_pieces(self):
        fen = self.board.convert_to_FEN().split("\n")
        for rank, line in enumerate(fen):
            file = 0
            for char in line:
                if char.isdigit():
                    file += int(char)
                elif char in PIECE_IMAGES:
                    self.screen.blit(self.images[char], (file * SQUARE_SIZE, rank * SQUARE_SIZE))
                    file += 1

    # Runs the main game loop
    def run(self):
        while self.running:
            self.draw_board()
            self.draw_pieces()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            pygame.display.update()
        pygame.quit()