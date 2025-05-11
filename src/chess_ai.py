import random

class ChessAI:
    def __init__(self, game, color):
        self.game = game
        self.color = color
        self.selected_piece = None
        self.piece_values = {
            "Pawn": 10,
            "Knight": 30,
            "Bishop": 31,
            "Rook": 50,
            "Queen": 90,
            "King": 2000
        }
        self.white_points = 0
        self.black_points = 0

    def minimax(self, depth):
        depth -= 1

    def calculate_points(self):
        for rank in self.game.board.board_state:
            for file in rank:
                if file:
                    if file.color == "white":
                        if type(file).__name__ in self.piece_values.keys():
                            self.white_points += self.piece_values[type(file).__name__]
                    elif file.color == "black":
                        if type(file).__name__ in self.piece_values.keys():
                            self.black_points += self.piece_values[type(file).__name__]

    def evaluate():
        pass





















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