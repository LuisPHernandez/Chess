class Piece:
    def __init__(self, color):
        self.color = color # Black or White

    def get_moves(self, board, position):
        """
        Generate possible moves for this piece.
        Should be overridden by subclasses.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.FEN = "p" if color == "black" else "P"

    def get_moves(self, board, position):
        moves = [] # Possible moves
        rank, file = position

        direction = -1 if self.color == "White" else 1 # White moves up, Black moves down

        # Moving forward one square	is possible if the next square in the correct direction is empty
        if board[rank + direction][file] is None:
            moves.append((rank + direction, file))

        if self.rank == 6 or self.rank == 1 and rank + (2 * direction) > 1 and rank + (2 * direction) < 6:
            if board[rank + (2 * direction)][file] is None:
                moves.append((rank + (2 * direction), file))

        for diagonal in [-1, 1, 2]:
            new_file = file + diagonal
            if 0 <= new_file < 8 and board[rank + direction][new_file] is not None and board[rank + direction][new_file].color != self.color:
                moves.append((rank + direction, new_file))

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.FEN = "r" if color == "black" else "R"

    def get_moves(self, board, position):
        moves = [] # Possible moves
        rank, file = position

        def add_moves(delta_rank, delta_file):
            r, f = rank + delta_rank, file + delta_file
            while 0 <= r < 8 and 0 <= f < 8:  # Stay within the board
                if board[r][f] is None: # Empty square
                    moves.append((r, f))
                else:
                    # If an opponent's piece, add the move and stop
                    if board[r][f].color != self.color:
                        moves.append((r, f))
                    break
                r += delta_rank
                f += delta_file

        # Add vertical and horizontal moves
        add_moves(-1, 0)  # Up
        add_moves(1, 0)   # Down
        add_moves(0, -1)  # Left
        add_moves(0, 1)   # Right
        return moves

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.FEN = "n" if color == "black" else "N"

    def get_moves(self, board, position):
        moves = []  # Possible moves
        rank, file = position

        # Define all possible knight move variations
        knight_deltas = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        for delta_rank, delta_file in knight_deltas:
            new_rank = rank + delta_rank
            new_file = file + delta_file

            # Check if the new position is within the board
            if 0 <= new_rank < 8 and 0 <= new_file < 8:
                # Check if the square is empty or contains an opponent's piece
                if board[new_rank][new_file] is None or board[new_rank][new_file].color != self.color:
                    moves.append((new_rank, new_file))

        return moves
    
class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.FEN = "b" if color == "black" else "B"

    def get_moves(self, board, position):
        moves = [] # Possible moves
        rank, file = position

        def add_moves(delta_rank, delta_file):
            r, f = rank + delta_rank, file + delta_file
            while 0 <= r < 8 and 0 <= f < 8:  # Stay within the board
                if board[r][f] is None: # Empty square
                    moves.append((r, f))
                else:
                    # If an opponent's piece, add the move and stop
                    if board[r][f].color!= self.color:
                        moves.append((r, f))
                    break
                r += delta_rank
                f += delta_file

        # Add moves in all directions
        add_moves(-1, -1)  # Up-left
        add_moves(-1, 1)   # Up-right
        add_moves(1, -1)   # Down-left
        add_moves(1, 1)    # Down-right
        return moves

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.FEN = "q" if color == "black" else "Q"

    def get_moves(self, board, position):
        moves = [] # Possible moves
        rank, file = position

        def add_straight_line_moves(delta_rank, delta_file):
            r, f = rank + delta_rank, file + delta_file
            while 0 <= r < 8 and 0 <= f < 8:  # Stay within the board
                if board[r][f] is None: # Empty square
                    moves.append((r, f))
                else:
                    # If an opponent's piece, add the move and stop
                    if board[r][f].color != self.color:
                        moves.append((r, f))
                    break
                r += delta_rank
                f += delta_file

        # Add vertical and horizontal moves
        add_straight_line_moves(-1, 0)  # Up
        add_straight_line_moves(1, 0)   # Down
        add_straight_line_moves(0, -1)  # Left
        add_straight_line_moves(0, 1)   # Right

        def add_diagonal_moves(delta_rank, delta_file):
            r, f = rank + delta_rank, file + delta_file
            while 0 <= r < 8 and 0 <= f < 8:  # Stay within the board
                if board[r][f] is None: # Empty square
                    moves.append((r, f))
                else:
                    # If an opponent's piece, add the move and stop
                    if board[r][f].color!= self.color:
                        moves.append((r, f))
                    break
                r += delta_rank
                f += delta_file

        # Add moves in all diagonal directions
        add_diagonal_moves(-1, -1)  # Up-left
        add_diagonal_moves(-1, 1)   # Up-right
        add_diagonal_moves(1, -1)   # Down-left
        add_diagonal_moves(1, 1)    # Down-right

        return moves

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.FEN = "k" if color == "black" else "K"

    def get_moves(self, board, position):
        moves = []  # Possible moves
        rank, file = position

        def add_straight_line_moves(delta_rank, delta_file):
            r, f = rank + delta_rank, file + delta_file
            if 0 <= r < 8 and 0 <= f < 8:  # Stay within the board
                if board[r][f] is None: # Empty square
                    moves.append((r, f))
                else:
                    # If an opponent's piece, add the move and stop
                    if board[r][f].color != self.color:
                        moves.append((r, f))

        # Add vertical and horizontal moves
        add_straight_line_moves(-1, 0)  # Up
        add_straight_line_moves(1, 0)   # Down
        add_straight_line_moves(0, -1)  # Left
        add_straight_line_moves(0, 1)   # Right

        def add_diagonal_moves(delta_rank, delta_file):
            r, f = rank + delta_rank, file + delta_file
            if 0 <= r < 8 and 0 <= f < 8:  # Stay within the board
                if board[r][f] is None: # Empty square
                    moves.append((r, f))
                else:
                    # If an opponent's piece, add the move and stop
                    if board[r][f].color!= self.color:
                        moves.append((r, f))

        # Add moves in all diagonal directions
        add_diagonal_moves(-1, -1)  # Up-left
        add_diagonal_moves(-1, 1)   # Up-right
        add_diagonal_moves(1, -1)   # Down-left
        add_diagonal_moves(1, 1)    # Down-right