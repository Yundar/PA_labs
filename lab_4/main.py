from lab_4.constants import *
from lab_4.game import Game
from lab_4.algorithm import minimax
import pygame

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Neutreeko')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(window)

    while run:

        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 4, True, game, float('-inf'), float('inf'))
            game.ai_move(new_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()


main()
