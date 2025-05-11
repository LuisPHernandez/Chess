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
        if (depth == 0) or (self.game.update_game_status() == "terminal"):
            return None, self.evaluate()
        
        piece_moves = self.game.get_all_legal_moves()
        random_best_piece = random.randint(0, (len(piece_moves) - 1))
        best_move = (piece_moves[random_best_piece], piece_moves[random_best_piece][random.randint(0, (len(piece_moves[random_best_piece]) - 1))])

        if (self.game.current_turn == self.color):
            max_value = float("-inf")
            for piece in piece_moves:
                for move in piece[1]:
                    self.game.select_piece(piece[0].current_pos)
                    self.game.make_move(move)
                    current_value = self.minimax(depth - 1)
                    self.game.undo_move()
                    if current_value[1] > max_value:
                        max_value = current_value[1]
                        best_move = (piece[0], move)
            return best_move, max_value
        else:
            min_value = float("inf")
            for piece in piece_moves:
                for move in piece[1]:
                    self.game.select_piece(piece[0].current_pos)
                    self.game.make_move(move)
                    current_value = self.minimax(depth - 1)
                    self.game.undo_move()
                    if current_value[1] < min_value:
                        min_value = current_value[1]
                        best_move = (piece[0], move)
            return best_move, min_value


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

    def evaluate(self):
        if self.color == "white":
            return self.white_points - self.black_points
        else:
            return self.black_points - self.white_points
        
    def make_move(self):
        move, value = self.minimax(2)
        self.game.select_piece(move[0].current_pos)
        self.game.make_move(move[1])