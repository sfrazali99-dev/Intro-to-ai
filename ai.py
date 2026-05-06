import math
import time
from game import check_win, get_valid_cols, get_next_open_row, drop_piece, is_board_full
from heuristic import score_board

def minimax(board, depth, alpha, beta, maximizing_player, piece, time_limit, start_time):
    opponent = 1 if piece == 2 else 2

    valid_cols = get_valid_cols(board)
    is_terminal = check_win(board, piece) or check_win(board, opponent) or is_board_full(board)

    if time.time() - start_time >= time_limit:
        return (None, score_board(board, piece))

    if depth == 0 or is_terminal:
        if check_win(board, piece):
            return (None, 100000000)
        elif check_win(board, opponent):
            return (None, -100000000)
        elif is_board_full(board):
            return (None, 0)
        else:
            return (None, score_board(board, piece))

    # Move ordering: center columns first
    valid_cols = sorted(valid_cols, key=lambda c: abs(c - len(board[0]) // 2))

    if maximizing_player:
        value = -math.inf
        best_col = valid_cols[0]
        for col in valid_cols:
            row = get_next_open_row(board, col)
            board[row][col] = piece
            _, new_score = minimax(board, depth-1, alpha, beta, False, piece, time_limit, start_time)
            board[row][col] = 0
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = math.inf
        best_col = valid_cols[0]
        for col in valid_cols:
            row = get_next_open_row(board, col)
            board[row][col] = opponent
            _, new_score = minimax(board, depth-1, alpha, beta, True, piece, time_limit, start_time)
            board[row][col] = 0
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

def get_best_move(board, piece, time_limit=3.0):
    start_time = time.time()
    best_col = get_valid_cols(board)[0]
    opponent = 1 if piece == 2 else 2

    # Check for immediate winning move
    for col in get_valid_cols(board):
        row = get_next_open_row(board, col)
        board[row][col] = piece
        if check_win(board, piece):
            board[row][col] = 0
            return col
        board[row][col] = 0

    # Check for immediate block (opponent about to win)
    for col in get_valid_cols(board):
        row = get_next_open_row(board, col)
        board[row][col] = opponent
        if check_win(board, opponent):
            board[row][col] = 0
            return col
        board[row][col] = 0

    # Iterative deepening
    for depth in range(1, 10):
        if time.time() - start_time >= time_limit:
            break
        col, _ = minimax(board, depth, -math.inf, math.inf, True, piece, time_limit, start_time)
        if col is not None:
            best_col = col

    return best_col