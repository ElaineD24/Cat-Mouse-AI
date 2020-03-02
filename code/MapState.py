from random import randint
from Mouse import Mouse
from Cat import Cat
from Cheese import Cheese
import math

gameMap = []

randomX = 0
randomY = 0
randomList = []

# constants
# CHEESE_NUM = 3
TOTAL_NUM = 5

class MapState():

    def __init__(self, parentState, cheeseList, mouse, cat, mapWidth, mapHeight):
        self.parentState = parentState
        self.cheeseList = cheeseList
        self.mouse = mouse
        self.cat = cat
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        # used for A star search
        self.estimate_H_n = self.heuristicFunc2()
        self.catMoveCount_G_n = 0
        self.cost_F_n = self.estimate_H_n + self.catMoveCount_G_n
        self.childrenStateList = []

    # def __eq__(self, other):
    #     if(other == None):
    #         return False
    #     return self.parentState == other.parentState and self.mouse == other.mouse and self.cat == other.cat \
    #         and self.estimate_H_n == other.estimate_H_n and self.catMoveCount_G_n == other.catMoveCount_G_n and self.cost_F_n == other.cost_F_n
        
    def setRandomPos(self, item):
        # randomly choose a position from the random position list
        chooseOnePosIndex = randint(0, len(randomList) - 1)
        chooseOnePosX = randomList[chooseOnePosIndex][0]
        chooseOnePosY = randomList[chooseOnePosIndex][1]
        if item == "🧀️"+"1" or item == "🧀️"+"2" or item == "🧀️"+"3":
            gameMap[chooseOnePosX][chooseOnePosY] = "🧀️"
        else:
            gameMap[chooseOnePosX][chooseOnePosY] = item
        
        if item == "😻":
            self.cat.setPos([chooseOnePosY, chooseOnePosX])
        if item == "🐭":
            self.mouse.setPos([chooseOnePosY, chooseOnePosX])
        if item == "🧀️"+"1":
            self.cheeseList[0].setPos([chooseOnePosY, chooseOnePosX])
        if item == "🧀️"+"2":
            self.cheeseList[1].setPos([chooseOnePosY, chooseOnePosX])
        if item == "🧀️"+"3":
            self.cheeseList[2].setPos([chooseOnePosY, chooseOnePosX])
        
        # remove used position
        randomList.remove([chooseOnePosX,chooseOnePosY])

            
    # set position for items
    def setPosInit(self):
        # to avoid duplicate position
        while len(randomList) == 0 or (len(randomList) < TOTAL_NUM):
            # create a random position list
            randomX = randint(0, self.mapWidth - 1)
            randomY = randint(0, self.mapHeight - 1)
            if [randomX, randomY] not in randomList:
                randomList.append([randomX, randomY])
        # print(randomList)

        # assign random position to different item
        for i in range (len(self.cheeseList)):
            self.setRandomPos("🧀️"+str(i+1))

        self.setRandomPos("🐭")
        self.setRandomPos("😻")


    def setInitState(self):
        # set position for blank space
        for i in range (self.mapHeight):
            gameMap.append([])
            for j in range (self.mapWidth):
                gameMap[i].append("_")

        self.setPosInit()
    
    def clearMap(self):
        for i in range (self.mapHeight):
            for j in range (self.mapWidth):
                gameMap[i][j] = "_"

    # print map to console
    def covertMapToUI(self):
        self.clearMap()
        for i in range (len(self.cheeseList)):
            gameMap[self.cheeseList[i].cheesePos[1]][self.cheeseList[i].cheesePos[0]] = "🧀️"
        gameMap[self.mouse.mousePos[1]][self.mouse.mousePos[0]] = "🐭"
        gameMap[self.cat.catPos[1]][self.cat.catPos[0]] = "😻"

        for i in range (self.mapHeight):
            print(" ".join(gameMap[i]))
        print("*********************************")

    def updateMousePos(self, newPos):
        # upate cheese list
        if (len(self.cheeseList) != 0):
            for cheese in self.cheeseList:
                if (cheese.getPos() == newPos):
                    self.cheeseList.remove(cheese)
                    break

        self.mouse.setPos(newPos)

    def updateCatPos(self, newPos):

        self.cat.setPos(newPos) 

# -------------------------Used for A star search-----------------------------------------
    def addChildren(self, childState):
        self.childrenStateList.append(childState)
    
    def updateCurrentCost(self):
        self.cost_F_n =  self.estimate_H_n + self.catMoveCount_G_n

    def updateCost(self, catMoveCount):
        self.catMoveCount_G_n = catMoveCount
        # Update the cost of getting to this node 
        self.cost_F_n = catMoveCount + self.estimate_H_n
        # Update the cost of getting to the children 
        self.updateChildrenCost(self)

    def updateChildrenCost(self, myMapState):
        if len(myMapState.childrenStateList) == 0:
            return
        else:
            # recursively “regenerating” the successors using the list of
            # successors that had been recorded in the found node
            for state in myMapState.childrenStateList:
                state.catMoveCount_G_n = self.catMoveCount_G_n
                myMapState.cost = state.catMoveCount_G_n + state.estimate_H_n
                self.updateChildrenCost(state)

    # Calculating the euclidean distance of the cat position relative to the mouse position at each state(where whenever mouse moves, cat moves)
    # and divide that by square root of 5 since 1 cat move = square root of 5 in euclidean distance, to ensure the heuristic function does not overestimate
    def heuristicFunc1(self):
        return (math.sqrt((math.pow(self.cat.catPos[0] - self.mouse.mousePos[0], 2)) + (math.pow(self.cat.catPos[1] - self.mouse.mousePos[1], 2)))) / math.sqrt(5)


    # Calculating the Manhattan distance of the cat position to the center of all of the cheese position coordinates
    # divide the value by 3 since 1 cat move = 3 in Manhattan distance, to ensure our heuristic function does not overestimate
    def heuristicFunc2(self):
        return (abs(self.cat.catPos[0] - self.mouse.mousePos[0]) + abs(self.cat.catPos[1] - self.mouse.mousePos[1])) / 3

    def heuristicFunc3(self):
        return (self.heuristicFunc1() + self.heuristicFunc2())/2