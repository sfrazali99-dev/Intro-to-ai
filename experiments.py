"""
experiments.py — Connect 5 AI Research Experiments
====================================================
Four experiments for the course research report:

  Exp 1 — Minimax AI vs Random Agent
  Exp 2 — Minimax AI vs Greedy Agent  ← NEW (algorithm comparison)
  Exp 3 — Time Limit vs Win Rate (Minimax vs Minimax)
  Exp 4 — First-Move Advantage
"""

import random
import time
from game import create_board, get_valid_cols, get_next_open_row, drop_piece, check_win, is_board_full
from ai import get_best_move
from heuristic import score_board

# ── Greedy Agent ──────────────────────────────────────────────────────────────

def get_greedy_move(board, piece):
    """
    Greedy agent: scores every valid column using the heuristic and picks
    the best one immediately — no lookahead, no search tree.
    """
    opponent = 1 if piece == 2 else 2
    valid_cols = get_valid_cols(board)
    best_score = -float('inf')
    best_col   = valid_cols[0]

    for col in valid_cols:
        row = get_next_open_row(board, col)
        board[row][col] = piece
        s = score_board(board, piece) - score_board(board, opponent)
        board[row][col] = 0
        if s > best_score:
            best_score = s
            best_col   = col

    return best_col

# ── Game runners ──────────────────────────────────────────────────────────────

def play_ai_vs_random(ai_piece, ai_time_limit=1.0):
    """Minimax AI vs purely random agent."""
    board = create_board()
    turn  = 1
    while True:
        valid = get_valid_cols(board)
        if not valid:
            return 0
        if turn == ai_piece:
            col = get_best_move(board, ai_piece, time_limit=ai_time_limit)
            if col is None:
                col = random.choice(valid)
        else:
            col = random.choice(valid)
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, turn)
        if check_win(board, turn):
            return turn
        turn = 1 if turn == 2 else 2


def play_ai_vs_greedy(ai_piece, ai_time_limit=1.0):
    """Minimax AI vs Greedy agent."""
    board = create_board()
    turn  = 1
    greedy_piece = 2 if ai_piece == 1 else 1

    while True:
        valid = get_valid_cols(board)
        if not valid:
            return 0
        if turn == ai_piece:
            col = get_best_move(board, ai_piece, time_limit=ai_time_limit)
            if col is None:
                col = random.choice(valid)
        else:
            col = get_greedy_move(board, greedy_piece)
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, turn)
        if check_win(board, turn):
            return turn
        turn = 1 if turn == 2 else 2


def play_ai_vs_ai(time_p1, time_p2):
    """Minimax(time_p1) vs Minimax(time_p2)."""
    board = create_board()
    turn  = 1
    while True:
        valid = get_valid_cols(board)
        if not valid:
            return 0
        tl  = time_p1 if turn == 1 else time_p2
        col = get_best_move(board, turn, time_limit=tl)
        if col is None:
            col = random.choice(valid)
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, turn)
        if check_win(board, turn):
            return turn
        turn = 1 if turn == 2 else 2


# ── Batch runner & helpers ────────────────────────────────────────────────────

def run_batch(game_fn, n, *args):
    w1, w2, draws = 0, 0, 0
    for _ in range(n):
        r = game_fn(*args)
        if r == 1:   w1 += 1
        elif r == 2: w2 += 1
        else:        draws += 1
    return w1, w2, draws

def pct(part, total):
    return f"{round(part/total*100, 1)}%" if total else "N/A"

# ── Experiment 1: Minimax vs Random ──────────────────────────────────────────

def experiment_ai_vs_random(games=10, time_limit=0.5):
    print("\n" + "=" * 60)
    print("EXPERIMENT 1: Minimax AI vs Random Agent")
    print(f"  Games: {games}  |  AI time limit: {time_limit}s")
    print("=" * 60)

    w1, w2, d = run_batch(play_ai_vs_random, games, 1, time_limit)
    print(f"\n  AI goes FIRST:")
    print(f"    AI Wins    : {w1}/{games} ({pct(w1,games)})")
    print(f"    Rand Wins  : {w2}/{games} ({pct(w2,games)})")
    print(f"    Draws      : {d}/{games}  ({pct(d,games)})")

    w1b, w2b, db = run_batch(play_ai_vs_random, games, 2, time_limit)
    print(f"\n  AI goes SECOND:")
    print(f"    AI Wins    : {w2b}/{games} ({pct(w2b,games)})")
    print(f"    Rand Wins  : {w1b}/{games} ({pct(w1b,games)})")
    print(f"    Draws      : {db}/{games}  ({pct(db,games)})")

    total_ai = w1 + w2b
    total    = games * 2
    print(f"\n  Overall AI Win Rate: {total_ai}/{total} ({pct(total_ai,total)})")

