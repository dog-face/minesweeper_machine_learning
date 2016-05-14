from src.emulator import minesweeper_emulator
import numpy
import pickle

epochs = 0

total_moves = 0
num_games = 0

while epochs < 100: #Total number of games to play per session
    epochs += 1
    print(epochs)
    board_width = 9
    board_height = 9

    true_board = minesweeper_emulator.generate_true_board(board_height, board_width, 1, 1) #16x16 board, with starting guess 1,1
    game_board = minesweeper_emulator.generate_game_board(true_board, 1, 1)

    print(game_board)

    def get_5x5_section(game_board, x, y):
        return_section = numpy.zeros((5, 5), dtype=numpy.int)
        for y1 in range(-2, 3):
            for x1 in range(-2, 3):
                if x+x1 < 0 or x+x1 > board_width - 1 or y+y1 < 0 or y+y1 > board_height - 1: #if this position is out of bounds on the real board
                    return_section[y1+2,x1+2] = -2 #mark it as unknown
                else:
                    return_section[y1+2,x1+2] = game_board[y+y1][x+x1]
        return return_section

    def vectorize(board_section):
        return board_section.reshape(25)

    def reasonable_guess(board_section):
        if board_section[1, 1] < 0 and board_section[1, 2] < 0 and board_section[1, 3] < 0 and board_section[2, 1] < 0 and board_section[2, 3] < 0 and board_section[3, 1] < 0 and board_section[3, 2] < 0 and board_section[3, 3] < 0:
            return False
        else:
            return True

    #choose your classifier here
    classifier = pickle.load(open("../data/generation_svm_classifier.pickle", "rb"))
    #classifier = pickle.load(open("../data/gameplay_svm_classifier.pickle", "rb"))

    #Generate data as we go
    #new_train_data = pickle.load(open("../data/gameplay_data.pickle", "rb"))
    #new_train_keys = pickle.load(open("../data/gameplay_keys.pickle", "rb"))

    stuck = False
    num_moves = 0
    while -2 in game_board and stuck is False:
        stuck = True
        max_certainty = 0
        best_square = (1, 1)
        guess = 0
        predictions = numpy.zeros((16, 16))
        for x in range(0, board_width):
            for y in range(0, board_height):
                if game_board[y][x] == -2: #if this square is still unclicked
                    board_section = get_5x5_section(game_board, x, y)
                    if reasonable_guess(board_section):

                        #Generate data as we go
                        '''new_train_data.append(board_section)
                        if true_board[y, x] == -1:
                            new_train_keys.append(-1)
                        else:
                            new_train_keys.append(1)'''

                        board_section = vectorize(board_section).reshape(1, -1)
                        prediction = classifier.predict_proba(board_section)

                        predictions[y, x] = prediction[0][0]

                        #discounting
                        '''
                        discount = 0
                        for neighbor in minesweeper_emulator.get_neighbors(x, y):
                            (x1, y1) = neighbor
                            if game_board[y1, x1] == -2:
                                discount += .1
                        prediction[0, 0] = prediction[0][0] - discount
                        prediction[0, 1] = prediction[0][1] - discount
                        '''

                        if prediction[0][0] > max_certainty: #confident prediction of bomb
                            max_certainty = prediction[0][0]
                            best_square = (x, y)
                            guess = -1
                        if prediction[0][1] > max_certainty: #confident prediction of not bomb
                            max_certainty = prediction[0][1]
                            best_square = (x, y)
                            guess = 1

        print("Best guess: " + str(best_square))
        print("Certainty: " + str(max_certainty))
        if guess == 1:
            print("not bomb")
            x, y = best_square
            boom, game_board = minesweeper_emulator.guess_square(game_board, true_board, x, y)
            num_moves += 1
            if boom:
                print(game_board)
                print("You Lose. ")
                break
            else:
                print(game_board)
            stuck = False #we found a move during this loop
        elif guess == -1:
            print("bomb")
            x, y = best_square
            game_board = minesweeper_emulator.mark_bomb(game_board, x, y)
            num_moves += 1
            print(game_board)
            stuck = False #we found a move during this loop
        if stuck is True:
            print("Stuck! Aborting.") #sometimes, we get stuck.

    num_games += 1
    total_moves += num_moves

    #Generate data as we go
    #pickle.dump(new_train_data, open("../data/gameplay_data.pickle", "wb"))
    #pickle.dump(new_train_keys, open("../data/gameplay_keys.pickle", "wb"))
    #print("Total size of gampeplay training data: " + str(len(new_train_keys)))

average_num_moves = total_moves/num_games
print("Average number of moves: " + str(average_num_moves))