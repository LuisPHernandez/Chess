from pieces import *

class Board:
    def __init__(self):
        # Board initializes with standard chess setup
        self.board = [[None] * 8 for i in range(8)]
        self.setup_board()

    def setup_board(self):
        # Place pawns
        for file in range(8):
            self.board[1][file] = Pawn("White")
            self.board[6][file] = Pawn("Black")

        # Place rooks
        self.board[0][0] = Rook("Black")
        self.board[0][7] = Rook("Black")
        self.board[7][0] = Rook("White")
        self.board[7][7] = Rook("White")

        # Place knights
        self.board[0][1] = Knight("Black")
        self.board[0][6] = Knight("Black")
        self.board[7][1] = Knight("White")
        self.board[7][6] = Knight("White")

        # Place bishops
        self.board[0][2] = Bishop("Black")
        self.board[0][5] = Bishop("Black")
        self.board[7][2] = Bishop("White")
        self.board[7][5] = Bishop("White")

        # Place queens
        self.board[0][3] = Queen("Black")
        self.board[7][3] = Queen("White")

        # Place kings
        self.board[0][4] = King("Black")
        self.board[7][4] = King("White")

    def convert_to_FEN(self):
        fen_string = ""

        for rank in self.board:
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

    def display(self):
        # Display the current state of the board
        print(self.convert_to_FEN())
        

    def move_piece(self, start_pos, end_pos):
        """
        Move a piece from start_pos to end_pos.
        :param start_pos: Tuple (row, col) for the starting position.
        :param end_pos: Tuple (row, col) for the ending position.
        """
        start_rank, start_file = start_pos
        end_rank, end_file = end_pos
        piece = self.board[start_rank][start_file]

        # Perform the move
        self.board[end_rank][end_file] = piece
        self.board[start_rank][start_file] = " "

    def get_piece(self, position):
        """
        Get the piece at a specific position.
        :param position: Tuple (row, col)
        :return: The piece at the position.
        """
        row, col = position
        return self.board[row][col]