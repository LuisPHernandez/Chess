from pieces import *

class Board:
    def __init__(self):
        # Board initializes with standard chess setup
        self.board_state = [[None] * 8 for i in range(8)]
        self.setup_board()

    def setup_board(self):
        # Place pawns
        for file in range(8):
            self.board_state[1][file] = Pawn("white", (1, file))
            self.board_state[6][file] = Pawn("black", (6, file))

        # Place rooks
        self.board_state[0][0] = Rook("white", (0, 0))
        self.board_state[0][7] = Rook("white", (0, 7))
        self.board_state[7][0] = Rook("black", (7, 0))
        self.board_state[7][7] = Rook("black", (7, 7))

        # Place knights
        self.board_state[0][1] = Knight("white", (0, 1))
        self.board_state[0][6] = Knight("white", (0, 6))
        self.board_state[7][1] = Knight("black", (7, 1))
        self.board_state[7][6] = Knight("black", (7, 6))

        # Place bishops
        self.board_state[0][2] = Bishop("white", (0, 2))
        self.board_state[0][5] = Bishop("white", (0, 5))
        self.board_state[7][2] = Bishop("black", (7, 2))
        self.board_state[7][5] = Bishop("black", (7, 5))

        # Place queens
        self.board_state[0][3] = Queen("white", (0, 3))
        self.board_state[7][3] = Queen("black", (7, 3))

        # Place kings
        self.board_state[0][4] = King("white", (0, 4))
        self.board_state[7][4] = King("black", (7, 4))

    def convert_to_FEN(self):
        fen_string = ""

        for rank in self.board_state:
            empty_count = 0  # Count consecutive empty squares in a rank

            for file in rank:
                if file is None:  # Empty square
                    empty_count += 1
                else:
                    if empty_count > 0:  # Add empty squares count before the piece
                        fen_string += str(empty_count)
                        empty_count = 0
                    fen_string += file.FEN  # Add the FEN character for the piece

            if empty_count > 0:  # If there are empty squares at the end of the rank
                fen_string += str(empty_count)

            fen_string += "\n" 

        return fen_string

    def move_piece(self, piece, end_pos):
        """
        Move a piece to a end_pos.
        :param piece: Object (Piece) that will perform the move.
        :param end_pos: Tuple (row, col) for the ending position.
        """
        # Get the start and end positions
        end_rank, end_file = end_pos
        start_rank, start_file = piece.current_pos

        # Perform the move
        self.board_state[start_rank][start_file] = None
        self.board_state[end_rank][end_file] = piece
        piece.current_pos = (end_rank, end_file)

    def get_piece(self, position):
        """
        Get the piece at a specific position.
        :param position: Tuple (row, col)
        :return: The piece at the position.
        """
        row, col = position
        return self.board_state[row][col]