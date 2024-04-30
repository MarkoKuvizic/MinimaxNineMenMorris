
from board import Board
from utils import Utils
class moveHandler(object):
    def __init__(self, g = None):
        if g == None:
            self.board = Board()
        else:
            self.board = Board(g.moveManager.board.board)
        self.movesLen = [0, 0]
    def findMoves(self, player):
        moves = {}
        movesLen = 0
        for i, line in enumerate(self.board.board):
            for j, space in enumerate(line):
                if self.board.board[i][j] == player and self.board.board[i][j] != 0:
                    moves[(i, j)] = self.testMoves(i, j)
                    movesLen += len(moves[(i, j)])
        # print("TEST BOARD 2")
        # print(self.board.board)
        # print(moves)
        self.movesLen[player - 1] = movesLen
        return moves
    def testMoves(self, i, j):  
        possibleMoves = []
        if j % 2 == 1 and self.testSpace(i-1, j) and i!= 0:
            possibleMoves.append((i-1, j))
        if j % 2 == 1 and self.testSpace(i+1, j):
            possibleMoves.append((i+1, j))
        if self.testSpace(i, j-1):
            possibleMoves.append((i, Utils.negativeConversion(j-1, self.board.board[i])))
        if self.testSpace(i, j+1):
            possibleMoves.append((i, j+1))
        return possibleMoves
    def testSpace(self, i , j):
        try:
            if i < 0:
                raise Exception
            if self.board.board[i][j] == 0:
                return True
        except:
            return False
        return False