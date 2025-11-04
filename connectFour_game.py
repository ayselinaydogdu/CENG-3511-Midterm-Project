import numpy as np
import math
import random


row_count = 6
column_count = 7
ai_piece = 2
player_piece = 1
empty = 0
WINDOW_LENGTH = 4


def create_board():
    return np.zeros((row_count, column_count), int)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[0][col] == 0

def get_next_open_row(board, col):
    for r in range(row_count - 1, -1, -1):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(board)

def winning_state(board, piece):
    # yatay kontrol
    for c in range(column_count - 3):
        for r in range(row_count):
            if all(board[r][c + i] == piece for i in range(4)):
                return True
    # dikey kontrol
    for c in range(column_count):
        for r in range(row_count - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return True
    # çapraz (sol üst -> sağ alt)
    for c in range(column_count - 3):
        for r in range(row_count - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True
    # çapraz (sağ üst -> sol alt)
    for c in range(column_count - 3):
        for r in range(3, row_count):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True
    return False


def get_valid_locations(board):
    return [col for col in range(column_count) if is_valid_location(board, col)]

def evaluate_window(window, piece):

    score = 0
    opp_piece = player_piece if piece == ai_piece else ai_piece

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(empty) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(empty) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(empty) == 1:
        score -= 4

    return score

def score_position(board, piece):

    score = 0

    center_array = [int(i) for i in list(board[:, column_count // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Yatay puan
    for r in range(row_count):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(column_count - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Dikey puan
    for c in range(column_count):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(row_count - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Çapraz (pozitif eğimli)
    for r in range(row_count - 3):
        for c in range(column_count - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    ## Çapraz (negatif eğimli)
    for r in range(3, row_count):
        for c in range(column_count - 3):
            window = [board[r - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def is_terminal_node(board):
    return winning_state(board, player_piece) or winning_state(board, ai_piece) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_state(board, ai_piece):
                return (None, 1000000000000)
            elif winning_state(board, player_piece):
                return (None, -1000000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, ai_piece))

    if maximizingPlayer:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, ai_piece)
            new_score = minimax(temp_board, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value

    else:
        value = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, player_piece)
            new_score = minimax(temp_board, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

def get_best_move(board):
    column, _ = minimax(board, depth=4, alpha=-math.inf, beta=math.inf, maximizingPlayer=True)
    return column

def main():
    board = create_board()
    game_over = False
    turn = 0  # 0 = player, 1 = AI

    print_board(board)

    while not game_over:
        if turn == 0:
            try:
                col = int(input("Player, select a column from 0-6: "))
            except ValueError:
                print("Invalid input. Please enter a number between 0-6.")
                continue

            if 0 <= col < column_count and is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, player_piece)

                if winning_state(board, player_piece):
                    print_board(board)
                    print("The player won")
                    game_over = True
            else:
                print("This column is invalid or full. Try again.")
        else:
            col = get_best_move(board)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, ai_piece)
                print(f"🤖 AI selected column  {col} ")

                if winning_state(board, ai_piece):
                    print_board(board)
                    print("AI won")
                    game_over = True

        print_board(board)
        turn = (turn + 1) % 2

if __name__ == "__main__":
    main()
