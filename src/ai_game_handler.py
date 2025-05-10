import pygame
import time
from chess_ai import ChessAI

class AIGameHandler:
    def __init__(self, game, gui):
        """Initializes the handler for AI opponent mode"""
        self.game = game
        self.gui = gui
        self.running = True
        self.human_player_color = "white"
        self.ai_color = "white" if self.human_player_color == "black" else "black"
        self.ai = ChessAI(self.game, self.ai_color)

    def run(self):
        """Runs the local multiplayer game loop"""
        self.gui.sound_effects["game_start"].play()
        while self.running:
            self.gui.draw_screen()
            self.display_game_status()

            if self.game.current_turn == self.human_player_color:
                self.highlight_possible_moves()

                if self.gui.promotion_active:
                    self.gui.draw_promotion_dialog()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.handle_mouse_click()
                    elif event.type == pygame.VIDEORESIZE:
                        self.gui.handle_resize(event.size)
            else:
                pygame.display.update()
                time.sleep(0.5)
                self.ai.make_move()
                if (self.game.move_history[-1]["captured"]):
                    self.gui.sound_effects["capture"].play()
                elif (self.game.current_turn == "black"):
                    self.gui.sound_effects["move_white"].play()
                else:
                    self.gui.sound_effects["move_black"].play()

            pygame.display.update()
        pygame.quit()
    
    def highlight_possible_moves(self):
        """Highlights the selected piece's possible moves"""
        for move in self.game.possible_moves:
                rank, file = move
                rank = abs(7 - rank)
                pygame.draw.circle(self.gui.screen, (145, 145, 145), 
                                (((self.gui.square_size * file) + (self.gui.square_size * 0.5)), 
                                ((self.gui.square_size * rank) + (self.gui.square_size * 0.5))), 
                                (self.gui.square_size * 0.4))

    def display_game_status(self):
        """Displays end game screens and plays sounds"""
        if self.game.game_status == "check":
            if not self.gui.check_sound_played:
                self.gui.sound_effects["check"].play()
                self.gui.check_sound_played = True
        else:
            self.gui.check_sound_played = False
        if self.game.game_status == "checkmate":
            if not self.gui.game_end_sound_played:
                self.gui.sound_effects["game_end"].play()
                self.gui.sound_effects["check"].play()
                self.gui.check_sound_played = True
                self.gui.game_end_sound_played = True
            self.gui.draw_checkmate_screen()
        if self.game.game_status == "stalemate":
            if not self.gui.game_end_sound_played:
                self.gui.sound_effects["game_end"].play()
                self.gui.game_end_sound_played = True
            self.gui.draw_stalemate_screen()
        if self.game.game_status == "draw 50-move":
            if not self.gui.game_end_sound_played:
                self.gui.sound_effects["game_end"].play()
                self.gui.game_end_sound_played = True
            self.gui.draw_tie_screen("50-move")
        if self.game.game_status == "draw insufficient material":
            if not self.gui.game_end_sound_played:
                self.gui.sound_effects["game_end"].play()
                self.gui.game_end_sound_played = True
            self.gui.draw_tie_screen("insufficient material")
        if self.game.game_status == "draw threefold repetition":
            if not self.gui.game_end_sound_played:
                self.gui.sound_effects["game_end"].play()
                self.gui.game_end_sound_played = True
            self.gui.draw_tie_screen("threefold repetition")

    def handle_mouse_click(self):
        """Handles mouse clicks for the local game mode"""
        x, y = pygame.mouse.get_pos()
        if hasattr(self.gui, "undo_button_rect") and self.gui.undo_button_rect.collidepoint(x, y):
            self.game.undo_move_ai_opp()
            
            if (self.game.current_turn == "white"):
                self.gui.sound_effects["move_white"].play()
            else:
                self.gui.sound_effects["move_black"].play()
            return
        elif (not self.gui.promotion_active) and (x > (self.gui.square_size * 8) or y > (self.gui.square_size * 8)):
            return

        rank = int(abs((self.gui.square_size * 8) - y) // self.gui.square_size)
        file = int(x // self.gui.square_size)
        
        if self.gui.promotion_active:
            selected_class = self.gui.handle_promotion_selection(x, y)
            if selected_class:  # Only proceed if a piece was selected
                self.game.finish_promotion(selected_class)
                self.gui.sound_effects["promotion"].play()
                return

        # Select piece or make move
        if self.game.selected_piece is None:
            self.game.select_piece((rank, file))
        else:
            # Try to move the selected piece
            result = self.game.make_move((rank, file))
            if result:
                if (self.game.move_history[-1]["captured"]):
                    self.gui.sound_effects["capture"].play()
                elif (self.game.current_turn == "black"):
                    self.gui.sound_effects["move_white"].play()
                else:
                    self.gui.sound_effects["move_black"].play()
            elif self.game.game_status == "promotion":
                # If move was a promotion
                self.gui.promotion_active = True
            elif not result:
                # If move failed for other reasons, try to select a different piece
                self.game.select_piece((rank, file))