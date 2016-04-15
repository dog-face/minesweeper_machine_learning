import minesweeper_emulator
import numpy
import pickle
import random

def generate_5x5_board():
    full_board = minesweeper_emulator.generate_true_board(7, 7, 1, 1)#7x7 so that edge spaces can reference unseen bombs
    section = numpy.copy(full_board[1:-1, 1:-1])
    true_section = full_board[1:-1, 1:-1]
    #make all bombs unclicked
    for y in range(0, 5):
        for x in range(0, 5):
            if section[y][x] == -1:
                section[y,x] = -2

    #make center square unclicked
    section[2, 2] = -2

    #randomly choose some squares to be unclicked.
    num_unclicked = random.randint(0, 25)
    for y in range(0, num_unclicked):
        y = random.randint(0, 4)
        x = random.randint(0, 4)
        section[y,x] = -2

    return section, true_section

data = []
keys = []
for i in range(0, 2000):
    board_section, true_board_section = generate_5x5_board()
    #print(true_board_section)
    #print(board_section)
    data.append(board_section)
    if true_board_section[2, 2] == -1:
        keys.append(-1)
    else:
        keys.append(1)

pickle.dump(data, open("../data/5x5_blocks_data.pickle", "wb"))
pickle.dump(keys, open("../data/5x5_blocks_keys.pickle", "wb"))