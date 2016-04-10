import minesweeper_emulator
import numpy
import pickle

#minesweeper_emulator.play_game()

def generate_boards():
    true_board = minesweeper_emulator.generate_true_board(16, 16, 1, 1) #first guess will be set to default to 1, 1
    game_board = minesweeper_emulator.generate_game_board(true_board, 1, 1)
    #print(game_board)
    return game_board, true_board

def vectorize_game_board(board):
    vector_board = numpy.zeros((16*16), dtype=numpy.int)
    for x in range(0, 16):
        for y in range(0, 16):
            vector_board[16 * y + x] = board[y][x]
    return vector_board

def train(game_board, true_board, game_board_vector, weight_vectors):
    for this_square in range(0, 256):
        current_weight_vector = weight_vectors[this_square]
        if numpy.dot(current_weight_vector, game_board_vector) < 0:
            prediction = -1 #bomb
        else:
            prediction = 1 #no bomb
        x = this_square%16
        y = this_square//16
        if prediction == -1: #bomb
            print("marking bomb: " + str(x) + ", " + str(y) + "...")
            if not true_board[y][x] == -1: #prediction is wrong
                print("SORRY, NO BOMB.")
                weight_vectors[this_square] = numpy.add(current_weight_vector, numpy.dot(1, game_board_vector))
            else: #prediction is right
                minesweeper_emulator.mark_bomb(game_board, x, y)
                print("CORRECT!")
                minesweeper_emulator.print_board(game_board)
        if prediction == 1: #no bomb
            print("guessing square: " + str(x) + ", " + str(y))
            boom = minesweeper_emulator.guess_square(game_board, true_board, x, y)
            minesweeper_emulator.print_board(game_board)
            if boom: #prediction is wrong
                weight_vectors[this_square] = numpy.add(current_weight_vector, numpy.dot(-1, game_board_vector))
                break
            else:
                pass #nothing to do

    return boom, weight_vectors

game_board, true_board = generate_boards()
print("NEW GAME:")
print("TRUE BOARD:")
minesweeper_emulator.print_board(true_board)
print("GAME BOARD:")
minesweeper_emulator.print_board(game_board)
game_board_vector = vectorize_game_board(game_board)
#print(game_board_vector)

master_weight_vectors = numpy.zeros((16*16, 16*16))

#pickle.dump(master_weight_vectors, open("../data/master_weight_vectors", "wb"))

num_games = 0

while num_games < 500:
    game_board_vector = vectorize_game_board(game_board)
    boom, master_weight_vectors = train(game_board, true_board, game_board_vector, master_weight_vectors)
    num_games += 1
    game_board, true_board = generate_boards()
    print("NEW GAME: " + str(num_games + 1))
    print("TRUE BOARD:")
    minesweeper_emulator.print_board(true_board)
    print("GAME BOARD:")
    minesweeper_emulator.print_board(game_board)
    #print(game_board)

pickle.dump(master_weight_vectors, open("../data/master_weight_vectors", "wb"))