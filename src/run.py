import pygame
from chessGUI import *
from menuGUI import *

WIDTH = 950
HEIGHT = 800

menu = MenuGUI(width=WIDTH, height=HEIGHT)
game_mode = menu.run()

# Start the game mode selected in the menu
chess_gui = ChessGUI(width=WIDTH, height=HEIGHT)
chess_gui.run(game_mode)
    
# If no selection was made or window was closed, pygame will quit automatically
pygame.quit()