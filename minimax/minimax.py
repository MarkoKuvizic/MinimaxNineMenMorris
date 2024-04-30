

from xmlrpc.client import MAXINT, MININT
from utils import Utils
import game
import time
from minimax.hashmap.hashmap import LinearHashMap
class Minimax(object): 
    def __init__(self):
        self.maxMap = LinearHashMap()
        self.p1Map = LinearHashMap()
        self.moves = []
        self.placements = []
        self.removal = []
        self.closedMorris = False
        self.won = False
    def minimax(self, game1, player, depth = 6):
        self.won = False
        self.removal = []
        self.moves = []
        game1TMP = game1
        self.depth = depth
        start = time.time()
        self.depth = depth
        self.start = start
        
        if player == game1.player:
            m, mo, re = self.max(MININT, game1, depth, game1.player)
        else:
            m, mo, re = self.min(MAXINT, game1, depth, game1.player)
        
        end = time.time()
        print(end - start)
        return m, mo, game1TMP.moveManager, re
    def removalMinimax(self, game1, player, removals, mode = True, depth = 5):
        max = -200000
        for rem in removals:
            g = game.Game(game1, rem, [], player, rem)
            m = 0
            m, mo, re = self.max(max, g, depth, game1.player)
            if m > max:
                max= m
                if mode:
                    
                    self.removal = rem
        if not mode:
            return m, mo, re
    def removalMin(self, game1, player, removals, mode = True, depth = 5):
        mn = 2000
        for rem in removals:
            g = game.Game(game1, rem, [], player, rem)
            m = 0
            m, mo, re = self.max(mn, g, depth, game1.player)
            if m < mn:
                mn= m
                if mode:
                    self.removal = rem
        if not mode:
            return m, mo, re
    def max(self, max, node, depth, player, toRemove=[], alpha=MININT, beta=MAXINT):
        # if node.moveManager.board.board
        if self.won:
            return MAXINT, [], []
        if repr([node.moveManager.board.board, depth]) in self.maxMap and depth != self.depth:
            return self.maxMap[repr([node.moveManager.board.board, depth])], node.move, toRemove
        if depth <= 0 or time.time()-self.start > 1.8:
            node.heuristics.testHeuristics()
            return node.heuristicValue, node.move, toRemove
        possibleMoves = node.possibleMoves(player)
        
        
        re = []
        mo = []
        r = []
        max = MININT
        for key in possibleMoves.keys():
            for move in possibleMoves[key]:
                
                
                tmpBoard = [row[:] for row in node.moveManager.board.board]
                game1 = game.Game(node, key, move, player)
                posRem = game1.possibleRemovals2(player)
                # print("MOVE", move, "POSREM", posRem)
                if posRem != []:
                    for rem in posRem:
                        g = game.Game(node, rem, [], player, rem)
                        
                        if min(g.numPieces[0], g.numPieces[1]) <= 3 and depth == self.depth:
                            self.moves = [[[list(key), list(move)], True]]
                            print("I CAN WIN")
                            self.removal = rem
                            self.won = True
                            return MAXINT, node.move, toRemove
                        m, faf, re = self.min(max, g, depth-1, player, rem, alpha, beta)
                        m -= (self.depth - depth)* 10000 #ako postoji moguca mica, ali nadjena je na vecoj dubini (depth je inverzan), ona vredi manje od mice koja je recimo odmah u sledecem potezu
                                                            #(dubina se koristi kao neka vrsta aproksimacije menhetn razdaljine)
                        if m > max:
                            max = m
                            
                            mo = [key, move]
                            if depth == self.depth:
                                self.removal = rem
                                self.moves = []
                                self.moves.append([[list(key), list(move)], True])

                        elif m == max and depth == self.depth:
                            self.moves.append([[list(key), list(move)], True])
                        if max >= beta:
                            return max, [key, move], toRemove
                        if max > alpha:
                            alpha = max
                else:
                    m, faf, re = self.min(max, game1, depth-1, Utils.otherPlayer(player), alpha, beta)
                self.maxMap[repr([node.moveManager.board.board, depth])] = m
                

                if m > max:
                    max = m
                    if depth == self.depth:
                        self.moves = []
                        self.moves.append([[list(key), list(move)], False])
                elif m == max and depth == self.depth:
                    self.moves.append([[list(key), list(move)], False])

                if max >= beta:
                    return max, [key, move], toRemove
                if max > alpha:
                    alpha = max
        return max, mo, re
        
    def min(self, mn, node, depth, player, toRemove=[], alpha=MININT, beta=MAXINT):
     
        if repr([node.moveManager.board.board, depth]) in self.maxMap and depth != self.depth:
            node.heuristics.testHeuristics()
            return self.maxMap[repr([node.moveManager.board.board, depth])], node.move, toRemove
        if depth <= 0 or time.time()-self.start > 1.8:
            return node.heuristicValue, node.move, toRemove
        possibleMoves = node.possibleMoves()

        r = []
        
        re = []
        mo = []
        r = []
        mn = MAXINT
        for key in possibleMoves.keys():
            for move in possibleMoves[key]:
                
                if node.moveManager.board.board[move[0]][move[1]] != 0:
                    continue

                game1 = game.Game(node, key, move, player)

                posRem = game1.possibleRemovals2(player)
                if posRem != []:
                #m, mo= self.removalMinimaxP1 (game1, player, posRem,max, True, depth-2) #-2 zato sto skidanje figure koristi jedan nivo dubine
                    node.numPieces[player-1] -= 1
                    for rem in posRem:
                        tmpBoard = [row[:] for row in game1.moveManager.board.board]
                        g = game.Game(node, rem, [], player, rem)
                        m, faf, re = self.min(mn, g, depth-1, player, rem, alpha, beta)
                        game1.moveManager.board.board = tmpBoard
                        if m < mn:
                            mn = m
                            mo = [key, move]
                        if mn <= alpha:
                            return mn, [key, move], toRemove
                        if mn < beta:
                            beta = mn

                else:
                    m, faf, re = self.max(mn, game1, depth-1, Utils.otherPlayer(player), alpha, beta)
                self.maxMap[repr([node.moveManager.board.board, depth])] = m
                
                if m < mn:
                    mn = m
                    mo = [key, move]
                    
                if mn <= alpha:
                    return mn, [key, move], toRemove

                if mn < beta:
                    beta = mn
        return mn, mo, re
        
    def minimaxP1(self, game1, player, closedMorris = False, depth = 5):
        self.placements = []
        self.moves = []
        self.closedMorris = closedMorris
        game1TMP = game1
        self.depth = depth
        start = time.time()
        self.start = start
        if player == game1.player:
            m , mo = self.maxP1(-2000, game1, depth, game1.player)
        else:
            m, mo = self.minP1(2000, game1, depth, game1.player)
        
        end = time.time()
        print(end - start)
        return m, mo, game1TMP.moveManager
        
       
    def maxP1(self, max, node, depth, player,  rem = [], alpha=MININT, beta=MAXINT):
        # if node.moveManager.board.board
        

        if repr([node.moveManager.board.board, depth]) in self.p1Map and depth != self.depth:
            return self.p1Map[repr([node.moveManager.board.board, depth])], node.move
        if depth <= 0 or time.time()-self.start > 1.8:
            return node.heuristicValue, node.move
        possibleMoves = node.free
        re = []
        mo = []
        r = []
        max = MININT
        
        for move in possibleMoves:
                
            game1 = game.Game(node, [], move, player)
            posRem = game1.possibleRemovals2(player)
            
            if posRem != []:
                for rem in posRem:
                    tmpBoard = [row[:] for row in game1.moveManager.board.board]
                    game1.moveManager.board.board[rem[0]][rem[1]] = 0
                    g = game.Game(game1, rem, [], player, rem)
                    m, faf  = self.minP1(max, g, depth-1, player, rem, alpha, beta)
                    game1.moveManager.board.board = tmpBoard
                    m -= (self.depth - depth)* 10000 #ako postoji moguca mica, ali nadjena je na vecoj dubini (depth je inverzan), ona vredi manje od mice koja je recimo odmah u sledecem potezu
                    if m > max:
                        max = m
                            
                        mo = move
                        if depth == self.depth:
                            self.removal = rem
                            self.moves = []
                            self.moves.append([list(move), True])

                    elif m == max and depth == self.depth:
                        self.moves.append([list(move), True])
                        self.removal = rem
                    if max >= beta:
                        return max, move
                    if max > alpha:
                        alpha = max                
            else:
                m, faf = self.minP1(max, game1, depth-1, Utils.otherPlayer(player), alpha, beta)
            self.p1Map[repr([node.moveManager.board.board, depth])] = m
                


            if m > max:
                max = m
                if depth == self.depth:
                    self.moves = []
                    self.moves.append([list(move), False])
            elif m == max and depth == self.depth:
                self.moves.append([list(move), False])

            if max >= beta:
                return max, move
            if max > alpha:
                alpha = max
        
        return max, mo
    def minP1(self, mn, node, depth, player,  rem = [], alpha=MININT, beta=MAXINT):

        if repr([node.moveManager.board.board, depth]) in self.p1Map and depth != self.depth:
            return self.p1Map[repr([node.moveManager.board.board, depth])], node.move
        if depth <= 0 or time.time()-self.start > 1.8:
            return node.heuristicValue, node.move
        possibleMoves = node.free

        
        re = []
        mo = []
        r = []
        max = MININT
        
        for move in possibleMoves:
                
            tmpBoard = [row[:] for row in node.moveManager.board.board]
            game1 = game.Game(node, [], move, player)
            posRem = game1.possibleRemovals2(player)
            if posRem != []:
                for rem in posRem:
                    tmpBoard = [row[:] for row in game1.moveManager.board.board]
                    game1.moveManager.board.board[rem[0]][rem[1]] = 0
                    g = game.Game(game1, rem, [], player, rem)
                    m, faf  = self.maxP1(max, g, depth-1, player, rem, alpha, beta)
                    game1.moveManager.board.board = tmpBoard
                    
                    if m < mn:
                        mn = m
                        mo = move
                    if mn <= alpha:
                        return mn, move
                    if mn < beta:
                        beta = mn
                
            else:
                m, faf = self.maxP1(max, game1, depth-1, Utils.otherPlayer(player), alpha, beta)
            self.p1Map[repr([node.moveManager.board.board, depth])] = m
                


            if m < mn:
                mn = m
                mo =  move
            if mn <= alpha:
                return mn, move
            if mn < beta:
                beta = mn
        
        return max, mo
    def removalMinP1(self, game1, player, removals, mode = True, depth = 5):
        if depth <= 0:
            return game1.heuristicValue, game1.placed
        if game1.moveManager.board.board in self.maxMap:
            return self.maxMap[repr(game1.moveManager.board.board)], game1.placed
        mn = 2000
        mo = []
        m = 0
        for rem in removals:
            g = game.Game(game1, rem, [], player, rem)
            
            m, mo = self.minP1(mn, g, depth, game1.player)
            if m < mn:
                mn= m
                self.minMap[repr(g.moveManager.board.board)] = m
                if mode:
                    self.removal = rem
        
        return m, mo
    
    
    