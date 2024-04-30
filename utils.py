

class Utils(object):
    co = {
        (0, 0) : ["A", 1],
        (0, 1) : ["D", 1],
        (0, 2) : ["G", 1],
        (0, 3) : ["G", 4],
        (0, 4) : ["G", 7],
        (0, 5) : ["D", 7],
        (0, 6) : ["A", 7],
        (0, 7) : ["A", 4],

        (1, 0) : ["B", 2],
        (1, 1) : ["D", 2],
        (1, 2) : ["F", 2],
        (1, 3) : ["F", 4],
        (1, 4) : ["F", 6],
        (1, 5) : ["D", 6],
        (1, 6) : ["B", 6],
        (1, 7) : ["B", 4],

        (2, 0) : ["C", 3],
        (2, 1) : ["D", 3],
        (2, 2) : ["E", 3],
        (2, 3) : ["E", 4],
        (2, 4) : ["E", 5],
        (2, 5) : ["D", 5],
        (2, 6) : ["C", 5],
        (2, 7) : ["C", 4],
    }    
    @staticmethod
    def negativeConversion(i, board):
        if i < 0:
            return len(board) - 1
        return i
    @staticmethod
    def coords(c):
        return Utils.co[tuple(c)]
    @staticmethod
    def positiveConversion(i, board):
        if i == len(board):
            return 0
        return i
    
    def generateBoard(board, move, player):
        board[move[0][0]][move[0][1]] = 0
        board[move[1][0]][move[1][1]] = player
    @staticmethod
    def otherPlayer(i):
        if (i == 1):
            return 2
        return 1
    