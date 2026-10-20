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
    for row in range(3):
        cells = state[row * 3:row * 3 + 3]
        print(" " + " | ".join(cells))
        if row < 2:
            print("---+---+---")


# --------------------------------------------------
# TASK 1 — AVAILABLE MOVES
# --------------------------------------------------

def available_moves(state):
    """Return indices of empty cells (0 through 8)."""
    return [i for i, cell in enumerate(state) if cell == " "]


# --------------------------------------------------
# TASK 1 — MAKE A MOVE
# --------------------------------------------------

def make_move(state, move, player):
    """Return a NEW board with player ('X' or 'O') at move.

    Assume move is legal. Do not modify the input board.
    """
    new_state = state.copy()
    new_state[move] = player
    return new_state


# --------------------------------------------------
# TASK 2 — WINNER
# --------------------------------------------------

def check_winner(state):
    """Return 'X', 'O' or None by checking all winning lines."""
    for a, b, c in WINNING_LINES:
        if state[a] != " " and state[a] == state[b] == state[c]:
            return state[a]
    return None


# --------------------------------------------------
# TASK 2 — TERMINAL STATE
# --------------------------------------------------

def is_terminal(state):
    """Return True for a win or a full board (draw)."""
    return check_winner(state) is not None or not available_moves(state)


# --------------------------------------------------
# TASK 2 — UTILITY
# --------------------------------------------------

def utility(state):
    """Return +1 for X win, -1 for O win, 0 for draw/no winner.

    Minimax calls this only at terminal states.
    """
    winner = check_winner(state)
    if winner == "X":
        return 1
    if winner == "O":
        return -1
    return 0


# --------------------------------------------------
# TASK 3 — MINIMAX
# --------------------------------------------------

def minimax(state, maximizing, counter):
    """Return game-theoretic score; count every visited node.

    maximizing=True means X moves next; False means O moves next.
    counter is a one-item dictionary: {'nodes': 0}.
    """
    counter["nodes"] += 1

    if is_terminal(state):
        return utility(state)

    if maximizing:
        best = float("-inf")
        for move in available_moves(state):
            score = minimax(make_move(state, move, "X"), False, counter)
            best = max(best, score)
        return best
    else:
        best = float("inf")
        for move in available_moves(state):
            score = minimax(make_move(state, move, "O"), True, counter)
            best = min(best, score)
        return best


# --------------------------------------------------
# TASK 4 AND 5 — BEST MOVE
# --------------------------------------------------

def best_move(state, counter):
    """Return the best move index for X, or None if game is over.

    Count nodes in recursive Minimax searches. Ties use first move.
    """
    if is_terminal(state):
        return None

    best_score = float("-inf")
    chosen = None
    for move in available_moves(state):
        score = minimax(make_move(state, move, "X"), False, counter)
        # Strict ">" keeps the first move when scores tie.
        if score > best_score:
            best_score = score
            chosen = move
    return chosen


# --------------------------------------------------
# TASK 6 — ALPHA-BETA PRUNING
# --------------------------------------------------

def alpha_beta(state, maximizing, alpha, beta, counter):
    """Return the same score as Minimax, pruning irrelevant branches.

    alpha = best score MAX can guarantee so far.
    beta  = best score MIN can guarantee so far.
    """
    counter["nodes"] += 1

    if is_terminal(state):
        return utility(state)

    if maximizing:
        best = float("-inf")
        for move in available_moves(state):
            score = alpha_beta(make_move(state, move, "X"), False,
                               alpha, beta, counter)
            best = max(best, score)
            alpha = max(alpha, best)
            if alpha >= beta:
                break  # MIN above will never let play reach here.
        return best
    else:
        best = float("inf")
        for move in available_moves(state):
            score = alpha_beta(make_move(state, move, "O"), True,
                               alpha, beta, counter)
            best = min(best, score)
            beta = min(beta, best)
            if alpha >= beta:
                break  # MAX above already has something at least as good.
        return best


# --------------------------------------------------
# TASK 6 — BEST MOVE WITH ALPHA-BETA
# --------------------------------------------------

def best_move_alpha_beta(state, counter):
    """Return the best move index for X using Alpha-Beta search."""
    if is_terminal(state):
        return None

    alpha = float("-inf")
    beta = float("inf")
    best_score = float("-inf")
    chosen = None
    for move in available_moves(state):
        score = alpha_beta(make_move(state, move, "X"), False,
                           alpha, beta, counter)
        if score > best_score:
            best_score = score
            chosen = move
        alpha = max(alpha, best_score)
    return chosen


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
    print("Tic-Tac-Toe has states (board positions), actions (legal moves), a transition function (make_move) and terminal states with utilities. Finding the best move means " \
    "\nsearching the tree of possible future positions to see which move leads to the best outcome.")
    print("\n")

    print("2. Why does Minimax assume an optimal opponent?")
    print("Minimax assumes the opponent always picks the move that is worst for us. This gives a guaranteed worst-case result: if the opponent plays worse than optimally, we can only do as well or better. It also makes the game-tree values well defined, with MAX choosing the highest value and MIN the lowest.")
    print("\n")


    print("3. What is the purpose of a utility function?")
    print("The utility function gives each terminal state a number (+1 for an X win, -1 for an O win, 0 for a draw). Minimax backs these values up the tree, so it can compare moves and choose the one with the best guaranteed outcome.")
    print("\n")


    print("4. What happens as games become larger?")
    print("The game tree grows exponentially with the branching factor and depth, so searching to the end becomes impossible. Tic-Tac-Toe from an empty board has 549,946 Minimax nodes, but chess and Go are vastly larger. Larger games need Alpha-Beta pruning (18,297 nodes from an empty board), depth-limited search and heuristic evaluation functions to estimate non-terminal positions.")