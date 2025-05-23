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

    def minimax(self, depth, alpha, beta):
        if (depth == 0) or (self.game.update_game_status() == "terminal"):
            return None, self.evaluate()
        
        if (self.game.current_turn == self.color):
            maximizing_player = True
        else:
            maximizing_player = False
        
        piece_moves = self.game.get_all_legal_moves()
        best_move = None

        if maximizing_player:
            max_value = float("-inf")
            for piece in piece_moves:
                for move in piece[1]:
                    self.game.select_piece(piece[0].current_pos)
                    self.game.make_move(move)
                    current_value = self.minimax(depth - 1, alpha, beta)
                    self.game.undo_move()
                    if current_value[1] > max_value:
                        max_value = current_value[1]
                        best_move = (piece[0], move)
                    alpha = max(alpha, current_value[1])
                    if beta <= alpha:
                        break
            return best_move, max_value
        else:
            min_value = float("inf")
            for piece in piece_moves:
                for move in piece[1]:
                    self.game.select_piece(piece[0].current_pos)
                    self.game.make_move(move)
                    current_value = self.minimax(depth - 1, alpha, beta)
                    self.game.undo_move()
                    if current_value[1] < min_value:
                        min_value = current_value[1]
                        best_move = (piece[0], move)
                    beta = min(beta, current_value[1])
                    if beta <= alpha:
                        break
            return best_move, min_value


    def calculate_points(self):
        self.white_points = 0
        self.black_points = 0
        for rank in self.game.board.board_state:
            for file in rank:
                if file:
                    if file.color == "white":
                        if type(file).__name__ in self.piece_values.keys():
                            self.white_points += self.piece_values[type(file).__name__]
                    elif file.color == "black":
                        if type(file).__name__ in self.piece_values.keys():
                            self.black_points += self.piece_values[type(file).__name__]

    def evaluate(self):
        self.calculate_points()
        if self.color == "white":
            return self.white_points - self.black_points
        else:
            return self.black_points - self.white_points
        
    def make_move(self):
        move, value = self.minimax(3, float("-inf"), float("inf"))
        self.game.select_piece(move[0].current_pos)
        self.game.make_move(move[1])