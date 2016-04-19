import numpy
import random

#0 thru 8 = number ofbombs adjacent to this square
#-2 = unclicked
#-9 = marked as bomb
#-1 = bomb

def is_in_range(x, y):
    if x < 0 or y < 0:
        return False
    if x >= width_master or y >= height_master:
        return False
    return True

def get_neighbors(x, y):
    neighbors = []
    if is_in_range(x-1, y-1):
        neighbors.append((x-1, y-1))
    if is_in_range(x-1, y):
        neighbors.append((x-1, y))
    if is_in_range(x-1, y+1):
        neighbors.append((x-1, y+1))
    if is_in_range(x, y+1):
        neighbors.append((x, y+1))
    if is_in_range(x+1, y+1):
        neighbors.append((x+1, y+1))
    if is_in_range(x+1, y):
        neighbors.append((x+1, y))
    if is_in_range(x+1, y-1):
        neighbors.append((x+1, y-1))
    if is_in_range(x, y-1):
        neighbors.append((x, y-1))
    return neighbors

def generate_true_board(height, width, x1, y1):
    global width_master
    width_master = width
    global height_master
    height_master = height
    board = numpy.zeros((height, width), dtype=numpy.int)
    number_of_bombs = 40 #random.randint(int(1 * height * width / 6), int(2 * height * width / 6)) #between 1/4 and 2/4 of the board is bombs
    for i in range(number_of_bombs):
        #place each bomb in a random location. If we place two in the same position, that's okay. Just reduces the total bombs by 1 which doesn't matter
        x_position = random.randint(0, width - 1)
        y_position = random.randint(0, height - 1)
        board[y_position, x_position] = -1

    #set first guess square to have no adjacent bombs
    if not is_in_range(x1, y1):
        print("Invalid coordinates")
        exit(1)
    board[y1, x1] = 0
    neighbors = get_neighbors(x1, y1)
    for x_y_pair in neighbors:
        x_n, y_n = x_y_pair
        board[y_n, x_n] = 0

    for y in range(height):
        for x in range(width):
            if board[y][x] == -1: #this square is a bomb.
                neighbors = get_neighbors(x, y)
                for x_y_pair in neighbors:
                    x_n, y_n = x_y_pair
                    if board[y_n][x_n] != -1: #if neighbor is not a bomb
                        board[y_n][x_n] += 1 #it should count this bomb as a neighbor
    return board

def generate_game_board(true_board, x, y):
    game_board = numpy.ones(true_board.shape, dtype=numpy.int)
    game_board = game_board * -2 # unclicked value
    game_board[y, x] = true_board[y][x]
    explore(true_board, game_board, x, y)
    return game_board

#expose adjacent squares until we have a perimiter of non-zero squares
def explore(true_board, game_board, x, y):
    visited = []
    visited.append((x, y))
    if true_board[y][x] == 0:
        neighbors = get_neighbors(x, y)
        for x_y_pair in neighbors:
            x_n, y_n = x_y_pair
            game_board[y_n][x_n] = true_board[y_n][x_n]
            if true_board[y_n][x_n] == 0:
                explore_recursive(true_board, game_board, x_n, y_n, visited)

def explore_recursive(true_board, game_board, x_n, y_n, visited):
    visited.append((x_n, y_n))
    if true_board[y_n][x_n] == 0:
        neighbors = get_neighbors(x_n, y_n)
        for x_y_pair in neighbors:
            x_n, y_n = x_y_pair
            game_board[y_n, x_n] = true_board[y_n][x_n]
            if true_board[y_n][x_n] == 0:
                if not (x_n, y_n) in visited:
                    explore_recursive(true_board, game_board, x_n, y_n, visited)

def mark_bomb(game_board, x, y):
    game_board[y][x] = -9 #marked as bomb value
    return game_board

def guess_square(game_board, true_board, x, y):
    if not is_in_range(x, y):
            print("Invalid coordinates")
            exit(1)
    game_board[y, x] = true_board[y][x] # update guessed square
    explore(true_board, game_board, x, y)
    if game_board[y][x] == -1:
        print("BOOM!")
        return True, game_board
    else:
        return False, game_board

def play_game():
    # first move
    game_board = numpy.ones((16, 16), dtype=numpy.int)
    game_board = game_board * -2 # unclicked value
    print_board(game_board)
    x = int(input("enter x coordinate "))
    y = int(input("enter y coordinate "))
    height, width = game_board.shape
    true_board = generate_true_board(height, width, x, y) # first guess is guaranteed to have no adjacent bombs
    print(true_board)
    game_board[y, x] = true_board[y][x] # update guessed square
    explore(true_board, game_board, x, y)

    # rest of the game
    while not numpy.array_equal(game_board, true_board):
        print_board(game_board)
        mark_or_guess = input("mark [m] or guess [g] ? ")
        x = int(input("enter x coordinate "))
        y = int(input("enter y coordinate "))
        if mark_or_guess == 'm':
            mark_bomb(game_board, x, y)
        elif mark_or_guess == 'g':
            boom = guess_square(game_board, true_board, x, y)
            if boom == True:
                break
        else:
            print("invalid input")
            exit(1)



def print_board(board):
    height, width = board.shape
    print("    ", end="")
    for i in range(width):
        if i < 10:
            print(str(i), end="  ")
        else:
            print(str(i), end=" ")
    print()
    for i in range(height):
        if i < 10:
            print(str(i), end=" ")
            print(board[i])
        else:
            print(str(i), end="")
            print(board[i])
    print("    ", end="")
    for i in range(width):
        if i < 10:
            print(str(i), end="  ")
        else:
            print(str(i), end=" ")
    print()

#play_game()
