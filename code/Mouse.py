class Mouse():

    def __init__(self, mousePos):

        self.mousePos = mousePos

    def __eq__(self, other):
        return self.mousePos == other.mousePos

    def getPos(self):
        return self.mousePos

    def setPos(self, pos):
        self.mousePos = pos