class Piece:
    def __init__(self, color, pos):
        self.color = color # Black or White
        self.current_pos = pos # Current position in board

    def get_moves(self, board):
        """
        Generate possible moves for this piece.
        Should be overridden by subclasses.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

class Pawn(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.FEN = "p" if color == "black" else "P"

    def get_moves(self, board):
        moves = [] # Possible moves
        rank, file = self.current_pos

        direction = 1 if self.color == "white" else -1 # White moves up, Black moves down

        # Moving forward one square	is possible if the next square in the correct direction is empty
        if ((rank + direction) < 8) and board[rank + direction][file] is None:
            moves.append((rank + direction, file))

        if (self.color == "white") and (rank == 1):
            if (board[rank + (2 * direction)][file] is None) and (board[rank + direction][file] is None):
                moves.append((rank + (2 * direction), file))
        elif (self.color == "black") and (rank == 6):
            if (board[rank + (2 * direction)][file] is None) and (board[rank + direction][file] is None):
                moves.append((rank + (2 * direction), file))

        for diagonal in [-1, 1]:
            new_file = file + diagonal
            if (0 <= (rank + direction) < 8) and (0 <= new_file < 8) and (board[rank + direction][new_file] is not None) and (board[rank + direction][new_file].color != self.color):
                moves.append((rank + direction, new_file))

        return moves

class Rook(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.FEN = "r" if color == "black" else "R"

    def get_moves(self, board):
        moves = [] # Possible moves
        rank, file = self.current_pos

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
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.FEN = "n" if color == "black" else "N"

    def get_moves(self, board):
        moves = []  # Possible moves
        rank, file = self.current_pos

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
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.FEN = "b" if color == "black" else "B"

    def get_moves(self, board):
        moves = [] # Possible moves
        rank, file = self.current_pos

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
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.FEN = "q" if color == "black" else "Q"

    def get_moves(self, board):
        moves = [] # Possible moves
        rank, file = self.current_pos

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
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.FEN = "k" if color == "black" else "K"

    def get_moves(self, board):
        moves = []  # Possible moves
        rank, file = self.current_pos

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
        return moves