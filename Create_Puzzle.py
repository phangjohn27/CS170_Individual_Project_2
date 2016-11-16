#puzzle.py pretty much maintain the puzzle logic
# Because of our general_search we are able to expand this puzzle.py so that it works
# for puzzle as large as 15 and 25
from math import sqrt

#if you want to change the puzzle
#for example if you want to change the puzzle to 15 you would change the Size_of_Puzzle = 9 to 15 or 25
Size_of_Puzzle = 9
edges_of_puzzle = int(sqrt(Size_of_Puzzle))

#The Answers here will update once you give it a Size_of_Puzzle for the puzzle
Answers = []
for i in range(1, Size_of_Puzzle, 1):
    Answers.append(i)
Answers.append(0)
def swap(self, x, y):
    self[x], self[y] = self[y], self[x]


# A group member pointed me in the direction of having a check solvable function
# What this does is an error checking function that basically check to see if
# A puzzle can be solved or not
# My group member directed me to this webpage that explains how the check solvability would work
# https://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html
def checkSolvable(puzzle):
    inversions = 0
    check = list(puzzle)
    check.remove(0)
    for i in range(0, check.__len__(), 1):
        for j in range(i, check.__len__(), 1):
            if check[i] > check[j]:
                inversions += 1
    if edges_of_puzzle % 2 == 1:
        return not(inversions % 2)
    else:
        zeropositionition = puzzle.index(0)
        for i in range(0, edges_of_puzzle*edges_of_puzzle, edges_of_puzzle*2):
            for j in range(0, edges_of_puzzle, 1):
                if zeropositionition == i+j:
                    return inversions % 2
        else:
            return not(inversions % 2)


def misplaced(state):
    num = 0
    for i in range(0, Size_of_Puzzle, 1):
        if state[i] is 0:
            continue
        if state[i] != Answers[i]:
            num += 1
    return num


#Manhattan Distance to solve Puzzle
def manhattan(state):
    manhattan_distance = 0
    for i in range(1, Size_of_Puzzle, 1):
        Values = state.index(i)
        manhattan_answer = Answers.index(i)
        if Values == manhattan_answer:
            continue
        #for each else branch below, first the vertical displacement is checked
        # then the horizontal displacement is found
        elif Values in range(0, edges_of_puzzle, 1):

            if manhattan_answer in range(0, edges_of_puzzle, 1):

                manhattan_distance += abs(Values - manhattan_answer)

            elif manhattan_answer in range(edges_of_puzzle, edges_of_puzzle*2, 1):

                Values += edges_of_puzzle

                manhattan_distance += abs(Values - manhattan_answer) + 1

            else:
                Values += edges_of_puzzle*2

                manhattan_distance += abs(Values - manhattan_answer) + 2

        elif Values in range(edges_of_puzzle, edges_of_puzzle*2, 1):

            if manhattan_answer in range(edges_of_puzzle, edges_of_puzzle*2, 1):

                manhattan_distance += abs(Values - manhattan_answer)

            elif manhattan_answer in range(0, edges_of_puzzle, 1):

                Values -= edges_of_puzzle

                manhattan_distance += abs(Values - manhattan_answer) + 1

            else:

                Values += edges_of_puzzle

                manhattan_distance += abs(Values - manhattan_answer) + 1

        elif Values in range(edges_of_puzzle*2, edges_of_puzzle*3, 1):

            if manhattan_answer in range(edges_of_puzzle*2, edges_of_puzzle*3, 1):

                manhattan_distance += abs(Values - manhattan_answer)

            elif manhattan_answer in range(manhattan_answer, edges_of_puzzle*2, 1):

                Values -= edges_of_puzzle

                manhattan_distance += abs(Values - manhattan_answer) + 1

            else:

                Values -= edges_of_puzzle*2

                manhattan_distance += abs(Values - manhattan_answer) + 2

    return manhattan_distance


# Class node represent the state of the puzzle previous, current, and eventually the goal
#  contain heurisitc and current depth from the root node
class node:
    def __init__(self, state, parent=None):
        self.STATE = state
        self.MISPLACED = None
        self.MANHATTAN = None

        if parent is None:
            self.PARENT = None
            self.DEPTH = 0
        else:
            self.STATE = state
            self.PARENT = parent #list
            self.DEPTH = self.PARENT.DEPTH+1

    def __getitem__(self, item):
        return self.STATE[item]

    def mis(self):
        if self.MISPLACED is None:
            self.MISPLACED = misplaced(self.STATE)
        return self.MISPLACED

    def man(self):
        if self.MANHATTAN is None:
            self.MANHATTAN = manhattan(self.STATE)
        return self.MANHATTAN

    def __index__(self, item):
        return self.STATE.index(item)

    def swap(self, x, y):
        self.STATE[x], self.STATE[y] = self.STATE[y], self.STATE[x]


#Each function represent a move you can make in the Puzzle game
#depending on the next move it will move at that certain spot
def move_left(state, position):
    if position in range(0, edges_of_puzzle*(edges_of_puzzle-1)+1, edges_of_puzzle):
        return 0
    else:
        child = node(list(state), state)
        child.swap(position, position-1)
        return child


def move_right(state, position):

    if position in range(edges_of_puzzle-1, edges_of_puzzle*edges_of_puzzle, edges_of_puzzle):

        return 0

    else:

        child = node(list(state), state)

        child.swap(position, position+1)

        return child


def move_up(state, position):

    if position in range(0, edges_of_puzzle, 1):

        return 0

    else:

        child = node(list(state), state)

        child.swap(position, position-edges_of_puzzle)

        return child


def move_down(state, position):

    if position in range(edges_of_puzzle*(edges_of_puzzle-1), edges_of_puzzle*edges_of_puzzle, 1):

        return 0

    else:

        child = node(list(state), state)

        child.swap(position, position+edges_of_puzzle)

        return child



def Check_Goal_State(state):

    if state == Answers:

        return 1

    else:

        return 0


# the structure of the puzzle: the root node, legal operators, and goal are all defined to define our problem scope
class Puzzle:
    def __init__(self, initialState):
        self.INITIAL_STATE = node(initialState)
        self.OPERATORS = [move_left, move_right, move_up, move_down]
        self.GOAL_TEST = Check_Goal_State