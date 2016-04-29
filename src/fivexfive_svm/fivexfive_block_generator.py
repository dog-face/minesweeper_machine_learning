import pickle
import random
import sys
import numpy

from src.emulator import minesweeper_emulator


def generate_5x5_board():
    x = random.randint(0, 6)
    y = random.randint(0, 6)
    full_board = minesweeper_emulator.generate_true_board(7, 7, x, y)#7x7 so that edge spaces can reference unseen bombs
    game_section = numpy.ones((5, 5), dtype=numpy.int) * -2#numpy.copy(full_board[1:-1, 1:-1])
    true_section = full_board[1:-1, 1:-1]

    for i in range(0, 50):
        x = random.randint(0, 4)
        y = random.randint(0, 4)
        if true_section[y, x] == -1:
            game_section[y, x] = -9
        else:
            game_section[y, x] = true_section[y, x]
            #print(str(x) + ", " + str(y))
            #boom, game_section = minesweeper_emulator.guess_square(game_section, true_section, x, y)
            #if boom:
                #print("ERROR: Bomb where there shouldn't be a bomb! 5x5_block_generator")
                #exit(1)

    '''#make all bombs unclicked
    for y in range(0, 5):
        for x in range(0, 5):
            if game_section[y][x] == -1:
                game_section[y,x] = -2

    #randomly choose some squares to be unclicked.
    num_unclicked = random.randint(0, 25)
    for i in range(0, num_unclicked):
        y = random.randint(0, 4)
        x = random.randint(0, 4)
        section[y,x] = -2'''



    '''#randomly choose some bombs to be marked.
    bomb_key = true_section == -1
    num_bombs = 0
    bomb_locs = []
    for x1 in range(0, 5):
        for y1 in range(0, 5):
            if bomb_key[y1,x1] == True:
                num_bombs += 1
                bomb_locs.append((y1,x1))
    num_marked_bombs = random.randint(0, int(num_bombs/2))
    for i in range(0, num_marked_bombs):
        index = random.randint(0, len(bomb_locs)-1)
        y1, x1 = bomb_locs[index]
        game_section[y1,x1] = -9'''

    #make center square unclicked
    game_section[2, 2] = -2

    return game_section, true_section

print("Generating training set...", end=" ")
sys.stdout.flush()
train_data = []
train_keys = []
for i in range(0, 10000):
    board_section, true_board_section = generate_5x5_board()
    #print(true_board_section)
    #print(board_section)
    train_data.append(board_section)
    if true_board_section[2, 2] == -1:
        train_keys.append(-1)
    else:
        train_keys.append(1)
print("Done. ")
#print(train_data[0])

print("Dumping to src/data/5x5_blocks_train_data.pickle...", end=" ")
sys.stdout.flush()
pickle.dump(train_data, open("../src/data/5x5_blocks_train_data.pickle", "wb"))
print("Done. ")

print("Dumping to src/data/5x5_blocks_train_keys.pickle...", end=" ")
sys.stdout.flush()
pickle.dump(train_keys, open("../src/data/5x5_blocks_train_keys.pickle", "wb"))
print("Done. ")

print("Generating validation set...", end=" ")
sys.stdout.flush()
validate_data = []
validate_keys = []
for i in range(0, 5000):
    board_section, true_board_section = generate_5x5_board()
    validate_data.append(board_section)
    if true_board_section[2, 2] == -1:
        validate_keys.append(-1)
    else:
        validate_keys.append(1)
print("Done. ")

print("Dumping to src/data/5x5_blocks_validate_data.pickle...", end=" ")
sys.stdout.flush()
pickle.dump(validate_data, open("../src/data/5x5_blocks_validate_data.pickle", "wb"))
print("Done. ")

print("Dumping to src/data/5x5_blocks_validate_keys.pickle...", end=" ")
sys.stdout.flush()
pickle.dump(validate_keys, open("../src/data/5x5_blocks_validate_keys.pickle", "wb"))
print("Done. ")

print("ALL DONE. ")