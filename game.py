

from pprint import pprint
from moveHandler import moveHandler
from minimax.heuristics import Heuristics
from minimax.minimax import Minimax
from utils import Utils
import random
import time

class Game(object):
    
    def __init__(self, game=None, a=None, b=None, player=None, removal = None):
        self.currentMorrises = [[], []]
        self.newlyClosedMorrises = []
        self.rPiece = -1
        self.mode = 0
        self.placed = []
        self.numPieces = [0, 0]

        if game != None:
            g = game
            self.move = [a, b]
            self.moveManager = moveHandler(g)
            self.free = [row[:] for row in g.free]
            self.currentMorrises = [row[:] for row in g.currentMorrises]
            self.heuristics = Heuristics(self) 
            self.player = g.player
            self.doublesDetected = g.doublesDetected
            self.morrisesDetected = g.morrisesDetected
            self.threesDetected = g.threesDetected  #non morris threes
            self.trakalice = g.trakalice   #dvojke koje se nalaze na jedno polje od dvojki su prilike za "mice trakalice", gde se jednim potezom otvara jedna mica i zatvara druga
            self.blockedPieces = g.blockedPieces   #protivnicke figure koje su u potpunosti okruzene nasim figurama
            self.semiBlockedPieces = g.semiBlockedPieces  #protivnicke figure koje samo sa jedne strane nisu okruzene nasim figurama
            self.twiceBlockedPieces = g.twiceBlockedPieces   #protivnicke figure koje sa 2 strane nisu okruzene nasim figurama
            self.numPieces[0] = g.numPieces[0]
            self.numPieces[1] = g.numPieces[1]
            self.phase = g.phase
            self.winningPlayer = g.winningPlayer
            self.heuristicValue = g.heuristicValue
            self.nodeValue = g.nodeValue

            if a!= None and a != []:
                self.deleter(a)
                if removal != None:
                    self.moveManager.board.board[removal[0]][removal[1]] = 0

                    self.numPieces[Utils.otherPlayer(player)-1] -= 1
                    if self.numPieces[Utils.otherPlayer(player)-1] < 3:
                        self.winningPlayer = player
                else:
                    self.rPiece = 0
                    self.doMove(a, b, player)
                    self.moveManager.board.board[a[0]][a[1]] = 0
                    self.moveManager.board.board[b[0]][b[1]] = player
                    
            
                self.heuristicValue = self.heuristics.testHeuristics()
                self.player = Utils.otherPlayer(self.player)

            else:
                
                self.placePiece(self.free, b)  
                self.heuristicValue = self.heuristics.testHeuristics()
  
            # morrises, threes, doubles = self.moveManager.board.morrisFinder(b)

            # self.doublesDetected[self.player-1] += doubles
            # self.morrisesDetected[self.player-1] += morrises
            # self.threesDetected[self.player-1] += threes

            # self.trakaliceFinder()
                
            # a, b, c = self.moveManager.board._checkAllBlocks(b[0],b[1], self.player)

            # self.blockedPieces[self.player-1] += a
            # self.semiBlockedPieces[self.player-1] += b
            # self.twiceBlockedPieces[self.player-1] += c

            
        else :
            x = self.menu()
            if x == 1:
                self.minimax = None
            elif x == 2:
                self.minimax = Minimax()
            else:
                self.minimax1 = Minimax()
                self.minimax2 = Minimax()
            self.moveManager = moveHandler()
            
            self.heuristics = Heuristics(self)  #zameni ovo celim minimax algoritmom kad bude gotov
            self.player = 1
            self.doublesDetected = [[], []]
            self.morrisesDetected = [[], []]
            self.threesDetected = [[], []]  #non morris threes
            self.trakalice = [[], []]   #dvojke koje se nalaze na jedno polje od dvojki su prilike za "mice trakalice", gde se jednim potezom otvara jedna mica i zatvara druga
            self.blockedPieces = [[], []]   #protivnicke figure koje su u potpunosti okruzene nasim figurama
            self.semiBlockedPieces = [[], []]   #protivnicke figure koje samo sa jedne strane nisu okruzene nasim figurama
            self.twiceBlockedPieces = [[], []]   #protivnicke figure koje sa 2 strane nisu okruzene nasim figurama
            self.numPieces = [0, 0]
            self.phase = 1
            self.winningPlayer = 0
            self.heuristicValue = 0
            self.nodeValue = 0
            self.free = self.possiblePlacements()
            self.moveManager.board.board = self.phase1()
            if self.mode == 2:
                self.minimax = Minimax()
                while True:
                    if self.playerFirst:
                        print("IGRAC JE 1, AI JE 2")
                        self.player = 1
                        self.makeMove()
                        self.player = 2
                        tmp = [row[:] for row in self.moveManager.board.board]                    
                        m, mo, mm, r = self.minimax.minimax(self, self.player)
                        random.seed(time.time())
                        mo = random.choice(self.minimax.moves)
                        print("MOVE", mo)
                        re = self.minimax.removal
                        self.moveManager.board.board = tmp
                        self.doMove(mo[0][0], mo[0][1])
                        if mo[1]:
                            print("REMOVED", Utils.coords(re))
                            
                            self.moveManager.board.board[re[0]][re[1]] = 0
                            self.numPieces[Utils.otherPlayer(self.player)-1] -= 1
                            if self.numPieces[Utils.otherPlayer(self.player)-1] < 3:
                                print("POBEDIO JE IGRAC BROJ ", self.player)
                                print(self.moveManager.board)
                                self.winningPlayer = self.player
                                exit()
                    else:
                        print("AI JE 1, IGRAC JE 2")
                        self.player = 1
                        tmp = [row[:] for row in self.moveManager.board.board]                    
                        m, mo, mm, r = self.minimax.minimax(self, self.player)
                        random.seed(time.time())
                        mo = random.choice(self.minimax.moves)
                        print("MOVE", mo)
                        re = self.minimax.removal
                        self.moveManager.board.board = tmp
                        self.doMove(mo[0][0], mo[0][1])
                        if mo[1]:
                            print("REMOVED", Utils.coords(re))
                            
                            self.moveManager.board.board[re[0]][re[1]] = 0
                            self.numPieces[Utils.otherPlayer(self.player)-1] -= 1
                            if self.numPieces[Utils.otherPlayer(self.player)-1] < 3:
                                print("POBEDIO JE IGRAC BROJ ", self.player)
                                print(self.moveManager.board)
                                self.winningPlayer = self.player
                                exit()
                        self.player = 2
                        self.makeMove()
                        print(self.moveManager.board)

                    
            elif self.mode == 1:
                while True:
                    self.makeMove()
                    self.makeMove()
            else:
                while True:
                    self.player = 1
                    m, mo, mm, r = self.minimax1.minimax(self, self.player)
                    random.seed(time.time())
                    mo = random.choice(self.minimax1.moves)
                    print("MOVE", mo)
                    re = self.minimax1.removal
                    self.doMove(mo[0][0], mo[0][1])
                    if mo[1]:
                        print("REMOVED", Utils.coords(re))
                        
                        self.moveManager.board.board[re[0]][re[1]] = 0
                        self.numPieces[Utils.otherPlayer(self.player)-1] -= 1
                        if self.numPieces[Utils.otherPlayer(self.player)-1] < 3:
                            print("POBEDIO JE IGRAC BROJ ", self.player)
                            print(self.moveManager.board)
                            self.winningPlayer = self.player
                            exit()
                    print(self.moveManager.board)
                    input("ENTER ZA SLEDECI POTEZ")
                    self.player = 2
                    m, mo, mm, r = self.minimax2.minimax(self, self.player)
                    random.seed(time.time())
                    mo = random.choice(self.minimax2.moves)
                    print("MOVE", mo)
                    re = self.minimax2.removal
                    self.doMove(mo[0][0], mo[0][1])
                    if mo[1]:
                        print("REMOVED", Utils.coords(re))
                        
                        self.moveManager.board.board[re[0]][re[1]] = 0
                        self.numPieces[Utils.otherPlayer(self.player)-1] -= 1
                        if self.numPieces[Utils.otherPlayer(self.player)-1] < 3:
                            print("POBEDIO JE IGRAC BROJ ", self.player)
                            print(self.moveManager.board)
                            self.winningPlayer = self.player
                            exit()
                    
                    print(self.moveManager.board)
                    input("ENTER ZA SLEDECI POTEZ")
    def possibleRemovals2(self, player):
        if len(self.currentMorrises[player-1])==0:
            return []
        pieces = []
        player = Utils.otherPlayer(player)
        for i, row in enumerate(self.moveManager.board.board):
            for j, piece in enumerate(self.moveManager.board.board[i]):
                if piece == player:
                    found = False
                    for morris in self.moveManager.board.possibleMorrises:
                        if [i, j] in morris and self.moveManager.board.board[morris[0][0]][morris[0][1]] == player and self.moveManager.board.board[morris[1][0]][morris[1][1]] == player and self.moveManager.board.board[morris[2][0]][morris[2][1]] == player:
                            found = True
                    if not found:
                        pieces.append([i, j])
        if pieces == []:
            for i, row in enumerate(self.moveManager.board.board):
                for j, piece in enumerate(self.moveManager.board.board[i]):
                    if piece == player:
                        pieces.append([i, j])
        return pieces   
    def possibleRemovals(self, player):
        if len(self.currentMorrises[self.player - 1])==0:
            return []
        player = Utils.otherPlayer(player)
        pieces = []
        for i, row in enumerate(self.moveManager.board.board):
            for j, piece in enumerate(self.moveManager.board.board[i]):
                if piece == player:
                    found = False
                    for morris in self.moveManager.board.possibleMorrises:
                        if [i, j] in morris and self.moveManager.board.board[morris[0][0]][morris[0][1]] == player and self.moveManager.board.board[morris[1][0]][morris[1][1]] == player and self.moveManager.board.board[morris[2][0]][morris[2][1]] == player:
                            found = True
                    if not found:
                        pieces.append([i, j])
        if pieces == []:
            for i, row in enumerate(self.moveManager.board.board):
                for j, piece in enumerate(self.moveManager.board.board[i]):
                    if piece == player:
                        pieces.append([i, j])
        return pieces   
    def menu(self):
        print("------------MICE------------")
        print("\n")
        print("1)   Igrac vs Igrac")
        print("2)   Igrac vs AI")
        print("3)   AI vs AI")
        i = 0
        i = self.takeX([0,0,0])
        self.mode = i + 1
        return i
    def first(self):
        print("------------Ko igra prvi?------------")
        print("\n")
        print("1)   Igrac")
        print("2)   AI")
        i = 0
        while i < 1 or i > 2:
            i = eval(input(">"))
        return i
    def winningTest(self, player):
        if self.winningPlayer == 0:
            return 0
        if self.winningPlayer == player:
            return -1
        return 1
    def deleter(self, position):  #funkcija koja proverava da li je neka formacija rasturena potezom i brise je iz liste ako jeste
        self.currentMorrises = [[], []]
        for i, double in enumerate(self.doublesDetected[self.player-1]):
            if position in double:
                del self.doublesDetected[self.player-1][i]
                for j, three in enumerate(self.threesDetected[self.player-1]):
                    if position in three:
                        del self.threesDetected[self.player-1][j]
                for k, morris in enumerate(self.morrisesDetected[self.player-1]):
                    if position in morris:
                        del self.morrisesDetected[self.player-1][k]
                        if morris in self.trakalice:
                            self.trakalice.remove(morris)
                        #za sad ne brisemo trakalicu ako je njen morris ostao netaknut, a double nije, procenjujem da je ovakva "poluraskvarena" trakalica i dalje vrednija 
                        #od obicnog morrisa
                        
        self.blockedDeleter(position)
        if position in self.blockedPieces[self.player-1]:
            self.blockedPieces[self.player-1].remove(position)
        if position in self.twiceBlockedPieces[self.player-1]:
            self.twiceBlockedPieces[self.player-1].remove(position)
        if position in self.semiBlockedPieces[self.player-1]:
            self.semiBlockedPieces[self.player-1].remove(position)
    def blockedDeleter(self, position):
        x = position[0]
        y = position[1]
        self._blockedDeleter(x + 1, y)
        self._blockedDeleter(x - 1, y)
        self._blockedDeleter(x, Utils.negativeConversion(y - 1, self.moveManager.board.board[x]))
        self._blockedDeleter(x, Utils.positiveConversion(y + 1, self.moveManager.board.board[x]))
        
    def _blockedDeleter(self, x, y):
        if [x, y] in self.blockedPieces[self.player-1]:
            self.blockedPieces[self.player-1].remove([x, y])
        if [x, y] in self.twiceBlockedPieces[self.player-1]:
            self.twiceBlockedPieces[self.player-1].remove([x, y])
        if [x, y] in self.semiBlockedPieces[self.player-1]:
            self.semiBlockedPieces[self.player-1].remove([x, y])
    def trakaliceFinder(self):
        trakaliceTMP = []
        for morris in self.morrisesDetected[self.player - 1]:
            matches = 0
            for i in range(0, 3):
                try:
                    if self.moveManager.board.board[morris[i][0]+1][morris[i][1]] == self.player and [morris[i][0]+1, morris[i][1]] not in morris:
                        matches += 1
                except: 
                    pass
                try: 
                    if self.moveManager.board.board[morris[i][0]-1][morris[i][1]] == self.player and [morris[i][0]-1, morris[i][1]] not in morris:
                        matches += 1
                except:
                    pass
                if self.moveManager.board.board[morris[i][0]][Utils.positiveConversion(morris[i][1]+1, self.moveManager.board.board[0])] and [morris[i][0], Utils.positiveConversion(morris[i][1]+1, self.moveManager.board.board[0])] not in morris:
                    matches += 1
                if self.moveManager.board.board[morris[i][0]][morris[i][1] - 1] and [morris[i][0], morris[i][1] - 1] not in morris:
                    matches += 1
            if matches == 2:
                trakaliceTMP.append(morris)
        
        self.trakalice[self.player-1] += trakaliceTMP
    
    def reset(self):
        # self.doublesDetected = 0
        # self.morrisesDetected = 0
        # self.threesDetected = 0
        pass
    def phase1(self):
        free = self.possiblePlacements()
        if self.mode == 2:
            self.minimax = Minimax()
            print("KO IGRA PRVI?    1) IGRAC    2) AI")
            playerOrAI = [True, False]
            self.playerFirst = playerOrAI[self.takeX(playerOrAI)]
            for i in range(0,9):
                if self.playerFirst:
                    print("IGRAC JE 1, AI JE 2")
                    free = self.placePiece(free)
                    m, mo, self.moveManager = self.minimax.minimaxP1(self, self.player)
                    random.seed(time.time())
                    mo = random.choice(self.minimax.moves)
                    print(mo, "MOVES I COULD MAKE")
                    free = self.placePiece(free, mo[0])
                    re = self.minimax.removal
                    if mo[1]:
                        print("REMOVED", Utils.coords(re))
                        self.moveManager.board.board[re[0]][re[1]] = 0
                        self.numPieces[Utils.otherPlayer(self.player)-1] -= 1
                        free.append(re)
                        self.free.append(re)
                else:
                    print("AI JE 1, IGRAC JE 2")

                    m, mo, self.moveManager = self.minimax.minimaxP1(self, self.player)
                    random.seed(time.time())
                    mo = random.choice(self.minimax.moves)
                    print(mo, "MOVES I COULD MAKE")
                    free = self.placePiece(free, mo[0])
                    re = self.minimax.removal
                    if mo[1]:
                        print("REMOVED", Utils.coords(re))
                        self.moveManager.board.board[re[0]][re[1]] = 0
                        self.numPieces[Utils.otherPlayer(self.player)-1] -= 1
                        free.append(re)
                        self.free.append(re)
                    free = self.placePiece(free)
                    print(self.moveManager.board)

            self.phase = 2
        elif self.mode == 1:
            for i in range(0, 9):
                free = self.placePiece(free)
                free = self.placePiece(free)
            self.phase = 2
        else:
            self.minimax1 = Minimax()
            self.minimax2 = Minimax()
            for i in range(0, 9):
                m, mo, self.moveManager = self.minimax1.minimaxP1(self, self.player)
                random.seed(time.time())
                mo = random.choice(self.minimax1.moves)
                print(mo, "MOVES I COULD MAKE")
                free = self.placePiece(free, mo[0])
                re = self.minimax1.removal
                if mo[1]:
                    print("REMOVED", Utils.coords(re))
                    self.moveManager.board.board[re[0]][re[1]] = 0
                    self.numPieces[Utils.otherPlayer(self.player)-1] -= 1
                    free.append(re)
                    self.free.append(re)
                print(self.moveManager.board)
                input("ENTER ZA SLEDECI POTEZ...")
                m, mo, self.moveManager = self.minimax2.minimaxP1(self, self.player)
                random.seed(time.time())
                mo = random.choice(self.minimax2.moves)
                print(mo, "MOVES I COULD MAKE")
                free = self.placePiece(free, mo[0])
                re = self.minimax2.removal
                if mo[1]:
                    print("REMOVED", Utils.coords(re))
                    self.moveManager.board.board[re[0]][re[1]] = 0
                    self.numPieces[Utils.otherPlayer(self.player)-1] -= 1
                    free.append(re)
                    self.free.append(re)
                print(self.moveManager.board)
                input("ENTER ZA SLEDECI POTEZ...")
            self.phase = 2
            
            
        return self.moveManager.board.board
    def placePiece(self, free = None, move = None):
        if free == None:
            free = self.possiblePlacements()
        #self.reset()
        if move == None:
            print(self.moveManager.board)
            for i, placement in enumerate(free):
                print(i+1, " " ,Utils.coords(placement))
            x = self.takeX(free)
            self.moveManager.board.board[free[x][0]][free[x][1]] = self.player
            f = free[x]
            del free[x]
            try: 
                self.free.remove(f)
            except:
                pass
        else:
            self.moveManager.board.board[move[0]][move[1]] = self.player
            try:
                self.free.remove(move)
                free.remove(move)
            except:
                pass
            f = move
        morrises , triples, doubles  = self.moveManager.board.morrisFinder(f)
        self.placed = move
        self.currentMorrises[self.player - 1] = morrises
        self.doublesDetected[self.player-1] += doubles
        self.morrisesDetected[self.player-1] += morrises
        self.threesDetected[self.player-1] += triples
        self.trakaliceFinder()
        if len(morrises) != 0 and move == None:
            free = self.removePiece(free)
        a, b, c = self.moveManager.board._checkAllBlocks(f[0], f[1], self.player)

        self.blockedPieces[self.player-1] += a
        self.semiBlockedPieces[self.player-1] += b
        self.twiceBlockedPieces[self.player-1] += c
        self.heuristicValue = self.heuristics.testHeuristics()
        self.numPieces[self.player - 1] += 1
        
        

        self.player = Utils.otherPlayer(self.player)
            
        
        return free
    def possiblePlacements(self):
        ret = []
        for i, line in enumerate(self.moveManager.board.board):
            for j, space in enumerate(line):
                if space == 0:
                    ret.append([i, j])
        return ret
    def possibleMoves(self, player = None):
        if player == None:
            player = self.player
        return self.moveManager.findMoves(player)
    def makeMove(self):
        #self.reset()
        print(self.moveManager.board)
        possibleMoves = self.moveManager.findMoves(self.player)
        keys = list(possibleMoves)
        pprint(keys)
        print("Figure koje mozete da pomerite su: ")
        for i, piece in enumerate(keys):
            print(i+1," ", Utils.coords(piece))
        x = Game.takeX(keys)
        print(possibleMoves[keys[x]])
        while possibleMoves[keys[x]] == []:
            print("ta figura je potpuno blokirana, probajte ponovo...")
            x = Game.takeX(keys)
        for i, move in enumerate(possibleMoves[keys[x]]):
            print(i+1," ", Utils.coords(move))
        y = Game.takeX(possibleMoves[keys[x]])
        morrises = self.doMove(keys[x], possibleMoves[keys[x]][y])
        pprint(self.moveManager.board.board)
        
        

        if morrises != []:
            self.removePiece()
        print(self.moveManager.board.board)
        self.player = Utils.otherPlayer(self.player)
    def removePiece(self, free = [], redo = False):
        print("Napravili ste micu, mozete ukloniti jednu protivnicku figuru...")    
        oppositePlayer = Utils.otherPlayer(self.player)
        oppositePieces = []
        for i, line in enumerate(self.moveManager.board.board):
            for j, space in enumerate(line):
                if self.moveManager.board.board[i][j] == oppositePlayer:
                    
                    found = False
                    for morris in self.morrisesDetected[Utils.otherPlayer(oppositePlayer)-1]:
                        if (not redo) and ([i, j] in morris):
                            found = True
                            break
                    if found:
                        break
                    oppositePieces.append([i, j])
        if oppositePieces == []:
            self.removePiece(free, True)
        for i, piece in enumerate(oppositePieces):
            print(i + 1, " ", piece)
        print(" Koju od ponudjenih protivnickih figura zelite ukloniti? ")
        x = Game.takeX(oppositePieces)
        print(oppositePieces[x])
        self.moveManager.board.board[oppositePieces[x][0]][oppositePieces[x][1]] = 0
        if free != []:
            free.append(oppositePieces[x])
        if self.phase == 2 and len(oppositePieces) < 3:
            print("POBEDIO JE IGRAC BROJ ", self.player)
            print(self.moveManager.board)
            self.winningPlayer = self.player
            exit()
        self.numPieces[self.player - 1] -= 1
        if free != []:
            return free
        return
        
    def doMove(self, a, b, player = None):
        if player == None:
            player = self.player
        self.move = [a, b]
        self.moveManager.board.board[a[0]][a[1]] = 0
        self.moveManager.board.board[b[0]][b[1]] = player

        self.deleter(a)
        morrises, threes, doubles = self.moveManager.board.morrisFinder(list(b))
        self.currentMorrises[self.player - 1] = morrises
        self.doublesDetected[self.player-1] += doubles
        self.morrisesDetected[self.player-1] += morrises
        self.threesDetected[self.player-1] += threes

        self.trakaliceFinder()
        aT, bT, cT = self.moveManager.board._checkAllBlocks(b[0], b[1], self.player)

        self.blockedPieces[self.player-1] += aT
        self.semiBlockedPieces[self.player-1] += bT
        self.twiceBlockedPieces[self.player-1] += cT
        return morrises

    @classmethod
    def takeX(cls, l):  #Funkcija koja ce uzeti input od korisnika, za datu listu. Ako input nije validan index za tu listu, pitace ponovo, osim ako je x ili X, sto je komanda za 
                            #izlazak iz aplikacije.
        try :
            x = input(">")
            x = eval(x)-1
            l[x]
            return x
        except:
            try:
                if str(x).upper() == "X":
                    exit()
            except Exception as e:
                print(e)
                return(cls.takeX(l))
            return(cls.takeX(l))

        