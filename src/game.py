from board import Board
from pieces import *

class Game:
    def __init__(self):
        self.board = Board()
        self.current_turn = "white"
        self.move_history = []  # List of moves in the format [(piece, from_pos, to_pos), ...]
        self.last_status = "active" # active, check, checkmate, stalemate, draw
        self.game_status = "active"  # active, check, checkmate, stalemate, draw
        self.selected_piece = None
        self.possible_moves = []
        # For special moves
        self.en_passant_target = None
        self.castling_rights = {
            "white": {"kingside": True, "queenside": True},
            "black": {"kingside": True, "queenside": True}
        }
        self.halfmove_clock = 0  # For 50-move rule
        self.fullmove_number = 1  # Increments after black's move
        self.repetition_count = {} # For threefold repetition rule

    def find_king(self, color):
        """Find the position of a king of the specified color"""
        for rank in range(8):
            for file in range(8):
                piece = self.board.board_state[rank][file]
                if (piece is not None) and isinstance(piece, King) and (piece.color == color):
                    return (rank, file)
        return None

    def select_piece(self, position):
        """
        Try to select a piece at the given position.
        Returns True if a piece was selected, False otherwise.
        """
        rank, file = position
        piece = self.board.get_piece(position)
        
        # Can only select pieces of the current turn's color
        if (piece is None) or (piece.color != self.current_turn):
            return False
            
        self.selected_piece = piece
        self.possible_moves = self.get_legal_moves(piece)
        return True
    
    def get_legal_moves(self, piece):
        """
        Get all legal moves for a piece considering check constraints.
        """
        # Get the basic moves the piece can make
        all_moves = piece.get_moves(self.board.board_state)
        legal_moves = []
        
        # Test each move to see if it would leave the king in check
        original_pos = piece.current_pos
        
        for move in all_moves:
            # Save the piece that might be captured
            target_piece = self.board.get_piece(move)
            
            # Make the move temporarily
            self.board.move_piece(piece, move)
            
            # Check if the move would leave the king in check
            if not self.is_in_check(piece.color):
                legal_moves.append(move)
            
            # Undo the move
            self.board.move_piece(piece, original_pos)
            if target_piece:
                self.board.board_state[move[0]][move[1]] = target_piece
                target_piece.current_pos = move
    
        # Add en passant moves
        if isinstance(piece, Pawn):
            if self.en_passant_target:
                if (self.en_passant_target[0] != piece.color):
                    if (abs(self.en_passant_target[1] - piece.current_pos[0]) == 1) and (abs(self.en_passant_target[2] - piece.current_pos[1]) == 1):
                        legal_moves.append((self.en_passant_target[1], self.en_passant_target[2]))
        # Add castling moves
        elif isinstance(piece, King) and (self.game_status != "check"):
            if self.castling_rights[piece.color]["queenside"]:
                if (self.board.board_state[piece.current_pos[0]][1] is None) and (self.board.board_state[piece.current_pos[0]][2] is None) and (self.board.board_state[piece.current_pos[0]][3] is None):
                    if (not self.is_in_check(piece.color, (piece.current_pos[0], 2))) and (not self.is_in_check(piece.color, (piece.current_pos[0], 3))):
                        legal_moves.append((piece.current_pos[0], 2))
            if self.castling_rights[piece.color]["kingside"]:
                if (self.board.board_state[piece.current_pos[0]][5] is None) and (self.board.board_state[piece.current_pos[0]][6] is None):
                    if (not self.is_in_check(piece.color, (piece.current_pos[0], 5))):
                        legal_moves.append((piece.current_pos[0], 6))

        return legal_moves
    
    def make_move(self, end_position):
        """
        Move the currently selected piece to the end position if it's a legal move.
        Returns True if the move was made, False otherwise.
        """
        if (self.selected_piece is None) or (end_position not in self.possible_moves):
            return False
        
        castled = False
        start_position = self.selected_piece.current_pos
        moved_piece = self.selected_piece
        captured_piece = self.board.get_piece(end_position)
        
        # Update halfmove clock for the 50-move rule
        if isinstance(moved_piece, Pawn) or (captured_piece is not None):
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1
        
        # Update fullmove number
        if self.current_turn == "black":
            self.fullmove_number += 1

        # Record the move
        self.move_history.append({
            "piece": moved_piece,
            "from": start_position,
            "to": end_position,
            "captured": captured_piece,
            "half-move clock": self.halfmove_clock,
            "promotion": None,
            "castling": None,
            "rook": None,
            "rook_from": None,
            "rook_to": None
        })
        
        # Handle special moves
        if isinstance(moved_piece, Pawn):
            # Handle en passant
            if self.en_passant_target and (end_position == (self.en_passant_target[1], self.en_passant_target[2])):
                self.move_history[-1]["captured"] = self.board.board_state[start_position[0]][end_position[1]]
                self.board.board_state[start_position[0]][end_position[1]] = None
            
            # Handle promotion
            promotion_rank = 7 if moved_piece.color == "white" else 0
            if end_position[0] == promotion_rank:
                # Make the actual move
                self.board.move_piece(moved_piece, end_position)

                # Update game status to "promotion"
                self.update_game_status(piece = moved_piece)
                
                return False

            # Set en passant target for the next move
            if abs(start_position[0] - end_position[0]) == 2:
                self.en_passant_target = (moved_piece.color,
                    (start_position[0] + end_position[0]) // 2,
                    start_position[1]
                )
            else:
                self.en_passant_target = None
        else:
            self.en_passant_target = None
        
        if isinstance(moved_piece, King):
            # Handle castling move
            if (self.castling_rights[moved_piece.color]["queenside"]) and (end_position == (moved_piece.current_pos[0], 2)):
                self.move_history[-1]["castling"] = "queenside"
                self.move_history[-1]["rook"] = self.board.board_state[end_position[0]][0]
                self.move_history[-1]["rook_from"] = (end_position[0], 0)
                self.move_history[-1]["rook_to"] = (end_position[0], 3)

                self.board.board_state[end_position[0]][0] = None
                self.board.board_state[end_position[0]][2] = King(moved_piece.color, (end_position[0], 2))
                self.board.board_state[start_position[0]][start_position[1]] = None
                self.board.board_state[end_position[0]][3] = Rook(moved_piece.color, (end_position[0], 3))
                castled = True
            elif (self.castling_rights[moved_piece.color]["kingside"]) and (end_position == (moved_piece.current_pos[0], 6)):
                self.move_history[-1]["castling"] = "kingside"
                self.move_history[-1]["rook"] = self.board.board_state[end_position[0]][7]
                self.move_history[-1]["rook_from"] = (end_position[0], 7)
                self.move_history[-1]["rook_to"] = (end_position[0], 5)

                self.board.board_state[end_position[0]][7] = None
                self.board.board_state[end_position[0]][6] = King(moved_piece.color, (end_position[0], 6))
                self.board.board_state[start_position[0]][start_position[1]] = None
                self.board.board_state[end_position[0]][5] = Rook(moved_piece.color, (end_position[0], 5))
                castled = True

            # Update castling rights
            self.castling_rights[moved_piece.color]["kingside"] = False
            self.castling_rights[moved_piece.color]["queenside"] = False
            
        elif isinstance(moved_piece, Rook):
            if start_position[1] == 0:  # Queenside rook
                self.castling_rights[moved_piece.color]["queenside"] = False
            elif start_position[1] == 7:  # Kingside rook
                self.castling_rights[moved_piece.color]["kingside"] = False
        
        # Make the actual move
        if not castled:
            self.board.move_piece(moved_piece, end_position)
        
        # Update repetition count for threefold repetition rule
        fen = self.get_fen().split(" ")[0:4]  # Ignore halfmove/fullmove for repetition
        fen_key = " ".join(fen)
        self.repetition_count[fen_key] = self.repetition_count.get(fen_key, 0) + 1

        # Check game status after the move
        self.update_game_status()

        # Switch turns
        self.current_turn = "black" if self.current_turn == "white" else "white"
        
        # Clear selection
        self.selected_piece = None
        self.possible_moves = []
        
        return True
    
    def finish_promotion(self, selected_class):
        """
        Complete the promotion process by replacing the pawn with the selected piece.
        """
        if self.selected_piece is None or not isinstance(self.selected_piece, Pawn):
            return
        
        pos = self.selected_piece.current_pos
        color = self.selected_piece.color

        new_piece = selected_class(color, pos)
        self.board.board_state[pos[0]][pos[1]] = new_piece

        # Update the last move in history to reflect the promotion
        if self.move_history:
            self.move_history[-1]["promotion"] = selected_class.__name__

        # Switch turns
        self.current_turn = "black" if self.current_turn == "white" else "white"

        # Reset game status
        self.update_game_status()

        # Clear selection
        self.selected_piece = None
        self.possible_moves = []

    def is_in_check(self, color, position = None):
        """
        Check if the king of the given color is in check.
        """
        if position:
            king_position = position
        else:
            king_position = self.find_king(color)
        opponent_color = "black" if color == "white" else "white"
        
        # Check if any opponent piece can attack the king
        for rank in range(8):
            for file in range(8):
                piece = self.board.board_state[rank][file]
                if piece is not None and piece.color == opponent_color:
                    moves = piece.get_moves(self.board.board_state)
                    if king_position in moves:
                        return True
        return False
    
    def is_checkmate(self, color):
        """
        Check if the king of the given color is in checkmate.
        """
        # If not in check, can't be checkmate
        if not self.is_in_check(color):
            return False
        
        # Check if any piece can make a legal move
        for rank in range(8):
            for file in range(8):
                piece = self.board.board_state[rank][file]
                if piece is not None and piece.color == color:
                    legal_moves = self.get_legal_moves(piece)
                    if legal_moves:
                        return False
        
        # No legal moves and in check = checkmate
        return True
    
    def is_stalemate(self, color):
        """
        Check if the position is a stalemate for the given color.
        """
        # If in check, it's not stalemate
        if self.is_in_check(color):
            return False
        
        # Check if any piece can make a legal move
        for rank in range(8):
            for file in range(8):
                piece = self.board.board_state[rank][file]
                if piece is not None and piece.color == color:
                    legal_moves = self.get_legal_moves(piece)
                    if legal_moves:
                        return False
        
        # No legal moves and not in check = stalemate
        return True
    
    def update_game_status(self, piece = None):
        """
        Update the game status after a move.
        """
        opponent_color = "black" if self.current_turn == "white" else "white"
        
        # Check for promotion
        if piece and isinstance(piece, Pawn):
            promotion_rank = 7 if piece.color == "white" else 0
            if piece.current_pos[0] == promotion_rank:
                self.game_status = "promotion"
                return

        # Check for checkmate or stalemate
        if self.is_checkmate(opponent_color):
            self.game_status = "checkmate"
            return
        
        if self.is_stalemate(opponent_color):
            self.game_status = "stalemate"
            return
        
        # Check for draw
        if self.halfmove_clock >= 100:  # 50 moves = 100 half-moves
            self.game_status = "draw 50-move"
            return
        
        if self.is_insufficient_material():
            self.game_status = "draw insufficient material"
            return
        
        fen = self.get_fen().split(" ")[0:4]
        fen_key = " ".join(fen)
        if self.repetition_count.get(fen_key, 0) >= 3:
            self.game_status = "draw threefold repetition"
            return
        
        # Check if the current player is in check
        if self.is_in_check(opponent_color):
            self.game_status = "check"
        else:
            self.game_status = "active"
    
    def is_insufficient_material(self):
        """Check for draw due to insufficient mating material"""
        pieces = []
        for rank in self.board.board_state:
            for piece in rank:
                if piece:
                    pieces.append(piece)

        # King vs King
        if len(pieces) == 2:
            return True

        # King + bishop/knight vs King
        if len(pieces) == 3:
            types = [type(p) for p in pieces]
            if all(t in [King, Bishop, Knight] for t in types):
                return True

        # King + bishop vs King + bishop, both bishops on same color
        if len(pieces) == 4:
            bishops = [p for p in pieces if isinstance(p, Bishop)]
            if len(bishops) == 2:
                b1_color = (bishops[0].current_pos[0] + bishops[0].current_pos[1]) % 2
                b2_color = (bishops[1].current_pos[0] + bishops[1].current_pos[1]) % 2
                if b1_color == b2_color:
                    return True
        return False

    def get_fen(self):
        """
        Get the FEN (Forsyth-Edwards Notation) string for the current position.
        """
        # Get the board position part
        fen = self.board.convert_to_FEN().replace("\n", "/").rstrip("/")
        
        # Add current turn
        fen += " " + ("w" if self.current_turn == "white" else "b")
        
        # Add castling availability
        castling = ""
        if self.castling_rights["white"]["kingside"]:
            castling += "K"
        if self.castling_rights["white"]["queenside"]:
            castling += "Q"
        if self.castling_rights["black"]["kingside"]:
            castling += "k"
        if self.castling_rights["black"]["queenside"]:
            castling += "q"
        fen += " " + (castling if castling else "-")
        
        # Add en passant target square
        if self.en_passant_target:
            rank = self.en_passant_target[1]
            file = self.en_passant_target[2]
            fen += " " + chr(97 + file) + str(rank + 1)
        else:
            fen += " -"
        
        # Add halfmove clock and fullmove number
        fen += " " + str(self.halfmove_clock) + " " + str(self.fullmove_number)
        
        return fen
    
    def undo_move(self):
        """
        Undo the last move made.
        Returns True if a move was undone, False if there's no move to undo.
        """
        if not self.move_history:
            return False
        
        # Decrease count of repetition for threefold repetition rule
        fen = self.get_fen().split(" ")[0:4]
        fen_key = " ".join(fen)
        if fen_key in self.repetition_count:
            self.repetition_count[fen_key] = max(0, self.repetition_count[fen_key] - 1)

        # Get the last move
        last_move = self.move_history.pop()
        piece = last_move["piece"]
        from_pos = last_move["from"]
        to_pos = last_move["to"]
        captured = last_move["captured"]
        promotion = last_move["promotion"]
        castling = last_move["castling"]
        rook = last_move["rook"]
        rook_from = last_move["rook_from"]
        
        # Check if this was an en passant capture
        was_en_passant = isinstance(piece, Pawn) and captured and to_pos != captured.current_pos

        if promotion:
            piece = Pawn(piece.color, to_pos)
    
        if castling:
            self.board.move_piece(rook, rook_from)

        # Move the piece back
        self.board.move_piece(piece, from_pos)
    
        # Restore captured piece if any
        if captured:
            if was_en_passant:
                # For en passant, the captured pawn's position is different
                # It's in the same file as the destination but same rank as the starting position
                captured_pos = (from_pos[0], to_pos[1])
                self.board.board_state[captured_pos[0]][captured_pos[1]] = captured
                captured.current_pos = captured_pos
            else:
                # Normal capture
                self.board.board_state[to_pos[0]][to_pos[1]] = captured
                captured.current_pos = to_pos

         # Restore the halfmove clock from before this move was made
        if len(self.move_history) > 0:
            # Get the clock value from the previous move record
            self.halfmove_clock = self.move_history[-1]["half-move clock"]
        else:
            # If this was the first move, reset to 0
            self.halfmove_clock = 0
        
        # Switch back to the previous player's turn
        self.current_turn = "black" if self.current_turn == "white" else "white"
        
        # Update game status
        self.update_game_status()
        
        # Decrement fullmove number if needed
        if self.current_turn == "black":
            self.fullmove_number -= 1
        
        return True