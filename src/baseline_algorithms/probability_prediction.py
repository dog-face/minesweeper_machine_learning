import random
from src.emulator import minesweeper_emulator
import numpy
import pickle

def reasonable_guess(board_section):
        if board_section[1, 1] < 0 and board_section[1, 2] < 0 and board_section[1, 3] < 0 and board_section[2, 1] < 0 and board_section[2, 3] < 0 and board_section[3, 1] < 0 and board_section[3, 2] < 0 and board_section[3, 3] < 0:
            return False
        else:
            #print(board_section)
            return True
    #print(get_5x5_section(game_board, 1, 1))

def get_5x5_section(game_board, x, y):
        return_section = numpy.zeros((5, 5), dtype=numpy.int)
        for y1 in range(-2, 3):
            for x1 in range(-2, 3):
                if x+x1 < 0 or x+x1 > board_width - 1 or y+y1 < 0 or y+y1 > board_height - 1: #if this position is out of bounds on the real board
                    return_section[y1+2,x1+2] = -2 #mark it as unknown
                else:
                    return_section[y1+2,x1+2] = game_board[y+y1][x+x1]
        return return_section

epochs = 0

total_moves = 0
num_games = 0

while epochs < 100:
    epochs += 1
    print("epoch: " + str(epochs))
    board_width = 9
    board_height = 9

    true_board = minesweeper_emulator.generate_true_board(board_height, board_width, 1, 1) #16x16 board, with starting guess 1,1
    game_board = minesweeper_emulator.generate_game_board(true_board, 1, 1)

    print(game_board)


    num_moves = 0
    while -2 in game_board:
        min_probability = 8
        best_square = (-1, -1)
        for x in range(0, board_width):
            for y in range(0, board_height):
                if game_board[y][x] == -2: #if this square is still unclicked
                    board_section = get_5x5_section(game_board, x, y)
                    if reasonable_guess(board_section):
                        probability = 0
                        neighbors = minesweeper_emulator.get_neighbors(x, y)
                        for neighbor in neighbors:
                            (x1, y1) = neighbor
                            if game_board[y1, x1] >= 0:
                                probability += game_board[y1, x1]/8
                        #print(probability)
                        if probability < min_probability:
                            min_probability = probability
                            best_square = (x, y)
        if min_probability < 8:
            print(best_square)
            x1, y1 = best_square
            boom, game_board = minesweeper_emulator.guess_square(game_board, true_board, x1, y1)
            print(game_board)
            num_moves += 1
            if boom:
                break

    num_games += 1
    total_moves += num_moves


average_num_moves = total_moves/num_games
print("Average number of moves: " + str(average_num_moves))