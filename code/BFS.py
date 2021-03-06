from Mouse import Mouse
from MapState import MapState
from Cat import Cat
from Cheese import Cheese
import math
import time

   
class BFS():
    
    def __init__(self):
        self.searchCount = 0
        self.ifCatWin = False

    def calculateDistance(self, point1, point2):
        distanceX = point1[0] - point2[0]
        distanceY = point1[1] - point2[1]
        distance = math.sqrt(distanceX * distanceX + distanceY * distanceY)
        # print("distance", distance)
        return distance

    def getClosestCheese(self, mousePos, cheeseList):
        closestCheese = cheeseList[0]
        currentDistance = self.calculateDistance(mousePos, cheeseList[0].getPos())
        for cheese in cheeseList:
            distance = self.calculateDistance(mousePos, cheese.getPos())
            if(distance < currentDistance):
                closestCheese = cheese
                currentDistance = distance
        return closestCheese

    def MouseMove(self, mousePos, cheesePos):
        # mousePossibleMoveDict = dict({-135 : [1, 1], -90 : [1, 0], -45 : [1, -1], 0 : [0, -1], 45 : [-1, -1], 90 : [-1, 0], 135 : [-1, 1], 180 : [0, 1], -180 : [0,1]})
        mousePossibleMoveDict2 = dict({-135 : [2, 2], -90 : [2, 0], -45 : [2, -2], 0 : [0, -2], 45 : [-2, -2], 90 : [-2, 0], 135 : [-2, 2], 180 : [0, 2], -180 : [0,2]})
        distanceX = mousePos[0] - cheesePos[0]
        distanceY = mousePos[1] - cheesePos[1]
        degree = math.degrees(math.atan2(distanceY, distanceX))
        roundedDegree = round(degree/45) * 45
        mouseMove = mousePossibleMoveDict2[roundedDegree]
        # mouseMove = mousePossibleMoveDict2[roundedDegree]
        newMousePos = [mousePos[0] + mouseMove[1], mousePos[1] + mouseMove[0]]
        return newMousePos

    def run(self, myMap):
        catPossibleMoveList = [[-2, -1], [-2, 1], [-1, -2], [-1, 2], [1, -2], [1, 2], [2, -1], [2, 1]]
        mouseMoveTrackingList = []
        moveTrackingState = []
        stateQueue = []
        catSearchedList = []
        remainingCheeseNum = 0
        stateQueue.append(myMap)
        solution = None
        mouseMoveTrackingList.append(myMap.mouse.getPos())

        while (solution == None):
            if(len(stateQueue) != 0):
                # FIFO queue for BFS
                currentState = stateQueue.pop(0)
            
                if (len(currentState.cheeseList) == 0):
                    print("Mouse has eaten all the cheeses! ")
                    self.ifCatWin = False
                    break

                closestCheese = self.getClosestCheese(currentState.mouse.getPos(), currentState.cheeseList)
                nextMouseMove = self.MouseMove(currentState.mouse.getPos(), closestCheese.getPos())
                # add mouseMove to list (for testing)
                if(nextMouseMove not in mouseMoveTrackingList):
                    mouseMoveTrackingList.append(nextMouseMove)

                # Generate current node's successors
                for possibleMoves in catPossibleMoveList:
                    
                    newCheeseList = []
                    for cheese in currentState.cheeseList:
                        cheese1 = Cheese(cheese.cheesePos)
                        newCheeseList.append(cheese1)
                    nextCatMove = [currentState.cat.catPos[0] + possibleMoves[1], currentState.cat.catPos[1] + possibleMoves[0]]
                    # generate a successor and set its parent to currentState
                    nextState = MapState(currentState, newCheeseList, Mouse(nextMouseMove), Cat(nextCatMove), currentState.mapWidth, currentState.mapHeight)
                    nextState.updateMousePos(nextMouseMove)

                    # make sure nextCatMove is in boundary and the state is not in visited state list
                    if (nextCatMove[0] >= 0 and nextCatMove[0] < nextState.mapWidth and nextCatMove[1] < nextState.mapHeight and nextCatMove[1] >= 0 and (nextState not in catSearchedList)):
                        nextState.updateCatPos(nextCatMove)
                        catSearchedList.append(nextState)

                        if(nextCatMove == nextMouseMove):
                            solution = nextState
                            break
                        # add the state to queue
                        stateQueue.append(nextState)
                # count for iterations
                self.searchCount += 1
                print(self.searchCount)
                if(self.searchCount > 10000):
                    print("Having more than 10000 searchs, generating a new map...")
                    self.ifCatWin = False
                    break

            # cannot find a solution
            else:
                solution = currentState
                self.ifCatWin = False
                break
        if(solution != None):
            self.ifCatWin = True
            remainingCheeseNum = len(solution.cheeseList)
            # add solution to tracking list one by one
            while(solution != None):
                moveTrackingState.append(solution)
                solution = solution.parentState
            moveTrackingState.reverse()

            for state in moveTrackingState:
                state.updateCatPos(state.cat.catPos)
                state.updateMousePos(state.mouse.mousePos)
                time.sleep(1)
                state.covertMapToUI()
            print("Cat Win!")
            print("Search Count:", self.searchCount)
            print("Total Move:", len(moveTrackingState) - 1)
            print("Number of cheeses remaining:", remainingCheeseNum)
            
                
        