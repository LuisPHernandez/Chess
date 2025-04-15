import pygame
import os
from game import Game

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
        self.game = Game()
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
        fen = self.game.board.convert_to_FEN().split("\n")
        for rank, line in enumerate(fen):
            rank = abs(7- rank)
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

            # Highlight possible moves
            for move in self.game.possible_moves:
                rank, file = move
                rank = abs(7 - rank)
                pygame.draw.circle(self.screen, (145, 145, 145), 
                                (((SQUARE_SIZE * file) + (SQUARE_SIZE * 0.5)), 
                                ((SQUARE_SIZE * rank) + (SQUARE_SIZE * 0.5))), 
                                (SQUARE_SIZE * 0.4))

            # Display game status (optional)
            if self.game.game_status == "check":
                # Display check status
                pass
            elif self.game.game_status == "checkmate":
                # Display checkmate status
                pass

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    file = int(x // SQUARE_SIZE)
                    rank = int(abs(800 - y) // SQUARE_SIZE)
                    
                    # Select piece or make move
                    if self.game.selected_piece is None:
                        self.game.select_piece((rank, file))
                    else:
                        # Try to move the selected piece
                        if not self.game.make_move((rank, file)):
                            # If move failed, try to select a different piece
                            self.game.select_piece((rank, file))

            pygame.display.update()
        pygame.quit()