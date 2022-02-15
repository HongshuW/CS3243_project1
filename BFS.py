import sys

# Helper functions to aid in your implementation. Can edit/remove
class Piece:
    def __init__(self, type, is_enemy):
        self.type = type
        self.is_enemy = is_enemy

    def to_string(self):
        if self.is_enemy:
            return "Enemy " + self.type
        else:
            return "Own " + self.type

class Grid:
    def __init__(self, row, col, cost):
        self.row = row
        self.col = col
        self.cost = cost
        self.piece = None
        self.is_goal = False

    def get_row_as_int(self):
        return self.row

    def get_col_as_int(self):
        return ord(self.col) - 97

    def set_piece(self, piece):
        self.piece = piece

    def set_is_goal(self):
        self.is_goal = True

    def to_string(self):
        if self.piece == None:
            return "[" + get_position_string(self.col, self.row) + ": None" + "]"
        return "[" + get_position_string(self.col, self.row) + ": " + self.piece.to_string() + "]"

class Board:
    def __init__(self, width, height, costs):
        # create an empty board of size width * height that does not contain pieces
        self.grids = []
        for row in range(height):
            row_array = []
            for col in range(width):
                pos = get_position_string(get_col_char(col), row)
                if pos in costs:
                    row_array.append(Grid(row, get_col_char(col), costs[pos]))
                else:
                    row_array.append(Grid(row, get_col_char(col), 1))
            self.grids.append(row_array)

    def set_piece(self, piece, row_char, col_char):
        row = int(row_char)
        col = get_col_int(col_char)
        self.grids[row][col].set_piece(piece)

    def set_goal(self, row_char, col_char):
        row = int(row_char)
        col = get_col_int(col_char)
        self.grids[row][col].set_is_goal()

    def to_string(self):
        string = ""
        for row in self.grids:
            for grid in row:
                string += grid.to_string() + " "
            string += "\n"
        return string

class State:
    def __init__(self, king, moves, nodesExplored):
        self.king = king # own king
        self.moves = moves
        self.nodesExplored = nodesExplored

def get_col_int(col_char):
    return ord(col_char) - 97;

def get_col_char(col_int):
    return chr(col_int + 97);

def get_position_string(col_char, row):
    return col_char + str(row)

def get_position_tuple(col_char, row):
    return (col_char, row)

def search(board, goals):
    moves = []
    nodesExplored = 0

    if (len(goals) == 0 or (len(goals) == 1 and "-" in goals)):
        return moves, nodesExplored

    return moves, nodesExplored


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_BFS():

    # Parse the file
    input_file = open(sys.argv[1], "r")
    lines = input_file.readlines()
    rows = int(lines[0][5:])
    cols = int(lines[1][5:])
    ### num_of_obstacles = int(lines[2][20:]) ###
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
            enemies[enemies_names[j]] = []
    i += 2
    while (lines[i][0] == "["):
        information = lines[i][1:-2].split(",")
        enemies[information[0]].append(information[1])
        i += 1
    # record positions of own pieces
    own_pieces = dict()
    own_names = lines[i][14:47].split(", ")
    own_count = lines[i][64:].split()
    for j in range(5):
        if (int(own_count[j]) > 0):
            own_pieces[own_names[j]] = []
    i += 2
    while (lines[i][0] == "["):
        information = lines[i][1:-2].split(",")
        own_pieces[information[0]].append(information[1])
        i += 1
    # parse goal position
    goals = lines[i][31:].split()

    # Initialise a board
    board = Board(cols, rows, costs)
    # Add obstacles
    for obstacle in obstacles:
        board.set_piece(Piece("Obstacle", True), obstacle[1:], obstacle[0])
    # Add pieces into the board
    def add_pieces(type):
        if type in enemies:
            for pos in enemies[type]:
                board.set_piece(Piece(type, True), pos[1:], pos[0])
        if type in own_pieces:
            for pos in own_pieces[type]:
                board.set_piece(Piece(type, False), pos[1:], pos[0])
    for type in enemies_names:
        add_pieces(type)
    # Add goals to the board
    for pos in goals:
        if pos != "-":
            board.set_goal(pos[1:], pos[0])

    # Search for path
    moves, nodesExplored = search(board, goals) #For reference
    return moves, nodesExplored #Format to be returned

print(run_BFS())