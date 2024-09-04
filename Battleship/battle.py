import argparse
import copy
import sys

# This is my solution for the classic Battleship Solitaire problem

# Reads an input file
# python battle.py --inputfile <input file> --outputfile <output file>
# python battle.py --inputfile puzzle1.txt --outputfile solution1.txt
def read_from_file(filename):
    f = open(filename)
    lines = f.readlines()
    f.close()
    puzzle = []
    for i, l in enumerate(lines):
        if i == 0:
            row_constraints = list(l)[:-1]
        elif i == 1:
            col_constraints = list(l)[:-1]
        elif i == 2:
            num_ships = list(l)[:-1]
        elif i < len(lines) - 1:
            puzzle.append(list(l)[:-1])
        else:
            puzzle.append(list(l))
    return [row_constraints, col_constraints, num_ships, puzzle]

# Prints the solution to an output file
def print_to_file(filename, solution):
    sys.stdout = open(filename, 'w')
    for l in solution:
        line = ''
        for cell in l:
            if cell != '0':
                line += cell
            else:
                line += '.'
        print(line)
    sys.stdout = sys.__stdout__
    return

# Checks if the solution is a valid solution
def check_solution(row_constraints, col_constraints, ships, puzzle, original):
    for i in row_constraints:
        if i != 0:
            return False
    for j in col_constraints:
        if j != 0:
            return False
    for k in ships:
        if k != 0:
            return False
    for i, row in enumerate(original):
        for j, val in enumerate(row):
            if val != '0' and val != puzzle[i][j]:
                return False
    return True


