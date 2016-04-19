from src.emulator import minesweeper_emulator
import numpy
import pickle

true_board = minesweeper_emulator.generate_true_board(16, 16, 1, 1) #16x16 board, with starting guess 1,1
game_board = minesweeper_emulator.generate_game_board(true_board, 1, 1)

print(game_board)

def get_5x5_section(game_board, x, y):
    return_section = numpy.zeros((5, 5), dtype=numpy.int)
    for y1 in range(-2, 3):
        for x1 in range(-2, 3):
            if x+x1 < 0 or x+x1 > 15 or y+y1 < 0 or y+y1 > 15: #if this position is out of bounds on the real board
                return_section[y1+2,x1+2] = -2 #mark it as unknown
            else:
                return_section[y1+2,x1+2] = game_board[y+y1][x+x1]
    return return_section

def vectorize(board_section):
    return board_section.reshape(25)


#print(get_5x5_section(game_board, 1, 1))

classifier = pickle.load(open("../data/5x5_trained_svm_classifier.pickle", "rb"))

while -2 in game_board:
    for x in range(0, 16):
        for y in range(0, 16):
            if game_board[y][x] == -2: #if this square is still unclicked
                board_section = get_5x5_section(game_board, x, y)
                #print(vectorize(board_section))
                board_section = vectorize(board_section).reshape(1, -1)
                prediction = classifier.predict_proba(board_section)
                #print(prediction)
                if prediction[0][1] > .75: #confident prediction of bomb
                    game_board = minesweeper_emulator.mark_bomb(game_board, x, y)
                    print(game_board)
                if prediction[0][0] > .75: #confident prediction of not bomb
                    boom, game_board = minesweeper_emulator.guess_square(game_board, true_board, x, y)
                    if boom:
                        print("You Lose. ")
                        exit(1)
                    else:
                        print(game_board)
