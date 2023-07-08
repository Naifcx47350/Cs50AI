"""
Tic Tac Toe Player
"""

from copy import deepcopy
import math

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


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    xcount = 0
    ocount = 0

    for i in range(3):  # count number of X's and O's on board
        for j in range(3):
            if (board[i][j] == X):
                xcount = xcount + 1
            elif (board[i][j] == O):
                ocount = ocount + 1

    if (board == initial_state()):  # when board is empty, X goes first
        return X

    elif (xcount > ocount):  # if X has more cells then O is next
        return O

    elif (xcount == ocount):  # because X goes first, if X and O have same number of cells, X is next
        return X
    else:
        raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    pActions = {}  # a set that will contain all possible actions

    for i in range(3):  # count number of empty cells on board and add them to pActions(possible actions) as a tuple
        for j in range(3):
            if (board[i][j] == EMPTY):
                pActions.add((i, j))

    return pActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if (action not in actions(board)):  # if action is not in possible actions, raise exception
        raise Exception("Invalid action")
    else:
        # deepcopy board so that original board is not changed
        boardDC = deepcopy(board)
        # change the cell at action to the player who made the move(X,O)
        boardDC[action[0]][action[1]] = player(board)

    return boardDC


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # chekiang for horizontal wins
    for i in range(3):  # i = rows
        if (board[i][0] == board[i][1] == board[i][2] != EMPTY):
            if (board[i][0] == X):
                return X
            else:
                return O

    # checking for vertical wins
    for j in range(3):  # j = columns
        if (board[0][j] == board[1][j] == board[2][j] != EMPTY):
            if (board[0][j] == X):
                return X
            else:
                return O

    # checking for diagonal wins
    for i in range(3):  # i = rows
        for j in range(3):  # j = columns
            if (i == j == 0):  # when we start at row 0 and column 0
                # (check for 0.0 == 1.1 == 2.2)
                if (board[i][j] == board[i+1][j+1] == board[i+2][j+2] != EMPTY):
                    if (board[i][j] == X):
                        return X
                    else:
                        return O
            elif (i == j == 2):
                if (board[i][j] == board[i-1][j-1] == board[i-2][j-2] != EMPTY):
                    if (board[i][j] == X):
                        return X
                    else:
                        return O

    return None  # if no winner, return none


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if (winner(board) == X or winner(board) == O):  # if there is a winner, game is over
        return True

    elif (len(actions(board)) == 0):  # if there are no more possible actions, game is over
        return True

    else:
        return False  # if there is no winner, game is not over


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if (winner(board) == X):
        return 1

    elif (winner(board) == O):
        return -1

    elif (terminal(board) == True):
        return 0

    else:
        raise NotImplementedError


# an additional function to help the minimax function {min_value, max_value}
def min_value(board):

    if (terminal(board) == True):  # if the game is over, return the utility of the board
        return utility(board)

    # we declare this variable with infinity so that the AI using the Minimax algorithm can find the minimum value compared to infinity
    v = float('inf')

    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v


def max_value(board):

    if (terminal(board) == True):  # if the game is over, return the utility of the board
        return utility(board)

    # we declare this variable with infinity so that the AI using the Minimax algorithm can find the minimum value compared to infinity
    v = float('-inf')

    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if (terminal(board) == True):
        return utility(board)

    # we declare this variable with infinity so that the AI using the Minimax algorithm can find the minimum value compared to infinity
    minV = float('inf')
    bestMove = {0, 0}

    for i in range(3):
        for j in range(3):
            if (board[i][j] == EMPTY):  # chekiang for possible actions on board
                # we set the cell to the player who made the move(X,O)
                board[i][j] = player(board)
                # we call the min_value function to find the minimum value
                v = min_value(board[i][j])
                # we reset the cell to empty so that we can check for other possible actions
                board[i][j] = EMPTY
                if (v < minV):  # if the value is less than the minimum value, we set the minimum value to v
                    minV = v
                    # we set the best move to the cell that has the minimum value
                    bestMove = {i, j}

    return bestMove
