import pygame
import sys
from game import *

# Colors
BLUE = (0, 105, 148)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
YELLOW = (240, 200, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK = (30, 30, 30)

CELL_SIZE = 60
RADIUS = CELL_SIZE // 2 - 5
HEADER = 80
SIDEBAR = 220

def init_layout():
    global CELL_SIZE, RADIUS, HEADER, SIDEBAR, WINDOW_WIDTH, WINDOW_HEIGHT
    info = pygame.display.Info()
    cell_from_w = int(info.current_w * 0.80) // (COLS + 4)
    cell_from_h = int(info.current_h * 0.80) // (ROWS + 1)
    CELL_SIZE   = max(32, min(cell_from_w, cell_from_h))
    RADIUS        = CELL_SIZE // 2 - max(3, CELL_SIZE // 12)
    HEADER        = max(50, int(CELL_SIZE * 1.15))
    SIDEBAR       = max(160, int(CELL_SIZE * 3.8))
    WINDOW_WIDTH  = COLS * CELL_SIZE + SIDEBAR
    WINDOW_HEIGHT = ROWS * CELL_SIZE + HEADER

WINDOW_WIDTH = COLS * CELL_SIZE + SIDEBAR
WINDOW_HEIGHT = ROWS * CELL_SIZE + HEADER

def draw_board(screen, board, font):
    screen.fill(DARK)

    # Sidebar
    pygame.draw.rect(screen, (45, 45, 45), (COLS * CELL_SIZE, 0, SIDEBAR, WINDOW_HEIGHT))

    # Title
    title = font.render("Connect 5", True, WHITE)
    screen.blit(title, (20, 20))

    # Board background
    pygame.draw.rect(screen, BLUE, (0, HEADER, COLS * CELL_SIZE, ROWS * CELL_SIZE))

    for r in range(ROWS):
        for c in range(COLS):
            x = c * CELL_SIZE + CELL_SIZE // 2
            y = r * CELL_SIZE + HEADER + CELL_SIZE // 2
            color = BLACK
            if board[r][c] == 1:
                color = RED
            elif board[r][c] == 2:
                color = YELLOW
            pygame.draw.circle(screen, color, (x, y), RADIUS)

    pygame.display.update()

def draw_sidebar(screen, font, small_font, turn, game_over, winner, difficulty):
    x = COLS * CELL_SIZE + 10
    pygame.draw.rect(screen, (45, 45, 45), (COLS * CELL_SIZE, 0, SIDEBAR, WINDOW_HEIGHT))

    # Turn info
    label = font.render("Turn:", True, WHITE)
    screen.blit(label, (x, 20))
    color = RED if turn == 1 else YELLOW
    name = "Player" if turn == 1 else "AI"
    turn_text = font.render(name, True, color)
    screen.blit(turn_text, (x, 50))

    # Difficulty
    diff_label = small_font.render(f"Difficulty: {difficulty}", True, GRAY)
    screen.blit(diff_label, (x, 110))

    # Controls
    screen.blit(small_font.render("R - Restart", True, GRAY), (x, 160))
    screen.blit(small_font.render("ESC - Quit", True, GRAY), (x, 185))
    screen.blit(small_font.render("1 - Easy", True, GRAY), (x, 210))
    screen.blit(small_font.render("2 - Medium", True, GRAY), (x, 235))
    screen.blit(small_font.render("3 - Hard", True, GRAY), (x, 260)) 
    # Winner
    if game_over:
        if winner == 1:
            msg = font.render("You Win!", True, RED)
        elif winner == 2:
            msg = font.render("AI Wins!", True, YELLOW)
        else:
            msg = font.render("Draw!", True, WHITE)
        screen.blit(msg, (x, 300))
        screen.blit(small_font.render("R to play again", True, GRAY), (x, 340))

    pygame.display.update()

def get_col_from_mouse(x):
    if x < COLS * CELL_SIZE:
        return x // CELL_SIZE
    return None