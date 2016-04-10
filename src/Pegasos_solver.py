import minesweeper_emulator
import numpy

#minesweeper_emulator.play_game()

def generate_boards():
    true_board = minesweeper_emulator.generate_true_board(16, 16, 1, 1) #first guess will be set to default to 1, 1
    game_board = minesweeper_emulator.generate_game_board(true_board, 1, 1)
    print(game_board)
    return game_board, true_board

def vectorize_game_board(board):
    vector_board = numpy.zeros((16*16))
    for x in range(0, 16):
        for y in range(0, 16)

def train(game_board_vector, weight_vector):

    return 0

game_board, true_board = generate_boards()
vectorize_game_board(game_board)
