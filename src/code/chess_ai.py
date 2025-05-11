import random

class ChessAI:
    def __init__(self, game, color):
        self.game = game
        self.color = color
        self.selected_piece = None
        self.piece_values = {
            "Pawn": 100,
            "Knight": 320,
            "Bishop": 330,
            "Rook": 500,
            "Queen": 900,
            "King": 20000
        }

    def make_move(self):
        legal_moves = []
        while not legal_moves:
            self.select_piece()
            legal_moves = self.game.get_legal_moves(self.selected_piece)
        move = legal_moves[random.randint(0, len(legal_moves) - 1)]
        self.game.make_move(move)

    def select_piece(self):
        pieces_in_board = []
        for rank in self.game.board.board_state:
            for piece in rank:
                if piece and piece.color == self.color:
                    pieces_in_board.append(piece)
        
        self.selected_piece = pieces_in_board[random.randint(0, len(pieces_in_board) - 1)]
        self.game.select_piece(self.selected_piece.current_pos)