class State:
    def __init__(self, row_constraints, col_constraints, ships, puzzle):
        self.row_constraints = row_constraints
        self.col_constraints = col_constraints
        self.ships = ships
        self.puzzle = puzzle
        self.original = copy.deepcopy(puzzle)

    # Prints the puzzle into terminal
    def display(self):
        print("Row Constraints:")
        print(self.row_constraints)
        print("Col Constraints:")
        print(self.col_constraints)
        print("Ships:")
        print(self.ships)
        print("Puzzle:")
        for row in self.puzzle:
            print(row)

    def check_constraints(self):
        for i in self.row_constraints:
            if i < 0:
                return False
        for j in self.col_constraints:
            if j < 0:
                return False
        for k in self.ships:
            if k < 0:
                return False
        return True

    def remove_connectors(self):
        for i, row in enumerate(self.puzzle):
            for j, val in enumerate(row):
                if val == 'M':
                    self.puzzle[i][j] = '0'

    #Fills rows and columns with water if the constraint is satisfied
    def fill_row_col_water(self):
        for i, row_c_val in enumerate(self.row_constraints):
            if row_c_val == 0:
                for c in self.puzzle[i]:
                    if c == '0':
                        c = '.'
        for i, col_c_val in enumerate(self.col_constraints):
            if col_c_val == 0:
                for row in self.puzzle:
                    if row[i] == '0':
                        row[i] = '.'
        return

    def fill_cell_with_water(self, x, y):
        if x >= 0 and x < len(self.puzzle) and y >= 0 and y < len(self.puzzle):
            if self.puzzle[x][y] == '0':
                self.puzzle[x][y] = '.'
        return

    def surround_cell_with_water(self, x, y):
        adj = [-1, 0, 1]
        for i in adj:
            for j in adj:
                self.fill_cell_with_water(x + i, y + j)
        return

    def surround_ship_with_water(self, x, y):
        ship = self.puzzle[x][y]
        if ship == 'S':
            self.surround_cell_with_water(x, y)
        if ship == '<':
            while self.puzzle[x][y] != '>':
                self.surround_cell_with_water(x, y)
                y += 1
            self.surround_cell_with_water(x, y)
        if ship == '^':
            while self.puzzle[x][y] != 'v':
                self.surround_cell_with_water(x, y)
                x += 1
            self.surround_cell_with_water(x, y)
        return

    def recalculate_constraints(self, i, j, length, orientation):
        if length == 1:
            self.row_constraints[i] -= 1
            self.col_constraints[j] -= 1
            self.ships[0] -= 1
        if length > 1 and orientation == 'Horizontal':
            self.row_constraints[i] -= length
            for n in range(length):
                self.col_constraints[j+n] -= 1
            self.ships[length-1] -= 1
        if length > 1 and orientation == 'Vertical':
            for n in range(length):
                self.row_constraints[i+n] -= 1
            self.col_constraints[j] -= length
            self.ships[length-1] -= 1
        return

    # Completes ships in the initial map that can be completed
    def complete_initial_ships(self):
        for i, row in enumerate(self.puzzle):
            for j, val in enumerate(row):
                if val == 'S':
                    self.surround_ship_with_water(i, j)
                    self.recalculate_constraints(i, j, 1, 'S')
                if val == '<':
                    if j+1 < len(self.puzzle[i]) and self.puzzle[i][j+1] == '>':
                        self.surround_ship_with_water(i, j)
                        self.recalculate_constraints(i, j, 2, 'Horizontal')
                    if j+2 < len(self.puzzle[i]) and self.puzzle[i][j+2] == '>':
                        self.puzzle[i][j+1] = 'M'
                        self.surround_ship_with_water(i, j)
                        self.recalculate_constraints(i, j, 3, 'Horizontal')
                    if j+3 < len(self.puzzle[i]) and self.puzzle[i][j+3] == '>':
                        self.puzzle[i][j+1] = 'M'
                        self.puzzle[i][j+2] = 'M'
                        self.surround_ship_with_water(i, j)
                        self.recalculate_constraints(i, j, 4, 'Horizontal')
                if val == '^':
                    if i+1 < len(self.puzzle) and self.puzzle[i+1][j] == 'v':
                        self.surround_ship_with_water(i, j)
                        self.recalculate_constraints(i, j, 2, 'Vertical')
                    if i+2 < len(self.puzzle) and self.puzzle[i+2][j] == 'v':
                        self.puzzle[i+1][j] = 'M'
                        self.surround_ship_with_water(i, j)
                        self.recalculate_constraints(i, j, 3, 'Vertical')
                    if i+3 < len(self.puzzle) and self.puzzle[i+3][j] == 'v':
                        self.puzzle[i+1][j] = 'M'
                        self.puzzle[i+2][j] = 'M'
                        self.surround_ship_with_water(i, j)
                        self.recalculate_constraints(i, j, 4, 'Vertical')
        return

    def check_incomplete(self, x, y):
        puzzle = self.puzzle
        if puzzle[x][y] == '<':
            for i in range(1, 4):
                if y+i < len(puzzle[x]) and puzzle[x][y+i] == '>':
                    return False
        if puzzle[x][y] == '>':
            for i in range(1, 4):
                if y-i >= 0 and puzzle[x][y-i] == '<':
                    return False
        if puzzle[x][y] == '^':
            for i in range(1, 4):
                if x+i < len(puzzle) and puzzle[x+i][y] == 'v':
                    return False
        if puzzle[x][y] == 'v':
            for i in range(1, 4):
                if x-i >= 0 and puzzle[x-i][y] == '^':
                    return False
        return True

    def find_incomplete_ships(self):
        incomplete = []
        for i, row in enumerate(self.puzzle):
            for j, val in enumerate(row):
                if val in ['<', '>', '^', 'v'] and self.check_incomplete(i, j):
                    incomplete.append([i, j])
        return incomplete

    def complete_ship(self, x, y, length):
        if self.ships[length-1] > 0:
            piece = self.puzzle[x][y]
            if piece == '<' and y+length-1 < len(self.puzzle[x]) and self.puzzle[x][y+length-1] == '0':
                self.puzzle[x][y+length-1] = '>'
                for i in range(1, length-1):
                    self.puzzle[x][y+i] = 'M'
                self.surround_ship_with_water(x, y)
                self.recalculate_constraints(x, y, length, 'Horizontal')
            if piece == '>' and y-(length-1) >= 0 and self.puzzle[x][y-(length-1)] == '0':
                self.puzzle[x][y-(length-1)] = '<'
                for i in range(1, length-1):
                    self.puzzle[x][y-i] = 'M'
                self.surround_ship_with_water(x, y-(length-1))
                self.recalculate_constraints(
                    x, y-(length-1), length, 'Horizontal')
            if piece == '^' and x+length-1 < len(self.puzzle) and self.puzzle[x+length-1][y] == '0':
                self.puzzle[x+length-1][y] = 'v'
                for i in range(1, length-1):
                    self.puzzle[x+i][y] = 'M'
                self.surround_ship_with_water(x, y)
                self.recalculate_constraints(x, y, length, 'Vertical')
            if piece == 'v' and x-(length-1) >= 0 and self.puzzle[x-(length-1)][y] == '0':
                self.puzzle[x-(length-1)][y] = '^'
                for i in range(1, length-1):
                    self.puzzle[x-i][y] = 'M'
                self.surround_ship_with_water(x-(length-1), y)
                self.recalculate_constraints(
                    x-(length-1), y, length, 'Vertical')
            self.fill_row_col_water()
        return

    def can_place_piece(self, i, j, length, orientation):
        if self.puzzle[i][j] == '0' and orientation == "Horizontal":
            if j + length - 1 < len(self.puzzle[i]) and self.puzzle[i][j + length - 1] == '0':
                return True
        if self.puzzle[i][j] == '0' and orientation == "Vertical":
            if i + length - 1 < len(self.puzzle) and self.puzzle[i + length - 1][j] == '0':
                return True
        return False

    def place_piece(self, i, j, length, orientation):
        new_state = State(copy.deepcopy(self.row_constraints),
                          copy.deepcopy(self.col_constraints),
                          copy.deepcopy(self.ships),
                          copy.deepcopy(self.puzzle))
        if orientation == "Horizontal":
            new_state.puzzle[i][j] = '<'
            new_state.complete_ship(i, j, length)
        if orientation == "Vertical":
            new_state.puzzle[i][j] = '^'
            new_state.complete_ship(i, j, length)
        if length == 1:
            new_state.puzzle[i][j] = 'S'
            new_state.surround_ship_with_water(i, j)
            new_state.recalculate_constraints(i, j, 1, "S")
        return new_state

    def solve_puzzle(self, output, original):
        incomplete = self.find_incomplete_ships()
        if incomplete:
            for i in range(2, 5):
                new_state = State(copy.deepcopy(self.row_constraints),
                                  copy.deepcopy(self.col_constraints),
                                  copy.deepcopy(self.ships),
                                  copy.deepcopy(self.puzzle))
                new_state.complete_ship(incomplete[0][0], incomplete[0][1], i)
                if new_state.check_constraints():
                    new_state.solve_puzzle(output, original)
        elif self.ships[3] > 0:
            for i, row in enumerate(self.puzzle):
                for j, val in enumerate(row):
                    if self.can_place_piece(i, j, 4, "Horizontal"):
                        new_state = self.place_piece(i, j, 4, "Horizontal")
                        if new_state.check_constraints():
                            new_state.solve_puzzle(output, original)
                    if self.can_place_piece(i, j, 4, "Vertical"):
                        new_state = self.place_piece(i, j, 4, "Vertical")
                        if new_state.check_constraints():
                            new_state.solve_puzzle(output, original)
        elif self.ships[2] > 0:
            for i, row in enumerate(self.puzzle):
                for j, val in enumerate(row):
                    if self.can_place_piece(i, j, 3, "Horizontal"):
                        new_state = self.place_piece(i, j, 3, "Horizontal")
                        if new_state.check_constraints():
                            new_state.solve_puzzle(output, original)
                    if self.can_place_piece(i, j, 3, "Vertical"):
                        new_state = self.place_piece(i, j, 3, "Vertical")
                        if new_state.check_constraints():
                            new_state.solve_puzzle(output, original)
        elif self.ships[1] > 0:
            for i, row in enumerate(self.puzzle):
                for j, val in enumerate(row):
                    if self.can_place_piece(i, j, 2, "Horizontal"):
                        new_state = self.place_piece(i, j, 2, "Horizontal")
                        if new_state.check_constraints():
                            new_state.solve_puzzle(output, original)
                    if self.can_place_piece(i, j, 2, "Vertical"):
                        new_state = self.place_piece(i, j, 2, "Vertical")
                        if new_state.check_constraints():
                            new_state.solve_puzzle(output, original)
        elif self.ships[0] > 0:
            for i, row in enumerate(self.puzzle):
                for j, val in enumerate(row):
                    if self.puzzle[i][j] == '0':
                        new_state = self.place_piece(i, j, 1, "S")
                        if new_state.check_constraints():
                            new_state.solve_puzzle(output, original)
        if check_solution(self.row_constraints, self.col_constraints, self.ships, self.puzzle, original):
            # self.display()
            for l in self.original:
                print(l)
            print_to_file(args.outputfile, self.puzzle)
            quit()
            return self.puzzle
        return


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzles."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    args = parser.parse_args()

    initial_params = read_from_file(args.inputfile)
    row_constraints = [eval(i) for i in initial_params[0]]
    col_constraints = [eval(i) for i in initial_params[1]]
    ship_constraints = [eval(i) for i in initial_params[2]]
    puzzle = initial_params[3]
    original = copy.deepcopy(puzzle)

    start = State(row_constraints, col_constraints, ship_constraints, puzzle)
    start.remove_connectors()
    start.complete_initial_ships()
    start.fill_row_col_water()
    start.solve_puzzle(args.outputfile, original)

    # print_to_file(args.outputfile, start.puzzle)
