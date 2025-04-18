import pygame
import os
from game import Game
from pieces import *

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

SFX = {
    "check": "check.mp3",
    "game_start": "game-start.mp3",
    "game_end": "game-end.mp3",
    "move_white": "move-self.mp3",
    "move_black": "move-opponent.mp3",
    "capture": "capture.mp3",
    "promotion": "promote.mp3"
}

class ChessGUI:
    def __init__(self):
        """Initializes the graphical interface"""
        pygame.init()
        self.game = Game()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.load_images()
        self.load_sound_effects()
        self.running = True
        self.check_sound_played = False
        self.game_end_sound_played = False
        self.promotion_active = False

    def load_images(self):
        """Loads images fot the chess pieces"""
        self.images = {}
        images_dir = os.path.join("static", "images") 

        for piece, file in PIECE_IMAGES.items():
            path = os.path.join(images_dir, file)
            self.images[piece] = pygame.transform.scale(pygame.image.load(path), (SQUARE_SIZE, SQUARE_SIZE))
    
    def load_sound_effects(self):
        """Loads sound effects"""
        self.sound_effects = {}
        sound_effects_dir = os.path.join("static", "sound_effects")

        for sound, file in SFX.items():
            path = os.path.join(sound_effects_dir, file)
            self.sound_effects[sound] = pygame.mixer.Sound(path)

    def draw_board(self):
        """Draws board on the screen"""
        for rank in range(0, 8):
            for file in range(0, 8):    
                square = pygame.Rect((rank * SQUARE_SIZE), (file * SQUARE_SIZE), SQUARE_SIZE, SQUARE_SIZE)
                color = WHITE if (rank + file) % 2 == 0 else BLACK
                pygame.draw.rect(self.screen, color, square)

    def draw_pieces(self):
        """Draws pieces onto board"""
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

    def draw_promotion_dialog(self):
        """Display dialog for handling promotions"""
        if not self.promotion_active:
            return
            
        rank, file = self.game.selected_piece.current_pos
        color = self.game.current_turn
        
        # Draw background
        dialog_width = SQUARE_SIZE
        dialog_height = SQUARE_SIZE * 4  # For Q, R, B, N
        dialog_x = file * SQUARE_SIZE
        dialog_y = 0 if rank == 7 else SCREEN_HEIGHT - dialog_height  # Position based on rank
        
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        pygame.draw.rect(self.screen, (230, 230, 230), dialog_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), dialog_rect, 2) 
        
        # Draw piece options
        pieces = ["Q", "R", "B", "N"]  # Queen, Rook, Bishop, Knight
        if color == "black":
            pieces = [p.lower() for p in pieces]
            
        for i, piece in enumerate(pieces):
            piece_rect = pygame.Rect(
                dialog_x, 
                dialog_y + (i * SQUARE_SIZE), 
                SQUARE_SIZE, 
                SQUARE_SIZE
            )
            pygame.draw.rect(self.screen, (200, 200, 200) if i % 2 == 0 else (180, 180, 180), piece_rect)
            # Draw the piece
            self.screen.blit(self.images[piece], (dialog_x, dialog_y + (i * SQUARE_SIZE)))

    def handle_promotion_selection(self, x, y):
        """Handle the selection of what piece the promoted Pawn will become"""
        if not self.promotion_active:
            return None
            
        rank, file = self.game.selected_piece.current_pos
        dialog_x = file * SQUARE_SIZE
        dialog_y = 0 if rank == 7 else SCREEN_HEIGHT - (SQUARE_SIZE * 4)
        
        # Check if click is within dialog
        if dialog_x <= x < dialog_x + SQUARE_SIZE and dialog_y <= y < dialog_y + (SQUARE_SIZE * 4):
            selection_index = int((y - dialog_y) // SQUARE_SIZE)
            promotion_pieces = [Queen, Rook, Bishop, Knight]
            selected_piece_class = promotion_pieces[selection_index]
            
            # Reset promotion state
            self.promotion_active = False
            return selected_piece_class
        return None

    def draw_checkmate_screen(self):
        """Displays the checkmate screen"""
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0)) 
        self.screen.blit(overlay, (0, 0))

        font = pygame.font.SysFont("arial", 72, bold=True)
        text = font.render("Checkmate!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
        self.screen.blit(text, text_rect)

        small_font = pygame.font.SysFont("arial", 36)
        winner = "White" if self.game.current_turn == "black" else "Black" 
        winner_text = small_font.render(f"{winner} wins!", True, (255, 255, 255))
        winner_rect = winner_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 20))
        self.screen.blit(winner_text, winner_rect)

        tip_text = small_font.render("Press any key to exit", True, (200, 200, 200))
        tip_rect = tip_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 80))
        self.screen.blit(tip_text, tip_rect)

        pygame.display.update()
        
    def run(self):
        """Runs the main game loop"""
        self.sound_effects["game_start"].play()
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

            # Display game status
            if self.game.game_status == "check":
                if not self.check_sound_played:
                    self.sound_effects["check"].play()
                    self.check_sound_played = True
            else:
                self.check_sound_played = False
            if self.game.game_status == "checkmate":
                if not self.game_end_sound_played:
                    self.sound_effects["game_end"].play()
                    self.game_end_sound_played = True
                self.draw_checkmate_screen()

            if self.promotion_active:
                self.draw_promotion_dialog()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    file = int(x // SQUARE_SIZE)
                    rank = int(abs(800 - y) // SQUARE_SIZE)
                    
                    if self.promotion_active:
                        selected_class = self.handle_promotion_selection(x, y)
                        if selected_class:  # Only proceed if a piece was selected
                            self.game.finish_promotion(selected_class)
                            self.sound_effects["promotion"].play()
                            continue

                    # Select piece or make move
                    if self.game.selected_piece is None:
                        self.game.select_piece((rank, file))
                    else:
                        # Try to move the selected piece
                        result = self.game.make_move((rank, file))
                        if result:
                            if (self.game.move_history[-1]["captured"]):
                                self.sound_effects["capture"].play()
                            elif (self.game.current_turn == "black"):
                                self.sound_effects["move_white"].play()
                            else:
                                self.sound_effects["move_black"].play()
                        elif self.game.game_status == "promotion":
                            # If move was a promotion
                            self.promotion_active = True
                        elif not result:
                            # If move failed for other reasons, try to select a different piece
                            self.game.select_piece((rank, file))

            pygame.display.update()
        pygame.quit()