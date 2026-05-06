ROWS = 12
COLS = 12
WIN_LENGTH = 5

def create_board():
    return [[0] * COLS for _ in range(ROWS)]

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[0][col] == 0

def get_next_open_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == 0:
            return r

def check_win(board, piece):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - WIN_LENGTH + 1):
            if all(board[r][c+i] == piece for i in range(WIN_LENGTH)):
                return True
    # Vertical
    for r in range(ROWS - WIN_LENGTH + 1):
        for c in range(COLS):
            if all(board[r+i][c] == piece for i in range(WIN_LENGTH)):
                return True
    # Diagonal down-right
    for r in range(ROWS - WIN_LENGTH + 1):
        for c in range(COLS - WIN_LENGTH + 1):
            if all(board[r+i][c+i] == piece for i in range(WIN_LENGTH)):
                return True
    # Diagonal down-left
    for r in range(ROWS - WIN_LENGTH + 1):
        for c in range(WIN_LENGTH - 1, COLS):
            if all(board[r+i][c-i] == piece for i in range(WIN_LENGTH)):
                return True
    return False

def is_board_full(board):
    return all(board[0][c] != 0 for c in range(COLS))

def get_valid_cols(board):
    return [c for c in range(COLS) if is_valid_location(board, c)]

def print_board(board):
    for row in board:
        print(row)