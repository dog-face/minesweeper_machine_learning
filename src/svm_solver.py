from sklearn.svm import SVC
import numpy
import pickle
import minesweeper_emulator

data = pickle.load(open("data/5x5_blocks_data.pickle", "rb"))
keys = pickle.load(open("data/5x5_blocks_keys.pickle", "rb"))
vector_data = []

for board in data:
    #print(board)
    vector_board = board.reshape(1, 25)
    vector_data.append(vector_board[0])
    #print(board)

#print(vector_data[0])

classifier = SVC(C=1.0, kernel='rbf', degree=3)
classifier.fit(vector_data, keys)

pickle.dump(classifier, open("data/SVC_classifier.pickle", "wb"))

def generate_boards():
    true_board = minesweeper_emulator.generate_true_board(16, 16, 1, 1) #first guess will be set to default to 1, 1
    game_board = minesweeper_emulator.generate_game_board(true_board, 1, 1)
    return game_board, true_board

game_board, true_board = generate_boards()
print(game_board)

def vectorize_section(section):
    assert(section.shape == (5, 5))
    vector_section = section.reshape(1, 25)
    #print(vector_section[0])
    return vector_section[0]

def is_in_range(x, y, game_board):
    width, height = game_board.shape
    if x < 0:
        return False
    if x >= width:
        return False
    if y < 0:
        return False
    if y >= height:
        return False
    return True

def generate_5x5_section(game_board, x1, y1):
    this_section = numpy.zeros((5, 5), dtype=numpy.int)
    for s_x, gb_x in enumerate(range(x1-2, x1+3)):
        for s_y, gb_y in enumerate(range(y1-2, y1+3)):
            #print("s_x = " + str(s_x) + ", gb_x = " + str(gb_x))
            #print("s_y = " + str(s_y) + ", gb_y = " + str(gb_y))
            if is_in_range(gb_x, gb_y, game_board):
                this_section[s_y, s_x] = game_board[gb_y, gb_x]
            else:
                this_section[s_y, s_x] = -2
    return this_section


def evaluate_squares(game_board, true_board):
    for x in range(0, 16):
        for y in range(0, 16):
            #print("x = " + str(x) + ", y = " + str(y))
            this_section = generate_5x5_section(game_board, x, y)
            #print(this_section)
            this_section_vector = vectorize_section(this_section)
            this_section_vector = this_section_vector.reshape(1, -1)
            prediction = classifier.predict(this_section_vector)
            if prediction == 1:
                minesweeper_emulator.guess_square(game_board, true_board, x, y)
            #if prediction == -1:
                #minesweeper_emulator.mark_bomb(game_board, x, y)
            print(game_board)

evaluate_squares(game_board, true_board)