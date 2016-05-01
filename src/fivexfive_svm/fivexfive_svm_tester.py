from src.emulator import minesweeper_emulator
import numpy
import pickle

true_board = minesweeper_emulator.generate_true_board(16, 16, 0, 0) #16x16 board, with starting guess 1,1
game_board = minesweeper_emulator.generate_game_board(true_board, 0, 0)

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

new_train_data = []
new_train_keys = []

stuck = False
threshold = .8
while -2 in game_board:
    max_certainty = 0
    best_square = (1, 1)
    guess = 0
    if stuck: # if we didn't find any moves during last loop
        threshold = 3 * threshold / 4 #take more risks
    if not stuck: # if we did find a move last loop: reset stuck to true.
        stuck = True
        threshold = .8  #reset certainty threshold
    for x in range(0, 16):
        for y in range(0, 16):
            if game_board[y][x] == -2: #if this square is still unclicked

                board_section = get_5x5_section(game_board, x, y)
                new_train_data.append(board_section)
                if true_board[y, x] == -1:
                    new_train_keys.append(-1)
                else:
                    new_train_keys.append(1)

                #print(vectorize(board_section))
                board_section = vectorize(board_section).reshape(1, -1)
                prediction = classifier.predict_proba(board_section)
                #print(prediction)
                if(prediction[0][1] > max_certainty):
                    max_certainty = prediction[0][1]
                    best_square = (x, y)
                    guess = -1
                '''if prediction[0][1] > threshold: #confident prediction of bomb
                    game_board = minesweeper_emulator.mark_bomb(game_board, x, y)
                    print(game_board)
                    stuck = False #we found a move during this loop'''
                if(prediction[0][0] > max_certainty):
                    max_certainty = prediction[0][0]
                    best_square = (x, y)
                    guess = 1
                '''elif prediction[0][0] > threshold: #confident prediction of not bomb
                    boom, game_board = minesweeper_emulator.guess_square(game_board, true_board, x, y)
                    if boom:
                        print(game_board)
                        print("You Lose. ")
                        exit(1)
                    else:
                        print(game_board)
                        stuck = False #we found a move during this loop'''
    if guess == 1:
        x, y = best_square
        boom, game_board = minesweeper_emulator.guess_square(game_board, true_board, x, y)
        if boom:
            print(game_board)
            print("You Lose. ")
            break
        else:
            print(game_board)
        stuck = False #we found a move during this loop
    elif guess == -1:
        x, y = best_square
        game_board = minesweeper_emulator.mark_bomb(game_board, x, y)
        print(game_board)
        stuck = False #we found a move during this loop

pickle.dump(new_train_data, open("../data/new_data.pickle", "wb"))
pickle.dump(new_train_keys, open("../data/new_keys.pickle", "wb"))
