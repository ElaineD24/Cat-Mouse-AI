from MapState import MapState
from random import randint
from Mouse import Mouse
from Cat import Cat
from Cheese import Cheese
from BFS import BFS
from DFS import DFS
from AStar import AStarSearch
import copy

# Initialize items' position, not used for random map
cheese1 = Cheese([1,10])
cheese2 = Cheese([11, 1])
cheese3 = Cheese([4,8])

cheeseList = [cheese1, cheese2, cheese3]
mouse = Mouse([6, 4])
cat = Cat([10, 7])

MAP_HEIGHT = 12
MAP_WIDTH = 12
searchMethod = BFS()


myMap = MapState(None, cheeseList, mouse, cat, MAP_WIDTH, MAP_HEIGHT)
# set random positions
myMap.setInitState()

# ------------------For random map---------------
while(searchMethod.ifCatWin == False):
    print("Generating a random map...")
    searchMethod = BFS()
    # searchMethod = DFS()
    # searchMethod = AStarSearch()
    myMap.setPosInit()
    searchMethod.run(myMap)

#-----------------For a centain map----------------
# searchMethod = BFS()
# searchMethod = DFS()
# searchMethod = AStarSearch()
# searchMethod.run(myMap)