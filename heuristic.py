from game import ROWS, COLS, WIN_LENGTH

def score_window(window, piece):
    opponent = 1 if piece == 2 else 2
    score = 0

    piece_count = window.count(piece)
    opp_count = window.count(opponent)
    empty_count = window.count(0)

    if piece_count == WIN_LENGTH:
        score += 100000
    elif piece_count == WIN_LENGTH - 1 and empty_count == 1:
        score += 1000
    elif piece_count == WIN_LENGTH - 2 and empty_count == 2:
        score += 100
    elif piece_count == WIN_LENGTH - 3 and empty_count == 3:
        score += 10

    if opp_count == WIN_LENGTH - 1 and empty_count == 1:
        score -= 2000
    elif opp_count == WIN_LENGTH - 2 and empty_count == 2:
        score -= 200

    return score

def score_board(board, piece):
    score = 0

   # Center area preference (multiple columns)
    for offset in [-1, 0, 1]:
      center_col = COLS // 2 + offset
      center_array = [board[r][center_col] for r in range(ROWS)]
      score += center_array.count(piece) * 4

    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - WIN_LENGTH + 1):
            window = [board[r][c+i] for i in range(WIN_LENGTH)]
            score += score_window(window, piece)

    # Vertical
    for r in range(ROWS - WIN_LENGTH + 1):
        for c in range(COLS):
            window = [board[r+i][c] for i in range(WIN_LENGTH)]
            score += score_window(window, piece)

    # Diagonal down-right
    for r in range(ROWS - WIN_LENGTH + 1):
        for c in range(COLS - WIN_LENGTH + 1):
            window = [board[r+i][c+i] for i in range(WIN_LENGTH)]
            score += score_window(window, piece)

    # Diagonal down-left
    for r in range(ROWS - WIN_LENGTH + 1):
        for c in range(WIN_LENGTH - 1, COLS):
            window = [board[r+i][c-i] for i in range(WIN_LENGTH)]
            score += score_window(window, piece)

    return score