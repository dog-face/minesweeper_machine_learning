import random
from src.emulator import minesweeper_emulator
import numpy
import pickle

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
        x = random.randint(0, 8)
        y = random.randint(0, 8)

        if(game_board[y, x] == -2):
            boom, game_board = minesweeper_emulator.guess_square(game_board, true_board, x, y)
            num_moves += 1
            print("number of moves: " + str(num_moves))
            if boom:
                print("breaking")
                num_games += 1
                total_moves += num_moves
                break

    num_games += 1
    total_moves += num_moves


average_num_moves = total_moves/num_games
print("Average number of moves: " + str(average_num_moves))