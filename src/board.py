from pieces import *

class Board:
    def __init__(self):
        # Board initializes with standard chess setup
        self.board_state = [[None] * 8 for i in range(8)]
        self.setup_board()

    def setup_board(self):
        # Place pawns
        for file in range(8):
            self.board_state[6][file] = Pawn("white")
            self.board_state[1][file] = Pawn("black")

        # Place rooks
        self.board_state[0][0] = Rook("black")
        self.board_state[0][7] = Rook("black")
        self.board_state[7][0] = Rook("white")
        self.board_state[7][7] = Rook("white")

        # Place knights
        self.board_state[0][1] = Knight("black")
        self.board_state[0][6] = Knight("black")
        self.board_state[7][1] = Knight("white")
        self.board_state[7][6] = Knight("white")

        # Place bishops
        self.board_state[0][2] = Bishop("black")
        self.board_state[0][5] = Bishop("black")
        self.board_state[7][2] = Bishop("white")
        self.board_state[7][5] = Bishop("white")

        # Place queens
        self.board_state[0][3] = Queen("black")
        self.board_state[7][3] = Queen("white")

        # Place kings
        self.board_state[0][4] = King("black")
        self.board_state[7][4] = King("white")

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

    def move_piece(self, start_pos, end_pos):
        """
        Move a piece from start_pos to end_pos.
        :param start_pos: Tuple (row, col) for the starting position.
        :param end_pos: Tuple (row, col) for the ending position.
        """
        start_rank, start_file = start_pos
        end_rank, end_file = end_pos
        piece = self.board_state[start_rank][start_file]

        # Perform the move
        self.board_state[end_rank][end_file] = piece
        self.board_state[start_rank][start_file] = " "

    def get_piece(self, position):
        """
        Get the piece at a specific position.
        :param position: Tuple (row, col)
        :return: The piece at the position.
        """
        row, col = position
        return self.board_state[row][col]