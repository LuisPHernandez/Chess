import unittest
import sys
import os

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.append(src_path)
from chess_ai import *
from game import Game

# Creating a test case
class TestAI(unittest.TestCase):
    def initialize(self):
        self.game = Game()
        self.ai = ChessAI(self.game, "black")
        print(self.game.board.convert_to_FEN())

    def test_point_calculation_start(self):
        self.initialize()
        self.ai.calculate_points()
        self.assertEqual(self.ai.white_points, 2392)  # Test white's points at the start of the game
        self.assertEqual(self.ai.black_points, 2392) # Test black's points at the start of the game
    
    def test_point_calculation_no_captures(self):
        self.initialize()
        piece = self.game.board.get_piece((1,0)) 
        self.game.selected_piece = piece
        self.game.make_move((3,0)) # Move 2 squares the white pawn at rank 2 and file 1 
        piece = self.game.board.get_piece((6,0))
        self.game.selected_piece = piece
        self.game.make_move((4,0)) # Move 2 squares the black pawn at rank 7 and file 1
        self.ai.calculate_points()

        self.assertEqual(self.ai.white_points, 2392)  # Test white's points after a move with no captures
        self.assertEqual(self.ai.black_points, 2392) # Test black's points after a move with no captures

    def test_point_calculation_captures(self):
        self.initialize()
        piece = self.game.select_piece((1,0))
        self.game.make_move((3,0)) # Move 2 squares the white pawn at rank 2 and file 1 
        piece = self.game.select_piece((6,1))
        self.game.make_move((4,1)) # Move 2 squares the black pawn at rank 7 and file 2
        piece = self.game.select_piece((3,0))
        self.game.make_move((4,1)) # Capture the black pawn with the white pawn
        self.ai.calculate_points()
        print(self.game.board.convert_to_FEN())

        self.assertEqual(self.ai.white_points, 2392)  # Test white's points after two moves with no captures
        self.assertEqual(self.ai.black_points, 2382) # Test black's points after a move with a capture

# Running the tests
if __name__ == '__main__':
    unittest.main()