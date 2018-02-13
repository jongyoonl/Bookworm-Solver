"""
The main methods for solving a Bookworm game board.
This module most importantly consists of implementing two functions:
createBoard() and searchBoard().
"""

from sys import stdin
from copy import deepcopy
from functools import reduce
import pickle, tree

treepath = "tree"

def main():
    """
    For every iteration, calls createBoard() to generate the board array,
    then calls searchBoard(). If a possible word is found, prints the
    longest string, its length, and the tiles that have been used.
    """
    treefile = open(treepath, "rb")
    wordtree = pickle.load(treefile)
    treefile.close()

    while True:

        board = createBoard()

        if isinstance(board, Exception):
            print("Error:" + str(board) + "\n")
            continue

        if not board:
            break

        maxlen, maxstr, tiles = searchBoard(board, wordtree)

        if maxlen:

            print(maxlen)
            print(maxstr)

            for column in tiles:
                print(column)

        else:
            print(None)

def createBoard():
    """Creates the board by reading inputs from the stdin. """
    print("Please type the letters of the board column by column separated by spaces:")

    board = []
    prevlen = 0

    for line in stdin:

        if line == "\n":
            return board

        char = line.lower().split()

        if prevlen != 0 and abs(len(char) - len(board[-1])) != 1:
            return ValueError("Column lengths mismatch.")
        else:
            prevlen = len(char)

        for index in range(len(char)):

            letter = char[index]

            if not letter.isalpha() or len(letter) != 1:
                return ValueError("Input is not a letter.")

            char[index] = letter.replace('q', 'qu')

        board.append(char)

    return board

def searchBoard(board, wordtree):
    """Searches the board for possible words by calling its helper function. """
    usedtiles = deepcopy(board)
    validindices = []

    for i in range(len(usedtiles)):
        for j in range(len(usedtiles[i])):
            usedtiles[i][j] = 1
            validindices.append((i,j))

    return reduce(reducer, 
        map(lambda currindex: searchBoardHelper(board, 
            wordtree, usedtiles, currindex, 0, ""), validindices))

def reducer(tuple0, tuple1):
    """Function for reducing. Chooses the tuple whose associated string is longer. """
    return tuple0 if tuple0[0] >= tuple1[0] else tuple1

def searchBoardHelper(board, prevtree, usedtiles, currindex, maxlen, maxstr):
    """
    Recursively searches the board. Looks at the immediately surrounding tiles
    afterwords to see if an even longer word is possible. 
    """
    i, j = currindex
    currchar = board[i][j]
    currtree = prevtree.getChildByChar(currchar)
    if currtree == None:
        raise ValueError("Child with the given letter does not exist.")
    char, string, parent, isword = currtree.getValues()
    childchars = currtree.getChildChars()

    currtiles = deepcopy(usedtiles)
    currtiles[i][j] = 0

    if isword and len(string) > maxlen:
        maxlen = len(string)
        maxstr = string

    newtiles = deepcopy(currtiles)

    for i, j in getSurroundingIndices(board, currindex):
        
        if currtiles[i][j] and (board[i][j] in childchars):

            sublen, substr, subtiles = searchBoardHelper(board, 
                currtree, currtiles, (i, j), maxlen, maxstr)

            if sublen > maxlen:
                maxlen = sublen
                maxstr = substr
                newtiles = subtiles

    return maxlen, maxstr, newtiles

def getSurroundingIndices(board, index):
    """Returns the array of indices of tiles that surround the given index. """
    indices = []
    i, j = index

    if i != 0:

        if len(board[i - 1]) < len(board[i]):
            indices.append((i - 1, j - 1))
            indices.append((i - 1, j))

        else:
            indices.append((i - 1, j))
            indices.append((i - 1, j + 1))

    if j != 0:
        indices.append((i, j - 1))
    if j != len(board[i]) - 1:
        indices.append((i, j + 1))

    if i != len(board) - 1:

        if len(board[i + 1]) < len(board[i]):
            indices.append((i + 1, j - 1))
            indices.append((i + 1, j))

        else:
            indices.append((i + 1, j))
            indices.append((i + 1, j + 1))

    def checkBounds(index):

        i, j = index

        if i < 0 or j < 0: return False

        try:
            board[i][j]
        except IndexError:
            return False
        return True

    return filter(checkBounds, indices)

if __name__ == "__main__":
    main()
