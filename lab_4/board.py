import pygame
from .constants import BLACK, WHITE, ROWS, SQUARE_SIZE, COLS
from .piece import Piece


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
        for row in range(ROWS):
            for col in range(COLS):
                if row + 1 == piece_row or row - 1 == piece_row or row == piece_row:
                    if col + 1 == piece_col or col - 1 == piece_col or col == piece_col:
                        if self.board[row][col] == 0:
                            moves.append((row, col))
        return moves

    def evaluate(self):
        if self.winner() == WHITE:
            return 3
        elif self.winner() == BLACK:
            return 0
        else:
            return 2

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def winner(self):
        black_line = []
        white_line = []

        for row in range(ROWS):
            for col in range(COLS):
                if len(str(self.board[row][col])) != 1:
                    if str(self.board[row][col])[1] == '2':
                        white_line.append((row, col))
                    if str(self.board[row][col])[1] == '0':
                        black_line.append((row, col))

        if white_line[2][1] - white_line[1][1] == white_line[1][1] - white_line[0][1] and white_line[2][0] - \
                white_line[1][0] == white_line[1][0] - white_line[0][0]:
            return WHITE

        if black_line[2][1] - black_line[1][1] == black_line[1][1] - black_line[0][1] and black_line[2][0] - \
                black_line[1][0] == black_line[1][0] - black_line[0][0]:
            return BLACK

        return None
