import sys

# Helper functions to aid in your implementation. Can edit/remove
class Piece:
    def __init__(self, type, is_enemy):
        self.type = type
        self.is_enemy = is_enemy

    def get_blocked_positions(self, row_char, col_char, rows, cols, board):
        blocked = set()
        row = int(row_char)
        col = get_col_int(col_char)
        if self.is_enemy == False:
            return blocked
        if self.type == "King":
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    if i >= 0 and i < rows and j >= 0 and j < cols:
                        blocked.add(get_position_tuple(get_col_char(j), i))
        if self.type == "Queen" or self.type == "Rook":
            for i in range(row + 1, rows):
                if board.is_occupied_at(i, col):
                    break
                blocked.add(get_position_tuple(col_char, i))
            i = row - 1
            while i >= 0:
                if board.is_occupied_at(i, col):
                    break
                blocked.add(get_position_tuple(col_char, i))
                i -= 1
            for j in range(col + 1, cols):
                if board.is_occupied_at(row, j):
                    break
                blocked.add(get_position_tuple(get_col_char(j), row_char))
            j = col - 1
            while j >= 0:
                if board.is_occupied_at(row, j):
                    break
                blocked.add(get_position_tuple(get_col_char(j), row_char))
                j -= 1
        if self.type == "Queen" or self.type == "Bishop":
            i = row
            j = col
            count = 0
            plus_stop = False
            minus_stop = False
            while i >= 0:
                if j + count < cols and (plus_stop == False):
                    if board.is_occupied_at(i, j + count):
                        if not(i == row and j == col):
                            plus_stop = True
                    else:
                        blocked.add(get_position_tuple(get_col_char(j + count), i))
                if j - count >= 0 and (minus_stop == False):
                    if board.is_occupied_at(i, j - count):
                        if not(i == row and j == col):
                            minus_stop = True
                    else:
                        blocked.add(get_position_tuple(get_col_char(j - count), i))
                i -= 1
                count += 1
            i = row
            count = 0
            plus_stop = False
            minus_stop = False
            while i < rows:
                if j + count < cols and (plus_stop == False):
                    if board.is_occupied_at(i, j + count):
                        if not(i == row and j == col):
                            plus_stop = True
                    else:
                        blocked.add(get_position_tuple(get_col_char(j + count), i))
                if j - count >= 0 and (minus_stop == False):
                    if board.is_occupied_at(i, j - count):
                        if not(i == row and j == col):
                            minus_stop = True
                    else:
                        blocked.add(get_position_tuple(get_col_char(j - count), i))
                i += 1
                count += 1
        if self.type == "Knight":
            if (col - 1 >= 0):
                if (row + 2 < rows):
                    blocked.add(get_position_string(get_col_char(col - 1), row + 2))
                if (row - 2 >= 0):
                    blocked.add(get_position_string(get_col_char(col - 1), row - 2))
            if (col - 2 >= 0):
                if (row + 1 < rows):
                    blocked.add(get_position_string(get_col_char(col - 2), row + 1))
                if (row - 1 >= 0):
                    blocked.add(get_position_string(get_col_char(col - 2), row - 1))
            if (col + 1 < cols):
                if (row + 2 < rows):
                    blocked.add(get_position_string(get_col_char(col + 1), row + 2))
                if (row - 2 >= 0):
                    blocked.add(get_position_string(get_col_char(col + 1), row - 2))
            if (col + 2 < cols):
                if (row + 1 < rows):
                    blocked.add(get_position_string(get_col_char(col + 2), row + 1))
                if (row - 1 >= 0):
                    blocked.add(get_position_string(get_col_char(col + 2), row - 1))
        return blocked

    def to_string(self):
        if self.is_enemy:
            return " E " + self.type[:2]
        else:
            return " O " + self.type[:2]

class Grid:
    def __init__(self, row, col, cost):
        self.row = row
        self.col = col
        self.cost = cost
        self.piece = None
        self.is_goal = False
        self.is_blocked = False

    def get_row_as_int(self):
        return self.row

    def get_col_as_int(self):
        return ord(self.col) - 97

    def set_piece(self, piece):
        if self.piece == None:
            self.piece = piece
            self.set_is_blocked()

    def set_is_goal(self):
        self.is_goal = True

    def set_is_blocked(self):
        self.is_blocked = True

    def to_string(self):
        if self.piece != None:
            return "[" + self.piece.to_string() + "]"
        elif self.is_blocked == True:
            return "[Block]"
        return "[     ]"

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

    def set_block(self, row_char, col_char):
        row = int(row_char)
        col = get_col_int(col_char)
        self.grids[row][col].set_is_blocked()

    def is_occupied_at(self, row_int, col_int):
        return self.grids[row_int][col_int].piece != None

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
    return ord(col_char) - 97

def get_col_char(col_int):
    return chr(col_int + 97)

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
    if num_of_obstacles > 0:
        for obstacle in obstacles:
            board.set_piece(Piece("Obstacle", True), obstacle[1:], obstacle[0])
    # Add pieces into the board
    def add_enemies(type):
        blocked = set()
        if type in enemies:
            for pos in enemies[type]:
                piece = Piece(type, True)
                board.set_piece(piece, pos[1:], pos[0])
                blocked_pos = piece.get_blocked_positions(pos[1:], pos[0], rows, cols, board)
                blocked = blocked.union(blocked_pos)
        return blocked
    def add_own(type):
        if type in own_pieces:
            for pos in own_pieces[type]:
                board.set_piece(Piece(type, False), pos[1:], pos[0])
    for type in enemies_names:
        add_own(type)
        blocked = add_enemies(type)
        for position in blocked:
            board.set_block(position[1], position[0])
    # Add goals to the board
    for pos in goals:
        if pos != "-":
            board.set_goal(pos[1:], pos[0])

    print(board.to_string())

    # Search for path
    moves, nodesExplored = search(board, goals) #For reference
    return moves, nodesExplored #Format to be returned

print(run_BFS())