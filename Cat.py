class Cat():

    def __init__(self, catPos):
        self.catPos = catPos
    
    def __eq__(self, other):
        return self.catPos == other.catPos

    def getPos(self):
        return self.catPos
    
    def setPos(self, pos):
        self.catPos = pos