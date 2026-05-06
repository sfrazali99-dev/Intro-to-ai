import threading
import pygame
import sys
from game import *
from ai import get_best_move
from gui import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),pygame.FULLSCREEN)
    pygame.display.set_caption("Connect 5 AI")
    font = pygame.font.SysFont("segoeui", 28, bold=True)
    small_font = pygame.font.SysFont("segoeui", 20)

    board = create_board()
    game_over = False
    turn = 1  # 1 = human, 2 = AI
    winner = None
    difficulty = "Medium"
    ai_thinking = False
    ai_result = [None]
    time_map = {"Easy": 1.0, "Medium": 3.0, "Hard": 5.0}

    draw_board(screen, board, font)
    draw_sidebar(screen, font, small_font, turn, game_over, winner, difficulty)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                   pygame.quit()
                   sys.exit()
                if event.key == pygame.K_r:
                    board = create_board()
                    game_over = False
                    turn = 1
                    winner = None
                    draw_board(screen, board, font)
                    draw_sidebar(screen, font, small_font, turn, game_over, winner, difficulty)

                if event.key == pygame.K_1:
                    difficulty = "Easy"
                    draw_sidebar(screen, font, small_font, turn, game_over, winner, difficulty)
                if event.key == pygame.K_2:
                    difficulty = "Medium"
                    draw_sidebar(screen, font, small_font, turn, game_over, winner, difficulty)
                if event.key == pygame.K_3:
                    difficulty = "Hard"
                    draw_sidebar(screen, font, small_font, turn, game_over, winner, difficulty)

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and turn == 1:
                x = event.pos[0]
                col = get_col_from_mouse(x)
                if col is not None and is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if check_win(board, 1):
                        game_over = True
                        winner = 1
                    elif is_board_full(board):
                        game_over = True
                        winner = None

                    turn = 2
                    draw_board(screen, board, font)
                    draw_sidebar(screen, font, small_font, turn, game_over, winner, difficulty)

# AI turn
        if not game_over and turn == 2 and not ai_thinking:
            ai_thinking = True
            ai_result = [None]
            def ai_worker():
                time_limit = time_map[difficulty]
                ai_result[0] = get_best_move(board, 2, time_limit=time_limit)
            threading.Thread(target=ai_worker, daemon=True).start()

        if ai_thinking and ai_result[0] is not None:
            col = ai_result[0]
            ai_thinking = False
            if col is not None and is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)
                if check_win(board, 2):
                    game_over = True
                    winner = 2
                elif is_board_full(board):
                    game_over = True
                    winner = None
                turn = 1
                draw_board(screen, board, font)
                draw_sidebar(screen, font, small_font, turn, game_over, winner, difficulty)

if __name__ == "__main__":
    main()