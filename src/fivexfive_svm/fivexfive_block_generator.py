import pickle
import random
import sys
import numpy

from src.emulator import minesweeper_emulator


def generate_5x5_board():
    x = random.randint(0, 6)
    y = random.randint(0, 6)
    full_board = minesweeper_emulator.generate_true_board(7, 7, x, y)#7x7 so that edge spaces can reference unseen bombs
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
    for i in range(0, num_unclicked):
        y = random.randint(0, 4)
        x = random.randint(0, 4)
        section[y,x] = -2

    #randomly choose some bombs to be marked.
    bomb_key = true_section == -1
    num_bombs = 0
    bomb_locs = []
    for x1 in range(0, 5):
        for y1 in range(0, 5):
            if bomb_key[y1,x1] == True:
                num_bombs += 1
                bomb_locs.append((y1,x1))
    num_marked_bombs = random.randint(0, num_bombs)
    for i in range(0, num_marked_bombs):
        index = random.randint(0, len(bomb_locs)-1)
        y1, x1 = bomb_locs[index]
        section[y1,x1] = -9

    return section, true_section

print("Generating Boards...", end=" ")
sys.stdout.flush()
data = []
keys = []
for i in range(0, 20000):
    board_section, true_board_section = generate_5x5_board()
    #print(true_board_section)
    #print(board_section)
    data.append(board_section)
    if true_board_section[2, 2] == -1:
        keys.append(-1)
    else:
        keys.append(1)
print("Done. ")
print(data[0])

print("Dumping to src/data/5x5_blocks_data.pickle...", end=" ")
sys.stdout.flush()
pickle.dump(data, open("../src/data/5x5_blocks_data.pickle", "wb"))
print("Done. ")

print("Dumping to src/data/5x5_blocks_keys.pickle...", end=" ")
sys.stdout.flush()
pickle.dump(keys, open("../src/data/5x5_blocks_keys.pickle", "wb"))
print("Done. ")

print("ALL DONE. ")