from xmlrpc.client import MAXINT
from minimax.hashmap.hashmap import LinearHashMap
from minimax.heuristicItem import HeuristicItem
from utils import Utils
class Heuristics(object):
    def __init__(self, game):
        self.game = game
        self.items = LinearHashMap()
        self.items["dvostruki"] = HeuristicItem(25, lambda x : len(game.doublesDetected[x]))
        self.items["mica"] = HeuristicItem(100, lambda x : len(game.morrisesDetected[x]))
        self.items["novaMica"] = HeuristicItem(100000, lambda x : len(game.currentMorrises[x]))
        self.items["trostruki"] = HeuristicItem(5, lambda x : len(game.threesDetected[x]))  #manja vrednost zato sto svaka trostruka konfiguracija vec sadrzi double
        self.items["trakalica"] = HeuristicItem(7.5, lambda x : len(game.trakalice[x]))  #manja vrednost zato sto svaka trostruka konfiguracija vec sadrzi double
        self.items["brFiguraIgraca"] = HeuristicItem(300000, lambda x : game.numPieces[x]) 
        self.items["brFiguraProtivnika"] = HeuristicItem(-300000, lambda x : game.numPieces[x]) 
        self.items["dvostrukoBlokiran"] = HeuristicItem(2.33, lambda x : len(game.twiceBlockedPieces[x])) 
        self.items["trostrukoBlokiran"] = HeuristicItem(2.33, lambda x : len(game.semiBlockedPieces[x])) 
        self.items["potpunoBlokiran"] = HeuristicItem(2.66, lambda x : len(game.blockedPieces[x])) 
        self.items["pobeda"] = HeuristicItem(MAXINT, lambda x : game.winningTest(x)) #ovo sluzi kao 2 heuristicke stavke (pobeda +10000, poraz -10000)
        self.items["mobilnost"] = HeuristicItem(5, lambda x : game.moveManager.movesLen[x]) #Ukupan broj poteza koji imamo (tako da su pozicije u kojima su figure mobilnije, vrednije)
        self.items["mobilnostProtivnika"] = HeuristicItem(-5, lambda x : game.moveManager.movesLen[x]) #Ukupan broj poteza koji protivnik ima
    def testHeuristics(self):
        totalHeuristicValue = 0
        totalHeuristicValue += self.items["dvostruki"].testHeuristic(self.game.player)
        totalHeuristicValue += self.items["mica"].testHeuristic(self.game.player)

        totalHeuristicValue += self.items["trostruki"].testHeuristic(self.game.player)
        totalHeuristicValue += self.items["trakalica"].testHeuristic(self.game.player)
        totalHeuristicValue += self.items["brFiguraIgraca"].testHeuristic(self.game.player)
        totalHeuristicValue += self.items["dvostrukoBlokiran"].testHeuristic(self.game.player)
        totalHeuristicValue += self.items["trostrukoBlokiran"].testHeuristic(self.game.player)
        totalHeuristicValue += self.items["potpunoBlokiran"].testHeuristic(self.game.player)
        totalHeuristicValue += self.items["brFiguraProtivnika"].testHeuristic(Utils.otherPlayer(self.game.player))
        totalHeuristicValue += self.items["pobeda"].testHeuristic(Utils.otherPlayer(self.game.player))
        totalHeuristicValue += self.items["mobilnost"].testHeuristic(self.game.player)
        totalHeuristicValue += self.items["mobilnostProtivnika"].testHeuristic(Utils.otherPlayer(self.game.player))
        totalHeuristicValue += self.items["novaMica"].testHeuristic(self.game.player)
        #print(self.items["brFiguraProtivnika"].testHeuristic(self.game.player))
        return totalHeuristicValue
        
        