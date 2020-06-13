"""
Tic Tac Toe Player
"""

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

#Self-written method.
def player(board):
    """
    Returns player who has the next turn on a board.
    """

    #If there are an odd # of empty spaces, it will be X's turn and if there is even # of spaces, it will be O's turn.
    moves = sum(row.count(EMPTY) for row in board)
    if moves % 2 == 0:
        return O
    else:
        return X


#Self-written method.
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    #Makes a set of all available spaces
    validSpaces = set()

    #Will add the coordinate to the list if it is empty
    for i in range(3):
        for j in range (3):
            if board[i][j] == EMPTY:
                validSpaces.add((i, j))

    return validSpaces

#Self-written method.
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    #The coordinate of the action will be saved into their x/y variables and a copy of the board will be made.
    row, col = action

    #An empty board is made before
    newBoard = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
    for i in range(3):
        for j in range(3):
            newBoard[i][j] = board[i][j]

    #The action spot will be attempted to be filled with whose ever turn it is but will raise an exception if its invalid.
    try:
        newBoard[row][col] = player(board)
    except:
        raise Exception("This is an invalid move")

    return newBoard

#Self-written method.
def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    #Check rows for a winner.
    for i in range(3):
        if board[i][0] == X and board[i][1] == X and board[i][2] == X:
            return X
        elif board[i][0] == O and board[i][1] == O and board[i][2] == O:
            return O

    #Checks columns for a winner.
    for i in range(3):
        if board[0][i] == X and board[1][i] == X and board[2][i] == X:
            return X
        elif board[0][i] == O and board[1][i] == O and board[2][i] == O:
            return O

    #Checks diagonals for a winner.
    if (board[0][0] == X and board[1][1] == X and board[2][2] == X) or (board[2][0] == X and board[1][1] == X and board[0][2] == X):
        return X
    elif (board[0][0] == O and board[1][1] == O and board[2][2] == O) or (board[2][0] == O and board[1][1] == O and board[0][2] == O):
        return O

    return None


#Self-written method.
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    #Returns true if X or O won from previous method or if there is no space left
    winnerOfGame = winner(board)
    if winnerOfGame != None or sum(row.count(EMPTY) for row in board) == 0:
        return True

    return False


#Self-written method.
def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    #Gets the winner.
    winnerOfGame = winner(board)

    #Returns the corresponding value of whoever wins.
    if winnerOfGame == X:
        return 1
    elif winnerOfGame == O:
        return -1
    return 0


#Self-written method.
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    #No minimaxing is needed if the board is in a terminal state.
    if terminal(board):
        return None

    #A dictionary is made to store an action with a certain value.
    actionValues = {}
    values = []
    value = 0

    #If it is X's turn, all actions will have it's value evaluated.
    if player(board) == X:
        for action in actions(board):
            value = minimum(result(board, action))

            #If the best case scenario will come at worst, it will jump straight to this one immediately.
            if value == 1:
                return action

            #Only adds an action if its value is already not in the dictionary.
            if value not in actionValues:
                actionValues[value] = action

        #The best case scenario is evaluated and will be returned
        for key in actionValues:
            values.append(key)
        value = max(values)
        return actionValues[value]

    #Similar code for O will be run but instead, it is looking for the smallest option.
    if player(board) == O:
        for action in actions(board):
            value = maximum(result(board, action))

            if value == -1:
                return action

            if value not in actionValues:
                actionValues[value] = action

        for key in actionValues:
            values.append(key)

        value = min(values)
        return actionValues[value]

#Helper method to determine the maximum value obtainable- the code comes from Week0 lesson
def maximum(board):
    if terminal(board):
        return utility(board)

    v = -100000000
    for action in actions(board):
        v = max(v, minimum(result(board, action)))

    return v

#Helper method to determine the minimum value obtainable- the code comes from Week0 lesson
def minimum(board):
    if terminal(board):
        return utility(board)

    v = 10000000
    for action in actions(board):
        v = min(v, maximum(result(board, action)))

    return v