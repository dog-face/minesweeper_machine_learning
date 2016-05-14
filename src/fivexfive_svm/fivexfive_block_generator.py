import pickle
import random
import sys
import numpy

from src.emulator import minesweeper_emulator


def generate_early_board():
    full_board = minesweeper_emulator.generate_true_board(7, 7, 1, 1)#7x7 so that edge spaces can reference unseen bombs
    game_section = numpy.ones((5, 5), dtype=numpy.int) * -2#numpy.copy(full_board[1:-1, 1:-1])
    true_section = full_board[1:-1, 1:-1]
    for x in range(0, 3):
        for y in range(0, 3):
            if true_section[y, x] != -1:
                game_section[y, x] = true_section[y, x]
    return game_section, true_section

def generate_5x5_board():
    x = random.randint(0, 6)
    y = random.randint(0, 6)
    full_board = minesweeper_emulator.generate_true_board(7, 7, x, y)#7x7 so that edge spaces can reference unseen bombs
    game_section = numpy.ones((5, 5), dtype=numpy.int) * -2#numpy.copy(full_board[1:-1, 1:-1])
    true_section = full_board[1:-1, 1:-1]

    for i in range(0, 25):
        x = random.randint(0, 4)
        y = random.randint(0, 4)
        if true_section[y, x] == -1:
            game_section[y, x] = -9
        else:
            game_section[y, x] = true_section[y, x]

    #make center square unclicked
    game_section[2, 2] = -2

    return game_section, true_section

print("Generating training set...", end=" ")
sys.stdout.flush()
train_data = []
train_keys = []
for i in range(0, 5000):
    board_section, true_board_section = generate_early_board()
    train_data.append(board_section)
    #print(board_section)
    if true_board_section[2, 2] == -1:
        train_keys.append(-1)
    else:
        train_keys.append(1)
for i in range(0, 10000):
    board_section, true_board_section = generate_5x5_board()
    train_data.append(board_section)
    if true_board_section[2, 2] == -1:
        train_keys.append(-1)
    else:
        train_keys.append(1)
print("Done. ")
#print(train_data[0])

print("Dumping to src/data/generation_train_data.pickle...", end=" ")
sys.stdout.flush()
pickle.dump(train_data, open("../data/generation_train_data.pickle", "wb"))
print("Done. ")

print("Dumping to src/data/generation_train_keys.pickle...", end=" ")
sys.stdout.flush()
pickle.dump(train_keys, open("../data/generation_train_keys.pickle", "wb"))
print("Done. ")

print("Generating validation set...", end=" ")
sys.stdout.flush()
validate_data = []
validate_keys = []
for i in range(0, 5000):
    board_section, true_board_section = generate_early_board()
    validate_data.append(board_section)
    if true_board_section[2, 2] == -1:
        validate_keys.append(-1)
    else:
        validate_keys.append(1)
for i in range(0, 5000):
    board_section, true_board_section = generate_5x5_board()
    validate_data.append(board_section)
    if true_board_section[2, 2] == -1:
        validate_keys.append(-1)
    else:
        validate_keys.append(1)
print("Done. ")

print("Dumping to src/data/generation_validate_data.pickle...", end=" ")
sys.stdout.flush()
pickle.dump(validate_data, open("../data/generation_validate_data.pickle", "wb"))
print("Done. ")

print("Dumping to src/data/generation_validate_keys.pickle...", end=" ")
sys.stdout.flush()
pickle.dump(validate_keys, open("../data/generation_validate_keys.pickle", "wb"))
print("Done. ")

print("ALL DONE. ")