# ── Experiment 2: Minimax vs Greedy ──────────────────────────────────────────

def experiment_ai_vs_greedy(games=10, time_limit=0.5):
    print("\n" + "=" * 60)
    print("EXPERIMENT 2: Minimax AI vs Greedy Agent")
    print(f"  Games: {games}  |  AI time limit: {time_limit}s")
    print("  Greedy picks the best-scoring move RIGHT NOW, no lookahead.")
    print("=" * 60)

    w1, w2, d = run_batch(play_ai_vs_greedy, games, 1, time_limit)
    print(f"\n  Minimax goes FIRST:")
    print(f"    Minimax Wins : {w1}/{games} ({pct(w1,games)})")
    print(f"    Greedy Wins  : {w2}/{games} ({pct(w2,games)})")
    print(f"    Draws        : {d}/{games}  ({pct(d,games)})")

    w1b, w2b, db = run_batch(play_ai_vs_greedy, games, 2, time_limit)
    print(f"\n  Minimax goes SECOND:")
    print(f"    Minimax Wins : {w2b}/{games} ({pct(w2b,games)})")
    print(f"    Greedy Wins  : {w1b}/{games} ({pct(w1b,games)})")
    print(f"    Draws        : {db}/{games}  ({pct(db,games)})")

    total_ai = w1 + w2b
    total    = games * 2
    print(f"\n  Overall Minimax Win Rate vs Greedy: {total_ai}/{total} ({pct(total_ai,total)})")
    print(f"\n  → Minimax (lookahead) vs Greedy (no lookahead): lookahead {'HELPS' if total_ai > total//2 else 'does NOT help significantly'}")

# ── Experiment 3: Time Limit vs Win Rate ─────────────────────────────────────

def experiment_time_vs_winrate(games=10):
    print("\n" + "=" * 60)
    print("EXPERIMENT 3: Time Limit vs Win Rate (Minimax vs Minimax)")
    print(f"  Games per matchup: {games}  |  Opponent fixed at 0.5s")
    print("=" * 60)

    OPPONENT_TIME = 0.5
    challengers   = [0.25, 0.5, 1.0, 2.0]

    print(f"\n  {'Challenger TL':<16} {'P1 Wins':<10} {'P2 Wins':<10} {'Draws':<8} {'P1 Win%'}")
    print("  " + "-" * 52)

    for tl in challengers:
        w1, w2, d = run_batch(play_ai_vs_ai, games, tl, OPPONENT_TIME)
        print(f"  {tl:<16} {w1:<10} {w2:<10} {d:<8} {pct(w1,games)}")

# ── Experiment 4: First-Move Advantage ───────────────────────────────────────

def experiment_first_move_advantage(games=20, time_limit=1.0):
    print("\n" + "=" * 60)
    print("EXPERIMENT 4: First-Move Advantage (Minimax vs Minimax, equal time)")
    print(f"  Games: {games}  |  Both agents: {time_limit}s")
    print("=" * 60)

    w1, w2, d = run_batch(play_ai_vs_ai, games, time_limit, time_limit)
    print(f"\n  {'Outcome':<20} {'Count':<8} {'Percentage'}")
    print("  " + "-" * 38)
    print(f"  {'Piece 1 (First)':<20} {w1:<8} {pct(w1,games)}")
    print(f"  {'Piece 2 (Second)':<20} {w2:<8} {pct(w2,games)}")
    print(f"  {'Draw':<20} {d:<8} {pct(d,games)}")

    if w1 > w2:
        print("\n  → First-mover advantage OBSERVED.")
    elif w2 > w1:
        print("\n  → Second-mover advantage OBSERVED.")
    else:
        print("\n  → No clear first-mover advantage.")

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    random.seed(123)
    print("\nRunning all experiments")

    t0 = time.time()
    experiment_ai_vs_random(games=10, time_limit=0.5)
    experiment_ai_vs_greedy(games=10, time_limit=0.5)
    experiment_time_vs_winrate(games=10)
    experiment_first_move_advantage(games=20, time_limit=1.0)

    print(f"\n{'=' * 60}")
    print(f"All experiments completed in {round(time.time()-t0, 1)}s")
    print("=" * 60)