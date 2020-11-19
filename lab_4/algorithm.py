from copy import deepcopy
import pygame
from .constants import WHITE, BLACK


def minimax(position, depth, max_player, game, alpha, beta):
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax(move, depth - 1, False, game, alpha, beta)[0]
            maxEval = max(maxEval, evaluation)
            alpha = max(alpha, evaluation)
            if maxEval == evaluation:
                best_move = move
            if beta <= alpha:
                break
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, BLACK, game):
            evaluation = minimax(move, depth - 1, True, game, alpha, beta)[0]
            minEval = min(minEval, evaluation)
            beta = min(beta, evaluation)
            if minEval == evaluation:
                best_move = move
            if beta >= 0:
                if beta < alpha:
                    break
            if beta < 0:
                if beta <= alpha:
                    break
        return minEval, best_move


def simulate_move(piece, move, board, game):
    board.move(piece, move[0], move[1])
    return board


def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move in valid_moves:
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game)
            moves.append(new_board)
    return moves
