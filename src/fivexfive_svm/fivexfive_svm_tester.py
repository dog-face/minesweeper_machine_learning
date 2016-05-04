from src.emulator import minesweeper_emulator
import numpy
import pickle

epochs = 0

total_moves = 0
num_games = 0

while epochs < 100:
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
            #print(board_section)
            return True
    #print(get_5x5_section(game_board, 1, 1))

    classifier = pickle.load(open("../data/5x5_trained_svm_classifier.pickle", "rb"))
    #classifier = pickle.load(open("../data/5x5_new_classifier.pickle", "rb"))

    #new_train_data = pickle.load(open("../data/new_data.pickle", "rb"))
    #new_train_keys = pickle.load(open("../data/new_keys.pickle", "rb"))


    stuck = False
    threshold = .8

    num_moves = 0
    while -2 in game_board:
        max_certainty = 0
        best_square = (1, 1)
        guess = 0
        '''if stuck: # if we didn't find any moves during last loop
            threshold = 3 * threshold / 4 #take more risks
        if not stuck: # if we did find a move last loop: reset stuck to true.
            stuck = True
            threshold = .8  #reset certainty threshold'''
        predictions = numpy.zeros((16, 16))
        for x in range(0, board_width):
            for y in range(0, board_height):
                if game_board[y][x] == -2: #if this square is still unclicked
                    board_section = get_5x5_section(game_board, x, y)
                    if reasonable_guess(board_section):
                        '''new_train_data.append(board_section)
                        if true_board[y, x] == -1:
                            new_train_keys.append(-1)
                        else:
                            new_train_keys.append(1)'''

                        #print(vectorize(board_section))
                        board_section = vectorize(board_section).reshape(1, -1)
                        prediction = classifier.predict_proba(board_section)

                        predictions[y, x] = prediction[0][0]

                        '''discount = 0
                        for neighbor in minesweeper_emulator.get_neighbors(x, y):
                            (x1, y1) = neighbor
                            if game_board[y1, x1] == -2:
                                discount += .1
                        #print("before: " + str(prediction[0][0]))
                        prediction[0, 0] = prediction[0][0] - discount
                        prediction[0, 1] = prediction[0][1] - discount
                        #print("after: " + str(prediction[0][0]))
'''

                        #print(prediction)
                        if(prediction[0][0] > max_certainty): #confident prediction of bomb
                            max_certainty = prediction[0][0]
                            best_square = (x, y)
                            guess = -1
                        '''if prediction[0][1] > threshold: #confident prediction of bomb
                            game_board = minesweeper_emulator.mark_bomb(game_board, x, y)
                            print(game_board)
                            stuck = False #we found a move during this loop'''
                        if(prediction[0][1] > max_certainty): #confident prediction of not bomb
                            max_certainty = prediction[0][1]
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
        #print(predictions)
        print(best_square)
        print(max_certainty)
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


    num_games += 1
    total_moves += num_moves
    #pickle.dump(new_train_data, open("../data/new_data.pickle", "wb"))
    #pickle.dump(new_train_keys, open("../data/new_keys.pickle", "wb"))

average_num_moves = total_moves/num_games
print("Average number of moves: " + str(average_num_moves))