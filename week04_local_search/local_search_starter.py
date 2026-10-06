"""
AINL3001 — Knowledge-Driven AI
Week 4 — Local Search and Optimisation
BSP 2026

This week introduces local search.

In previous weeks, search algorithms explored paths through
a state space in order to reach a goal.

Local search takes a different approach:

    1. Start with a state.
    2. Evaluate how good that state is.
    3. Generate neighbouring states.
    4. Move to a better neighbour.
    5. Repeat.

We will explore this using the N-Queens problem.

Tasks
-----

1. Understand the problem representation.
2. Implement conflict counting.
3. Explore neighbouring states.
4. Implement Hill Climbing.
5. Implement Simulated Annealing.
"""

import math
import random

from queens_problem import QueensProblem

N = 20


# --------------------------------------------------
# TASK 0 — UNDERSTANDING THE STATE
# --------------------------------------------------

example_board = [0, 1, 2, 3]

print("Manual Exploration Board:")
print(example_board)

print(
    "\nEach list position represents a column."
)

print(
    "Each value represents the row containing the queen."
)

print(
    "\nQuestion: How many conflicts exist on this board?"
)


# --------------------------------------------------
# TASK 1 — EVALUATE A STATE
# --------------------------------------------------

def count_conflicts(board):
    """
    Return the number of pairs of queens
    that attack each other.

    Lower values are better.

    A solution has:

        conflict count = 0
    """

    # TODO:
    # Compare each queen with every queen
    # that comes after it.
    #
    # Queens conflict when they are:
    #
    #   1. in the same row
    #   2. on the same diagonal

    conflicts = 0

    for i in range(len(board)):
        for j in range(i + 1, len(board)):

            same_row = board[i] == board[j]
            same_diagonal = abs(board[i] - board[j]) == j - i

            if same_row or same_diagonal:
                conflicts += 1

    return conflicts


# --------------------------------------------------
# TASK 2 — EXPLORE THE PROBLEM
# --------------------------------------------------

def generate_neighbours(problem, state):
    """
    Generate all neighbouring boards.

    Use the Problem interface introduced this week:

        problem.actions(state)
        problem.result(state, action)
    """

    neighbours = []

    # TODO:
    #
    # 1. Ask the problem for the available actions.
    # 2. Apply each action.
    # 3. Add the resulting state to neighbours.

    for action in problem.actions(state):
        neighbours.append(
            problem.result(state, action)
        )

    return neighbours


# --------------------------------------------------
# TASK 3 — HILL CLIMBING
# --------------------------------------------------

def hill_climbing(problem, start_board):
    """
    Use Hill Climbing to reduce the number
    of conflicts.

    Algorithm:

        current = start state

        repeat:

            generate neighbours

            find the neighbour with the
            lowest conflict count

            if the neighbour is not better:
                stop

            otherwise:
                move to the neighbour

        return current
    """

    current = start_board

    while True:

        neighbours = generate_neighbours(problem, current)

        best_neighbour = min(
            neighbours,
            key=count_conflicts
        )

        if count_conflicts(best_neighbour) >= count_conflicts(current):
            break

        current = best_neighbour

    return current


# --------------------------------------------------
# TASK 4 — SIMULATED ANNEALING
# --------------------------------------------------

def simulated_annealing(problem, start_board):
    """
    Use Simulated Annealing to search for
    a solution.

    Unlike Hill Climbing, Simulated Annealing
    can sometimes accept a worse state.

    This can help escape local minima.
    """

    current = start_board

    temperature = 10.0

    # Slow cooling gives the search enough steps to explore.
    # (0.95 only allowed ~135 steps before the temperature hit 0.01.)
    cooling_rate = 0.999

    while temperature > 0.01:

        if count_conflicts(current) == 0:
            break

        action = random.choice(problem.actions(current))
        neighbour = problem.result(current, action)

        # Positive delta means the neighbour is worse.
        delta = count_conflicts(neighbour) - count_conflicts(current)

        if delta < 0 or random.random() < math.exp(-delta / temperature):
            current = neighbour

        temperature *= cooling_rate

    return current


# --------------------------------------------------
# EXTENSION 2 — RANDOM RESTART HILL CLIMBING
# --------------------------------------------------

def random_board(n):
    """
    Return a random board with one queen per column.
    """

    return [
        random.randint(0, n - 1)
        for _ in range(n)
    ]


def random_restart_hill_climbing(n, max_restarts=100):
    """
    Run Hill Climbing from random starting boards
    until a solution is found or we run out of restarts.

    Returns the best board found and the number of
    Hill Climbing runs used.
    """

    best = None

    for attempt in range(1, max_restarts + 1):

        start = random_board(n)
        problem = QueensProblem(start)

        result = hill_climbing(problem, start)

        if best is None or count_conflicts(result) < count_conflicts(best):
            best = result

        if count_conflicts(best) == 0:
            return best, attempt

    return best, max_restarts


# --------------------------------------------------
# TASK 5.1 — COMPARE THE ALGORITHMS
# --------------------------------------------------

def compare_algorithms(n, runs=20):
    """
    Run Hill Climbing and Simulated Annealing from the
    same random starting boards and record the final costs.
    """

    hc_costs = []
    sa_costs = []

    for _ in range(runs):

        start = random_board(n)
        problem = QueensProblem(start)

        hc_costs.append(
            count_conflicts(hill_climbing(problem, start))
        )
        sa_costs.append(
            count_conflicts(simulated_annealing(problem, start))
        )

    print(f"\nComparison over {runs} runs (N = {n})")
    print(f"{'Algorithm':<22}{'Best':>6}{'Mean':>8}{'Solved':>9}")

    for name, costs in [
        ("Hill Climbing", hc_costs),
        ("Simulated Annealing", sa_costs),
    ]:
        solved = costs.count(0)
        mean = sum(costs) / len(costs)
        print(f"{name:<22}{min(costs):>6}{mean:>8.2f}{solved:>6}/{runs}")

    print("\nHill Climbing costs:      ", hc_costs)
    print("Simulated Annealing costs:", sa_costs)


# --------------------------------------------------
# TESTING AREA
# --------------------------------------------------

if __name__ == "__main__":

    board = [
        random.randint(0, N - 1)
        for _ in range(N)
    ]

    problem = QueensProblem(board)

    print("\nRandom Board")
    print(board)

    print("\nConflicts")
    print(
        count_conflicts(board)
    )

    print("\nPossible Actions")

    actions = problem.actions(board)

    print(
        f"{len(actions)} actions available"
    )

    print("\nNeighbours")

    neighbours = generate_neighbours(
        problem,
        board
    )

    print(
        f"{len(neighbours)} neighbours generated"
    )

    print("\nHill Climbing")

    hc_board = hill_climbing(problem, board)

    print(hc_board)
    print(f"Conflicts: {count_conflicts(hc_board)}")

    print("\nSimulated Annealing")

    sa_board = simulated_annealing(problem, board)

    print(sa_board)
    print(f"Conflicts: {count_conflicts(sa_board)}")

    compare_algorithms(N)

    print("\nRandom Restart Hill Climbing")

    for max_restarts in [1, 5, 20, 100]:

        rr_board, used = random_restart_hill_climbing(N, max_restarts)

        print(
            f"max_restarts={max_restarts:<4} "
            f"runs used={used:<4} "
            f"conflicts={count_conflicts(rr_board)}  {rr_board}"
        )