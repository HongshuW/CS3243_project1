import sys
# Helper functions to aid in your implementation. Can edit/remove
class Piece:
    def __init__(self, type):
        self.type = type

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class State:
    def __init__(self, location, moves, nodesExplored):
        self.location = location
        self.moves = moves
        self.nodesExplored = nodesExplored

def search():
    moves = []
    nodesExplored = 0

    return moves, nodesExplored


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_BFS():

    # Parse the file
    input_file = open(sys.argv[1], "r")
    lines = input_file.readlines()
    rows = int(lines[0][5:])
    cols = int(lines[1][5:])
    num_of_obstacles = int(lines[2][20:])
    # list of positions of the obstacles
    obstacles = lines[3][38:].split()
    # record all costs
    costs = dict()
    i = 5
    while (lines[i][0] == "["):
        information = lines[i][1:-2].split(",")
        position = information[0]
        cost = int(information[1])
        costs[position] = cost
        i += 1
    # record positions of enemies
    enemies = dict()
    enemies_names = lines[i][16:49].split(", ")
    enemies_count = lines[i][66:].split()
    for j in range(5):
        if (int(enemies_count[j]) > 0):
            enemies[enemies_names[j]] = set()
    i += 2
    while (lines[i][0] == "["):
        information = lines[i][1:-2].split(",")
        enemies[information[0]].add(information[1])
        i += 1
    # record positions of own pieces
    own_pieces = dict()
    own_names = lines[i][14:47].split(", ")
    own_count = lines[i][64:].split()
    for j in range(5):
        if (int(own_count[j]) > 0):
            own_pieces[own_names[j]] = set()
    i += 2
    while (lines[i][0] == "["):
        information = lines[i][1:-2].split(",")
        own_pieces[information[0]].add(information[1])
        i += 1
    # parse goal position
    goal = lines[i][31:].split()

    # Search for path
    moves, nodesExplored = search() #For reference
    return moves, nodesExplored #Format to be returned

run_BFS()