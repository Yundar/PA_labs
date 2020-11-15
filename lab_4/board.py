import pygame
from .constants import BLACK, WHITE, ROWS, SQUARE_SIZE, COLS
from .piece import Piece
from copy import deepcopy


class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.create_board()

    def draw_squares(self, window):
        window.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(window, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if 0 < col < 4:
                    if row == 0 and col != 2:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row == 1 and col == 2:
                        self.board[row].append(Piece(row, col, BLACK))
                    elif row == 3 and col == 2:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row == 4 and col != 2:
                        self.board[row].append(Piece(row, col, BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_valid_moves(self, piece):
        moves = []
        piece_row, piece_col = piece.row, piece.col

        row, col = piece_row, piece_col
        fl = 0
        while row != 0:
            row -= 1
            if self.board[row][col] != 0:
                if row + 1 != piece_row:
                    moves.append((row + 1, col))
                fl = 1
                break
        if fl == 0 and piece_row != 0:
            moves.append((0, col))

        row, col = piece_row, piece_col
        fl = 0
        while row != 4:
            row += 1
            if self.board[row][col] != 0:
                if row - 1 != piece_row:
                    moves.append((row - 1, col))
                fl = 1
                break
        if fl == 0 and piece_row != 4:
            moves.append((4, col))

        row, col = piece_row, piece_col
        fl = 0
        while col != 0:
            col -= 1
            if self.board[row][col] != 0:
                if col + 1 != piece_col:
                    moves.append((row, col + 1))
                fl = 1
                break
        if fl == 0 and piece_col != 0:
            moves.append((row, 0))

        row, col = piece_row, piece_col
        fl = 0
        while col != 4:
            col += 1
            if self.board[row][col] != 0:
                if col - 1 != piece_col:
                    moves.append((row, col - 1))
                fl = 1
                break
        if fl == 0 and piece_col != 4:
            moves.append((row, 4))

        row, col = piece_row, piece_col
        fl = 0
        while col != 4 and row != 4:
            col += 1
            row += 1
            if self.board[row][col] != 0:
                if row - 1 != piece_row and col - 1 != piece_col:
                    moves.append((row - 1, col - 1))
                fl = 1
                break
        if fl == 0 and piece_row != 4 and piece_col != 4:
            m = max(piece_row, piece_col)
            moves.append((4 - m + piece_row, 4 - m + piece_col))

        row, col = piece_row, piece_col
        fl = 0
        while col != 0 and row != 0:
            col -= 1
            row -= 1
            if self.board[row][col] != 0:
                fl = 1
                if row + 1 != piece_row and col + 1 != piece_col:
                    moves.append((row + 1, col + 1))
                break
        if fl == 0 and piece_row != 0 and piece_col != 0:
            m = min(piece_row, piece_col)
            moves.append((0 - m + piece_row, 0 - m + piece_col))

        row, col = piece_row, piece_col
        fl = 0
        while col != 0 and row != 4:
            col -= 1
            row += 1
            if self.board[row][col] != 0:
                fl = 1
                if row - 1 != piece_row and col + 1 != piece_col:
                    moves.append((row - 1, col + 1))
                break
        if fl == 0 and piece_row != 4 and piece_col != 0:
            row, col = piece_row, piece_col
            while col != 0 and row != 4:
                col -= 1
                row += 1
                if row == 4:
                    moves.append((row, col))
                    break
                if col == 0:
                    moves.append((row, col))
                    break

        row, col = piece_row, piece_col
        fl = 0
        while col != 4 and row != 0:
            col += 1
            row -= 1
            if self.board[row][col] != 0:
                fl = 1
                if row + 1 != piece_row and col - 1 != piece_col:
                    moves.append((row + 1, col - 1))
                break
        if fl == 0 and piece_row != 0 and piece_col != 4:
            row, col = piece_row, piece_col
            while col != 4 and row != 0:
                col += 1
                row -= 1
                if row == 0:
                    moves.append((row, col))
                    break
                if col == 4:
                    moves.append((row, col))
                    break
        return moves

    def evaluate(self):
        black, white_line = self.find_pieces()
        evaluation = 0
        # vertical
        if (white_line[0][0] == white_line[1][0] == white_line[2][0]) and (
                white_line[0][1] == white_line[1][1] - 1 == white_line[2][1] - 2):
            evaluation += 10 ** 4

        # horizontal
        if (white_line[0][1] == white_line[1][1] == white_line[2][1]) and (
                white_line[0][0] == white_line[1][0] - 1 == white_line[2][0] - 2):
            evaluation += 10 ** 4

        # diagonal
        if (white_line[0][0] == white_line[1][0] - 1 == white_line[2][0] - 2) and ((
                                                                                           white_line[0][1] ==
                                                                                           white_line[1][1] - 1 ==
                                                                                           white_line[2][
                                                                                               1] - 2) or (
                                                                                           white_line[0][1] ==
                                                                                           white_line[1][1] + 1 ==
                                                                                           white_line[2][1] + 2)):
            evaluation += 10 ** 4

        return evaluation

    def find_pieces(self):
        black = []
        white = []

        for row in range(ROWS):
            for col in range(COLS):
                if len(str(self.board[row][col])) != 1:
                    if str(self.board[row][col])[1] == '2':
                        white.append((row, col))
                    if str(self.board[row][col])[1] == '0':
                        black.append((row, col))

        return black, white

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def winner(self):
        black_line, white_line = self.find_pieces()

        # vertical
        if (white_line[0][0] == white_line[1][0] == white_line[2][0]) and (
                white_line[0][1] == white_line[1][1] - 1 == white_line[2][1] - 2):
            return WHITE
        if (black_line[0][0] == black_line[1][0] == black_line[2][0]) and (
                black_line[0][1] == black_line[1][1] - 1 == black_line[2][1] - 2):
            return BLACK

        # horizontal
        if (white_line[0][1] == white_line[1][1] == white_line[2][1]) and (
                white_line[0][0] == white_line[1][0] - 1 == white_line[2][0] - 2):
            return WHITE
        if (black_line[0][1] == black_line[1][1] == black_line[2][1]) and (
                black_line[0][0] == black_line[1][0] - 1 == black_line[2][0] - 2):
            return BLACK

        # diagonal
        if (white_line[0][0] == white_line[1][0] - 1 == white_line[2][0] - 2) and ((
                                                                                           white_line[0][1] ==
                                                                                           white_line[1][1] - 1 ==
                                                                                           white_line[2][1] - 2) or (
                                                                                           white_line[0][1] ==
                                                                                           white_line[1][1] + 1 ==
                                                                                           white_line[2][1] + 2)):
            return WHITE
        if (black_line[0][0] == black_line[1][0] - 1 == black_line[2][0] - 2) and ((
                                                                                           black_line[0][1] ==
                                                                                           black_line[1][1] - 1 ==
                                                                                           black_line[2][1] - 2) or (
                                                                                           black_line[0][1] ==
                                                                                           black_line[1][1] + 1 ==
                                                                                           black_line[2][1] + 2)):
            return BLACK

        return None
