from MapState import MapState
from Mouse import Mouse
from Cat import Cat
from Cheese import Cheese
import math
import time


class AStarSearch():
    
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
        mousePossibleMoveDict = dict({-135 : [1, 1], -90 : [1, 0], -45 : [1, -1], 0 : [0, -1], 45 : [-1, -1], 90 : [-1, 0], 135 : [-1, 1], 180 : [0, 1], -180 : [0,1]})
        distanceX = mousePos[0] - cheesePos[0]
        distanceY = mousePos[1] - cheesePos[1]
        degree = math.degrees(math.atan2(distanceY, distanceX))
        roundedDegree = round(degree/45) * 45
        mouseMove = mousePossibleMoveDict[roundedDegree]
        newMousePos = [mousePos[0] + mouseMove[1], mousePos[1] + mouseMove[0]]
        return newMousePos

    def run(self, myMap):
        catPossibleMoveList = [[-2, -1], [-2, 1], [-1, -2], [-1, 2], [1, -2], [1, 2], [2, -1], [2, 1]]
        moveTrackingState = []
        remainingCheeseNum = 0
        openStateList = []
        myMap.updateCurrentCost()
        openStateList.append(myMap)
        solution = None
        closedStateList = []

        while (solution == None):
            if(len(openStateList) != 0):
                # sort the list by F(n) (Estimated total cost of path through n to goal)
                openStateList.sort(key=lambda x: x.cost_F_n)
                # pick the best node in list
                currentState = openStateList.pop(0)
                if (currentState not in closedStateList):
                    # place the visited node in CLOSED
                    closedStateList.append(currentState)

                if (len(currentState.cheeseList) == 0):
                    print("Mouse has eaten all the cheeses! ")
                    self.ifCatWin = False
                    break

                closestCheese = self.getClosestCheese(currentState.mouse.getPos(), currentState.cheeseList)
                nextMouseMove = self.MouseMove(currentState.mouse.getPos(), closestCheese.getPos())
                # Generate current node's successors
                for possibleMoves in catPossibleMoveList:
                    nextCatMove = [currentState.cat.catPos[0] + possibleMoves[1], currentState.cat.catPos[1] + possibleMoves[0]]
                    newCheeseList = []
                    for cheese in currentState.cheeseList:
                        cheese1 = Cheese(cheese.cheesePos)
                        newCheeseList.append(cheese1)
                    # generate a successor and set its parent to currentState
                    nextState = MapState(currentState, newCheeseList, Mouse(nextMouseMove), Cat(nextCatMove), currentState.mapWidth, currentState.mapHeight)
                    # incremented G(n) by 1
                    nextState.catMoveCount_G_n = currentState.catMoveCount_G_n + 1

                    # If not previously generated (not found in OPEN or CLOSED)
                    # Evaluate, add to OPEN , and record its parent
                    if (nextCatMove[0] >= 0 and nextCatMove[0] < nextState.mapWidth and nextCatMove[1] < nextState.mapHeight and nextCatMove[1] >= 0 and (nextState not in closedStateList) and (nextState not in openStateList)):
                        nextState.updateMousePos(nextMouseMove)
                        # add children
                        currentState.addChildren(nextState)
                        if(nextCatMove == nextMouseMove):
                            solution = nextState
                            break
                        nextState.updateCurrentCost()
                        # add successor to OPEN
                        openStateList.append(nextState)      
                    # If previously generated ( found in OPEN or CLOSED), 
                    # and if the new path is better then the previous one
                    for state in openStateList:
                        if state.mouse.mousePos == currentState.mouse.mousePos and not state.parentState == currentState.parentState and \
                            currentState.catMoveCount_G_n < state.catMoveCount_G_n:
                            # Change parent pointer that was recorded in the found node
                            state.parentState = currentState.parentState
                            state.updateCost(currentState.catMoveCount_G_n)
                    for state in closedStateList:
                        if state.mouse.mousePos == currentState.mouse.mousePos and not state.parentState == currentState.parentState and \
                            currentState.catMoveCount_G_n < state.catMoveCount_G_n:
                            # Change parent pointer that was recorded in the found node
                            state.parentState = currentState.parentState
                            state.updateCost(currentState.catMoveCount_G_n)        
                # count for iterations
                self.searchCount += 1
                print(self.searchCount)
                if(self.searchCount > 1000):
                    print("Having more than 1000 searchs, generating a new map...")
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
            
                
        