
import time
from game import Game

def move_generation_test(depth):
    """Optimized move generation test function"""
    game = Game()
    return perft(game, depth)

def perft(game, depth):
    """
    Performance test function with optimizations:
    - Early termination for leaf nodes
    - Batch legal move generation
    - Reduced redundant calculation
    """
    # Base case - leaf node
    if depth == 0:
        return 1
    
    num_positions = 0
    # Get all legal moves at once instead of piece by piece
    all_piece_moves = game.get_all_legal_moves()
    
    # Track move history start index to optimize undo operations
    history_start_index = len(game.move_history)
    
    for piece, moves in all_piece_moves:
        for move in moves:
            # Make move and recursive call
            game.select_piece(piece.current_pos)
            game.make_move(move)
            
            # Recursively count positions from this new position
            num_positions += perft(game, depth - 1)
            
            # Undo move
            game.undo_move()
    
    return num_positions

# Optional: Bulk counting for specific depths for even more performance
def bulk_counting_perft(game, depth):
    """
    Enhanced performance with bulk counting at leaf nodes.
    When depth=1, we don't need recursion - just count moves.
    """
    if depth == 0:
        return 1
    
    if depth == 1:
        # Just count all legal moves without recursion
        move_count = 0
        all_piece_moves = game.get_all_legal_moves()
        for piece, moves in all_piece_moves:
            move_count += len(moves)
        return move_count
    
    num_positions = 0
    all_piece_moves = game.get_all_legal_moves()
    
    for piece, moves in all_piece_moves:
        for move in moves:
            game.select_piece(piece.current_pos)
            game.make_move(move)
            num_positions += bulk_counting_perft(game, depth - 1)
            game.undo_move()
    
    return num_positions

if __name__ == "__main__":
    # Test both implementations
    print("Testing optimized move generation:")
    for depth in range(0, 7):
        start_time = time.time()
        positions = move_generation_test(depth)
        elapsed_time = time.time() - start_time
        print(f"Depth: {depth}, Positions: {positions}, Time: {elapsed_time:.4f} seconds")
    
    print("\nTesting bulk counting optimization:")
    for depth in range(0, 7):
        game = Game()
        start_time = time.time()
        positions = bulk_counting_perft(game, depth)
        elapsed_time = time.time() - start_time
        print(f"Depth: {depth}, Positions: {positions}, Time: {elapsed_time:.4f} seconds")