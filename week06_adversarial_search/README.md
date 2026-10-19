# Week 6 — Adversarial Search

**AINL3001 — Knowledge-Driven AI · BSP 2026**

## Learning objectives

By the end of this lab you should be able to represent a game state, distinguish terminal states from utility scores, implement Minimax, choose an AI move, count searched nodes, and compare Minimax with Alpha-Beta Pruning. You should also be able to explain why games differ from single-agent search and CSPs.

## Getting started

Open your own fork of the course repository in VS Code. Follow the [main README](../README.md) if you need to set up your environment or pull updates from the module's `upstream` repository.

Open **`week06_adversarial_search/adversarial_search_starter.py`** and click **Run Python File**. The file uses standard Python; no new dependencies are needed. Complete the TODOs in order and rerun after each stage. The lecturer will release `adversarial_search_solution.py` later.

## Background

In previous weeks, you searched for paths, better states, or valid assignments. In a two-player game, the opponent also chooses moves and may deliberately work against you. We therefore consider possible sequences of *both* players' actions.

We use Tic-Tac-Toe: **X is MAX**, trying to maximise utility; **O is MIN**, trying to minimise it. Both players are assumed to play optimally. A completed game scores **+1 for X winning, -1 for O winning, and 0 for a draw**.

## Task 0 — Manual Minimax

Study the small tree printed by the starter:

```text
            MAX
           /   \
         MIN   MIN
        /  \   /  \
       3    5  2    9
```

Discuss: What does each MIN node return? What does MAX choose? Which branch should MAX follow? Explain why MIN and MAX make different choices.

## Task 1 — Board representation

The board is a nine-element list in row-major order. Empty cells contain a space (`" "`). Positions are numbered as follows:

```text
0 | 1 | 2
--+---+--
3 | 4 | 5
--+---+--
6 | 7 | 8
```

Implement `print_board(state)`, `available_moves(state)` and `make_move(state, move, player)`. The last function must **return a new board**, leaving the original unchanged. Inspect the provided starting board: it is X's turn, with four empty cells.

## Task 2 — Game outcomes

Implement `check_winner(state)` using the provided `WINNING_LINES`, then `is_terminal(state)` and `utility(state)`.

A **terminal state** is a win for either player or a full board (draw). `utility()` returns the result score. For this exercise, Minimax calls `utility()` only at terminal states. A non-terminal board with utility 0 is **not** necessarily a draw.

Test the functions using boards where X wins, O wins, and the game ends in a draw.

## Task 3 — Minimax

Implement `minimax(state, maximizing, counter)` recursively. At each node:

1. Count the visited node by increasing `counter["nodes"]`.
2. If the board is terminal, return its utility.
3. If X moves next (`maximizing=True`), try every legal X move and return the **maximum** child score.
4. Otherwise try every legal O move and return the **minimum** child score.

Use `make_move()` to create a fresh board for each possible move. Do not alter the original board while searching.

Why does MAX take the largest score, while MIN takes the smallest?

## Task 4 — Choose the AI's move

Implement `best_move(state, counter)` to choose the best move for **X**. For each legal X move, call `minimax()` for the resulting position with **O to play next**. Return the index of the highest-scoring move. Return `None` if the game is already over. If moves tie, choose the first in the list.

The testing area prints the selected move and displays the resulting board. The starting position has an immediate winning move for X. Can you identify it before running the solution?

**Optional interaction:** Adapt the testing code to ask a human for an O move and alternate between the human and the X agent. You can also explore AI versus AI. This is not required for the core lab.

## Task 5 — Count visited nodes

Use the `counter` dictionary already passed into `minimax()` and `best_move()`:

```python
counter = {"nodes": 0}
```

Increment it **once per call to the recursive search function**, including terminal nodes. The counter measures *game-tree nodes visited*, not unique board configurations. Different move sequences may lead to equivalent positions, but this lab does not deduplicate them.

How many nodes does Minimax visit from the supplied board? What might happen on a much larger board?

## Task 6 — Alpha-Beta Pruning

Implement `alpha_beta(state, maximizing, alpha, beta, counter)` and `best_move_alpha_beta(state, counter)`.

- `alpha` tracks the best score MAX can guarantee so far.
- `beta` tracks the best score MIN can guarantee so far.
- When `alpha >= beta`, remaining branches at that node need not be searched.

Alpha-Beta should return the **same optimal game value** as Minimax while potentially visiting fewer nodes. The testing area runs both approaches on the **same starting board** with separate counters.

Record your results:

| Algorithm | Chosen move | Nodes visited |
|---|---|---|
| Minimax | | |
| Alpha-Beta | | |

Did both choose the same move? Which visited fewer nodes? Does Alpha-Beta always prune the same amount regardless of move ordering?

## GitHub task

Commit your changes to your own fork as you complete the stages. Suggested messages:

```bash
git add week06_adversarial_search/adversarial_search_starter.py
git commit -m "Implement Tic-Tac-Toe board and utility"

git add week06_adversarial_search/adversarial_search_starter.py
git commit -m "Implement Minimax and AI move selection"

git add week06_adversarial_search/adversarial_search_starter.py
git commit -m "Compare Minimax and Alpha-Beta pruning"

git push origin main
```

## Reflection

1. Why is Tic-Tac-Toe considered a search problem?
2. Why does Minimax assume an optimal opponent?
3. What is the purpose of a utility function?
4. What happens as games become larger?

## Extensions

**Depth-limited search.** Add a `depth` parameter and stop recursion after a fixed number of levels, such as 3. A depth cutoff is not necessarily a terminal game state, so consider how to evaluate it.

**Heuristic evaluation.** Develop an estimate for non-terminal positions (e.g. two X marks in an open line, an opponent threat). Use it at the depth cutoff rather than treating every unfinished position as a draw. How does this affect move quality?

**Connect Four.** Research why searching its game tree is more demanding than Tic-Tac-Toe. No implementation is required.

## Checklist

- [ ] Explain the manual MIN/MAX tree.
- [ ] Display a board, list moves, and return a copied board after a move.
- [ ] Detect wins, draws and terminal states.
- [ ] Implement recursive Minimax and choose a move for X.
- [ ] Count visited nodes consistently.
- [ ] Implement Alpha-Beta and compare it with Minimax.
- [ ] Answer the reflection questions and push work to your fork.

**Key takeaway:** Minimax chooses a move by considering an opponent who plays optimally. Alpha-Beta Pruning avoids exploring branches that cannot affect the final decision.
