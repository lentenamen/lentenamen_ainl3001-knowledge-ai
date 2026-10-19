"""
AINL3001 — Knowledge-Driven AI
Week 6 — Adversarial Search (Tic-Tac-Toe)
BSP 2026

X is MAX (+1 for a win); O is MIN (-1 for a win).
A draw has utility 0. Search assumes both players play optimally.

Tasks:
0. Evaluate a small game tree manually.
1. Represent and display a board; implement legal moves.
2. Check winners, terminal states and utility.
3. Implement Minimax.
4. Choose the best move for X.
5. Count visited game-tree nodes.
6. Implement Alpha-Beta Pruning and compare results.

Extensions: depth-limited search, heuristic evaluation, Connect Four.
"""

# TASK 0 — MANUAL MINIMAX
print("=" * 50)
print("TASK 0 — MANUAL MINIMAX")
print("=" * 50)
print(r"""
            MAX
           /   \
         MIN   MIN
        /  \   /  \
       3    5  2    9
""")
print("Which values do the two MIN nodes return?")
print("Which branch should MAX choose, and why?")

# BOARD — X plays next (three X marks and two O marks).
# Board positions are numbered 0 to 8, left to right, top to bottom.
board = [
    "X", "O", "X",
    " ", "O", " ",
    " ", " ", "X",
]

WINNING_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]


# --------------------------------------------------
# TASK 1 — BOARD REPRESENTATION
# --------------------------------------------------

def print_board(state):
    """Display the nine cells as a 3-by-3 board."""
    # TODO: Print three rows of three cells.
    pass


# --------------------------------------------------
# TASK 1 — AVAILABLE MOVES
# --------------------------------------------------

def available_moves(state):
    """Return indices of empty cells (0 through 8)."""
    # TODO: Find every position containing " ".
    pass


# --------------------------------------------------
# TASK 1 — MAKE A MOVE
# --------------------------------------------------

def make_move(state, move, player):
    """Return a NEW board with player ('X' or 'O') at move.

    Assume move is legal. Do not modify the input board.
    """
    # TODO: Copy the board and place the player's mark.
    pass


# --------------------------------------------------
# TASK 2 — WINNER
# --------------------------------------------------

def check_winner(state):
    """Return 'X', 'O' or None by checking all winning lines."""
    # TODO: Check each (a, b, c) in WINNING_LINES.
    pass


# --------------------------------------------------
# TASK 2 — TERMINAL STATE
# --------------------------------------------------

def is_terminal(state):
    """Return True for a win or a full board (draw)."""
    # TODO: Detect a winner OR no remaining empty cells.
    pass


# --------------------------------------------------
# TASK 2 — UTILITY
# --------------------------------------------------

def utility(state):
    """Return +1 for X win, -1 for O win, 0 for draw/no winner.

    Minimax calls this only at terminal states.
    """
    # TODO: Use check_winner() and return +1, -1 or 0.
    pass


# --------------------------------------------------
# TASK 3 — MINIMAX
# --------------------------------------------------

def minimax(state, maximizing, counter):
    """Return game-theoretic score; count every visited node.

    maximizing=True means X moves next; False means O moves next.
    counter is a one-item dictionary: {'nodes': 0}.
    """
    # TODO:
    # 1. Count this node: counter["nodes"] += 1.
    # 2. If terminal, return utility(state).
    # 3. For X (MAX), recursively choose the highest score.
    # 4. For O (MIN), recursively choose the lowest score.
    # Use make_move() to avoid changing the original board.
    pass


# --------------------------------------------------
# TASK 4 AND 5 — BEST MOVE
# --------------------------------------------------

def best_move(state, counter):
    """Return the best move index for X, or None if game is over.

    Count nodes in recursive Minimax searches. Ties use first move.
    """
    # TODO: Try each legal X move, call minimax() for O's turn,
    # and return the move with the highest score.
    # If the board is terminal, return None.
    pass


# --------------------------------------------------
# TASK 6 — ALPHA-BETA PRUNING
# --------------------------------------------------

def alpha_beta(state, maximizing, alpha, beta, counter):
    """Return the same score as Minimax, pruning irrelevant branches.

    alpha = best score MAX can guarantee so far.
    beta  = best score MIN can guarantee so far.
    """
    # TODO: Adapt minimax():
    # - MAX updates alpha; MIN updates beta.
    # - Stop exploring remaining moves if alpha >= beta.
    # - Count visited nodes exactly as in minimax().
    pass


# --------------------------------------------------
# TASK 6 — BEST MOVE WITH ALPHA-BETA
# --------------------------------------------------

def best_move_alpha_beta(state, counter):
    """Return the best move index for X using Alpha-Beta search."""
    # TODO: Like best_move(), but call alpha_beta().
    # Start alpha at -infinity and beta at +infinity.
    # Update alpha after each candidate X move.
    pass


# --------------------------------------------------
# TESTING — RUN PYTHON FILE IN VS CODE
# --------------------------------------------------

if __name__ == "__main__":
    print("\nCurrent board (X to move):")
    print_board(board)
    print("\nAvailable moves:", available_moves(board))
    print("Winner:", check_winner(board))
    print("Terminal:", is_terminal(board))
    print("Utility:", utility(board))

    # For a meaningful comparison, both algorithms use the same board
    # and count the same thing: recursive game-tree nodes visited.
    minimax_counter = {"nodes": 0}
    move_minimax = best_move(board, minimax_counter)
    print("\nMinimax best move for X:", move_minimax)
    print("Minimax nodes visited:", minimax_counter["nodes"])

    alpha_beta_counter = {"nodes": 0}
    move_ab = best_move_alpha_beta(board, alpha_beta_counter)
    print("\nAlpha-Beta best move for X:", move_ab)
    print("Alpha-Beta nodes visited:", alpha_beta_counter["nodes"])

    if move_minimax is not None:
        print("\nBoard after Minimax move:")
        print_board(make_move(board, move_minimax, "X"))

    print("\nReflection:")
    print("1. Why is Tic-Tac-Toe a search problem?")
    print("2. Why does Minimax assume an optimal opponent?")
    print("3. What is the purpose of a utility function?")
    print("4. What happens as games become larger?")
