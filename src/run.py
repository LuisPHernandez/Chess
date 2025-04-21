import pygame
from local_chessGUI import *
from menuGUI import *

WIDTH = 950
HEIGHT = 800

menu = MenuGUI(width=WIDTH, height=HEIGHT)
game_mode = menu.run()

# Start the game mode selected in the menu
if game_mode == "local":
    # Initialize and run the local multiplayer chess GUI
    chess_gui = LocalChessGUI(width=WIDTH, height=HEIGHT)
    chess_gui.run()
    
# If no selection was made or window was closed, pygame will quit automatically
pygame.quit()