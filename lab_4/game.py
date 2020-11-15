import pygame
from lab_4.board import Board
from .constants import BLACK, WHITE, GREY, SQUARE_SIZE, ROWS, COLS
from tkinter import messagebox


class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = []

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            self.winner()
        else:
            return False

        return True

    def change_turn(self):
        self.valid_moves = []
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, GREY,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 10)

    def winner(self):
        line = []

        for row in range(ROWS):
            for col in range(COLS):
                if len(str(self.board.board[row][col])) != 1:
                    if str(self.board.board[row][col])[1] == '2' and self.turn[0] == 255:
                        line.append((row, col))
                    if str(self.board.board[row][col])[1] == '0' and self.turn[0] == 0:
                        line.append((row, col))

        if len(line) == 3:
            # vertical
            if (line[0][0] == line[1][0] == line[2][0]) and (
                    line[0][1] == line[1][1] - 1 == line[2][1] - 2):
                if self.turn[0] == 255:
                    self.turn = 'White'
                else:
                    self.turn = 'Black'
                self.valid_moves = []
                messagebox.showinfo('Winner', str(self.turn))
                return True

            # horizontal
            if (line[0][1] == line[1][1] == line[2][1]) and (
                    line[0][0] == line[1][0] - 1 == line[2][0] - 2):
                if self.turn[0] == 255:
                    self.turn = 'White'
                else:
                    self.turn = 'Black'
                self.valid_moves = []
                messagebox.showinfo('Winner', str(self.turn))
                return True

            # diagonal
            if (line[0][0] == line[1][0] - 1 == line[2][0] - 2) and ((
                                                                             line[0][1] ==
                                                                             line[1][1] - 1 ==
                                                                             line[2][
                                                                                 1] - 2) or (
                                                                             line[0][1] ==
                                                                             line[1][1] + 1 ==
                                                                             line[2][1] + 2)):
                if self.turn[0] == 255:
                    self.turn = 'White'
                else:
                    self.turn = 'Black'
                self.valid_moves = []
                messagebox.showinfo('Winner', str(self.turn))
                return True

        self.change_turn()

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.winner()
