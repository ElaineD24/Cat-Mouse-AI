class Cheese():

    def __init__(self, cheesePos):
        self.cheesePos = cheesePos
    
    def __eq__(self, other):
        return self.cheesePos == other.cheesePos
    
    def getPos(self):
        return self.cheesePos
    
    def setPos(self, pos):
        self.cheesePos = pos