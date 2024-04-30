from re import M
from utils import Utils
class Board(object):
    def __init__(self, board = None):
        #board za testiranje: [[1,0,0,1,1,1,1,1],[0,1,2,0,2,2,0,0],[1,0,0,0,2,0,0,0]]
        self.possibleMorrises = [[[0, 0], [0, 1], [0, 2]], [[0, 2], [0, 3], [0, 4]], [[0, 4], [0, 5], [0, 6]], [[0, 6], [0, 7], [0, 0]],
                                    [[1, 0], [1, 1], [1, 2]], [[1, 2], [1, 3], [1, 4]], [[1, 4], [1, 5], [1, 6]], [[1, 6], [1, 7], [1, 0]],
                                    [[2, 0], [2, 1], [2, 2]], [[2, 2], [2, 3], [2, 4]], [[2, 4], [2, 5], [2, 6]], [[2, 6], [2, 7], [2, 0]],
                                    [[0, 1], [1, 1], [2, 1]], [[0, 3], [1, 3], [2, 3]], [[0, 5], [1, 5], [2, 5]], [[0, 7], [1, 7], [2, 7]]
                                    ]
        
        if board == None:
            self.board = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]] #0 - prazno, 1 - prvi igrac, 2 - drugi igrac
        else:
            self.board = board
            self.board = [row[:] for row in board]
            
    def morrisFinder(self, m):
        
        player = self.board[m[0]][m[1]]
        morrises = []
        threes = []
        doubles = []
       
        for morris in self.possibleMorrises:
            matchScore = 0
            if m in morris: 
                
                if self.board[morris[0][0]][morris[0][1]] == player:
                    
                    matchScore += 1
                    if [morris[0][0], morris[0][1]] != m:
                        doubles.append([[morris[0][0], morris[0][1]]] + [m])
                if self.board[morris[1][0]][morris[1][1]] == player:
                    matchScore += 1
                    if [morris[1][0], morris[1][1]] != m:
                        doubles.append([[morris[1][0], morris[1][1]]] + [m])
                if self.board[morris[2][0]][morris[2][1]] == player:
                    matchScore += 1
                    if [morris[2][0], morris[2][1]] != m:
                        doubles.append([[morris[2][0], morris[2][1]]] + [m])
            if matchScore == 3:
                morrises.append(morris)
        for double in doubles:
            threes += self.threePieceFinder(double, player, False)
        return morrises, threes, doubles
    def threePieceFinder(self, double, player, horizontal = True):    #trostruke konfiguracije koje nisu mice
        threes = []
        if horizontal:
            for coord in double:
                if self._checkSpace(coord[0] + 1, coord[1], player):
                    threes.append(double + [[coord[0] + 1, coord[1]]])
                if self._checkSpace(coord[0] - 1, coord[1], player):
                    threes.append(double + [[coord[0] - 1, coord[1]]])
        else:
            for coord in double:
                if self._checkSpace(coord[0], coord[1] + 1, player):
                    threes.append(double + [[coord[0], coord[1] + 1]])
                if self._checkSpace(coord[0], coord[1] - 1, player):
                    threes.append(double + [[coord[0], coord[1] - 1]])
        return threes
    def doubleFinder(self, movedPiece):
        
        x = movedPiece[0]
        y = movedPiece[1]
        player = self.board[x][y]
        return self._checkAllSpaces(x, y, player)
    def _checkSpace(self, x, y, player, mode="morrises"):
        if x == -1:
            return False
        try:
            if self.board[x][y] == player:
                return True
        except:
            if x==3:
                x = 0
            if self.board[x][0] == player and y == 8 and mode != "morrises":
                return True
        return False
    def _checkBlocked(self, x, y, player):
        blockSeverity = 0
        otherPlayer = Utils.otherPlayer(player)
        if x == -1 or x == 3:
            return blockSeverity
        if self.board[x][y] != otherPlayer:
            return blockSeverity
        
        if self._checkSpace(x, y+1, player, "doubles"):
            blockSeverity += 1
        if self._checkSpace(x, y-1, player, "doubles"):
            blockSeverity += 1
        if self._checkSpace(x-1, y, player, "doubles"):
            blockSeverity += 1
        if self._checkSpace(x+1, y, player, "doubles"):
            blockSeverity += 1
        return blockSeverity
    def _checkAllBlocks(self, x, y, player):
        fullBlocks = []
        tripleBlocks = []
        doubleBlocks = []

        a, b, c = self._blockConverter(self._checkBlocked(x, Utils.positiveConversion(y + 1, self.board[x]), player), x, Utils.positiveConversion(y + 1, self.board[x]))
        fullBlocks += a
        tripleBlocks += b
        doubleBlocks += c
        
        a, b, c = self._blockConverter(self._checkBlocked(x, y-1, player), x, Utils.negativeConversion(y - 1, self.board[x]))
        fullBlocks += a
        tripleBlocks += b
        doubleBlocks += c
        
        a, b, c = self._blockConverter(self._checkBlocked(x+1, y, player), x+1, y)
        fullBlocks += a
        tripleBlocks += b
        doubleBlocks += c
        
        a, b, c = self._blockConverter(self._checkBlocked(x-1, y, player), x-1, y)
        fullBlocks += a
        tripleBlocks += b
        doubleBlocks += c
        
        
        
        return fullBlocks, tripleBlocks, doubleBlocks
    def _blockConverter(self, a, x, y):     #funkcija nalazi na osnovu broja blockSeverity u koju grupu treba da ide block
        if a == 2:
            return [], [], [[x, y]]

        if a == 3:
            return [], [[x, y]], []
        if a == 4:
            return  [[x, y]], [], []
        return [], [], []
    def _checkAllSpaces(self, x, y, player):
        doubles = []
        if self._checkSpace(x, y+1, player, "doubles"):
            doubles.append([[x, y], [x, Utils.positiveConversion(y + 1, self.board[x])]])
        if self._checkSpace(x, y-1, player, "doubles"):
            doubles.append([[x, y], [x, Utils.negativeConversion(y - 1, self.board[x])]])
        if self._checkSpace(x-1, y, player, "doubles"):
            doubles.append([[x, y], [x - 1, y]])
        if self._checkSpace(x+1, y, player, "doubles"):
            doubles.append([[x, y], [x + 1, y]])
        return doubles
    def __str__(self):
        vs = "--------" #vertical spacer
        evs = "     " #empty vertical spacer
        vs2 = "-----"
        evs2 = "        "
        s = "   A" + evs + "B" + "  " + evs + "C" + "  " + evs2 + "D" + "  " + evs2 + "E" + evs + "  " + "F" + evs + "G" + "\n"
        s += "1  " + str(self.board[0][0]) + vs + vs + vs + str(self.board[0][1]) + vs + vs + vs + str(self.board[0][2]) + "\n"
        s += "   |" + evs2 + evs2 + evs2 + "|" + evs2 + evs2 + evs2 + "|" + "\n"
        s += "   |" + evs2 + evs2 + evs2 + "|" + evs2 + evs2 + evs2 + "|" + "\n"
        s += "2  |" + evs + str(self.board[1][0]) + vs + vs + "--" + str(self.board[1][1]) + vs + vs + "--" + str(self.board[1][2]) +  evs + "|" "\n"
        s += "   |" + evs + "|" + evs2 + evs2 + "  " + "|" + evs2 + evs2 + "  " + "|" + evs + "|" + "\n" + "   |" + evs + "|" + evs2 + evs2 + "  " + "|" + evs2 + evs2 + "  " + "|" + evs + "|" + "\n"
        s += "3  |" + evs + "|" + evs2 + str(self.board[2][0]) + vs + "-" +  str(self.board[2][1]) + vs + "-" + str(self.board[2][2]) + evs2 + "|" + evs + "|" + "\n"
        s += "   |" + evs + "|" + evs2 + "|" + evs2 + "  " + evs2 + " " + "|" + evs2 + "|" + evs + "|" + "\n" 
        s += "   |" + evs + "|" + evs2 + "|" + evs2 + "  " + evs2 + " " + "|" + evs2 + "|" + evs + "|" + "\n" 
        s += "4  " + str(self.board[0][7])  + vs2 + str(self.board[1][7]) + vs + str(self.board[2][7]) + evs2 + "  " + evs2 + " " + str(self.board[2][3]) + vs + str(self.board[1][3]) + vs2 + str(self.board[0][3]) + "\n" 
        s += "   |" + evs + "|" + evs2 + "|" + evs2 + "  " + evs2 + " " + "|" + evs2 + "|" + evs + "|" + "\n" 
        s += "   |" + evs + "|" + evs2 + "|" + evs2 + "  " + evs2 + " " + "|" + evs2 + "|" + evs + "|" + "\n" 
        s += "5  |" + evs + "|" + evs2 + str(self.board[2][6]) + vs + "-" +  str(self.board[2][5]) + vs + "-" + str(self.board[2][4]) + evs2 + "|" + evs + "|" + "\n"
        s += "   |" + evs + "|" + evs2 + evs2 + "  " + "|" + evs2 + evs2 + "  " + "|" + evs + "|" + "\n" + "   |" + evs + "|" + evs2 + evs2 + "  " + "|" + evs2 + evs2 + "  " + "|" + evs + "|" + "\n"
        s += "6  |" + evs + str(self.board[1][6]) + vs + vs + "--" + str(self.board[1][5]) + vs + vs + "--" + str(self.board[1][4]) +  evs + "|" "\n"
        s += "   |" + evs2 + evs2 + evs2 + "|" + evs2 + evs2 + evs2 + "|" + "\n"
        s += "   |" + evs2 + evs2 + evs2 + "|" + evs2 + evs2 + evs2 + "|" + "\n"
        s += "7  " + str(self.board[0][6]) + vs + vs + vs + str(self.board[0][5]) + vs + vs + vs + str(self.board[0][4]) + "\n"
        s += "   A" + evs + "B" + "  " + evs + "C" + "  " + evs2 + "D" + "  " + evs2 + "E" + evs + "  " + "F" + evs + "G" + "\n"

        return s