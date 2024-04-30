class HeuristicItem(object):    #klasa modeluje jednu stavku heuristike (sa vrednoscu i opciono funkcijom za proveravanje)
    def __init__(self, value, function):
        self.value = value
        self.function = function
    def testHeuristic(self, x):    
        return self.function(x -1) * self.value #Vazno je da sve funkcije za testiranje heuristickih elemenata vracaju broj pojavljivanja tog elementa (0-n)