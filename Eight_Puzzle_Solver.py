#eight_puzzle.py is like the main file that runs the User's Interface
#it calls both general_search as well as puzzle class
#is uses regular expression hence the import of re
#the user's interface follows the example from the PDF prompt provided to us

import re
import General_Search_Puzzle
import Create_Puzzle

# default puzzle
default = Create_Puzzle.Puzzle([1, 2, 3, 4, 0, 6, 7, 5, 8])
                        #This default puzzle can be found in the PDF File


#answer is automatically generated
answer = []
for i in range(1, Create_Puzzle.Size_of_Puzzle, 1):
    answer.append(i)
answer.append(0)
custom_puzzle = []


# the following are helper functions for a text-based UI
# Create_Puzzle_To_Solve receives input from the user to make a customized 8-puzzle, no error checking is currently in place
def Create_Puzzle_To_Solve():
    print "    Enter your own custom 8 Puzzle, remember 0 represent the space."
    get = raw_input('    Give numbers for the first row, remember to space or tab between each number ')
    temp = map(int, re.split(', | ', get))
    for num in temp:
            custom_puzzle.append(num)

    get = raw_input('    Give numbers for the second row, remember to space or tab between each number ')
    temp = map(int, re.split(', | ', get))
    for num in temp:
            custom_puzzle.append(num)
    get = raw_input('    Give numbers for the third row, remember to space or tab between each number ')
    temp = map(int, re.split(', | ', get))
    for num in temp:
            custom_puzzle.append(num)
    return Create_Puzzle.Puzzle(custom_puzzle)


# Choose_Puzzle gets a default or user-entered puzzle from the user
def Choose_Puzzle():
    print "Type \"1\" to use a default puzzle, or \"2\" to enter your own puzzle."
    y = input()
    if y == 1:
        return default
    elif y == 2:
        return Create_Puzzle_To_Solve()
    else:
        print "incorrect input"
        return Choose_Puzzle()


# Search_Algorithms will choose the appropriate search algorithm from the user's input.
# 1 will be for Uniform Cost Search
# 2 will be hueristic searching
# 3 will be the manhattan distance
def Search_Algorithms(thePuzzle):
    print "     Please choose one to execute: "
    print "         1. Uniform Cost Search"
    print "         2. A* with the Misplaced Tile heuristic."
    print "         3. A* with the Manhattan distance heuristic.\n"
    option = input('         ')
    if not  Create_Puzzle.checkSolvable(thePuzzle.INITIAL_STATE.STATE):
        print "The puzzle provided cannot be solved."
        exit(0)
    if not(option > 3) and not(option < 1):
        return General_Search_Puzzle.search(thePuzzle, option)
    else:
        print "Wrong input!"
        return Search_Algorithms()



# This part mirrors the output found on the PDF Assignment
# The way everything prints is exactly or closely related to how the
# sample printing looks like, on the PDF Assignment page
print "Welcome to John Phang's 8-puzzle solver."
thePuzzle = Choose_Puzzle()
print "Here is the chosen puzzle: "

General_Search_Puzzle.Print_Puzzle(thePuzzle.INITIAL_STATE)
result, total, maxSize = Search_Algorithms(thePuzzle)
if result is 0:
    print "Bug found in this puzzle"
else:
    print "\n\nGoal!!"
    print "\nTo solve this problem the search algorithm expanded a total number of %d nodes." % total
    print "The maximum number of nodes in the queue at any one time was %i" % maxSize
    print "The depth of the goal node was %d" % result.DEPTH

x = raw_input(' Print Trace? ')
if x:
    if x[0]=='y' or x[0]=='Y':
        trace = []
        trace.append(result)
        node = result.PARENT
        while node.PARENT is not None:
            trace.append(node)
            node = node.PARENT
        trace.append(node)
        trace.reverse()
        for node in trace[:len(trace)-1]:
            print "Expanding node with g(n) = %d and h(n) = %d" % (node.DEPTH, node.MANHATTAN)
            General_Search_Puzzle.Print_Puzzle(node.STATE)
            print 'Expanding this node...'
        General_Search_Puzzle.Print_Puzzle(trace[len(trace)-1].STATE)
        print "\n\nGoal!!"
        print "\nTo solve this problem the search algorithm expanded a total number of %d nodes." % total
        print "The maximum number of nodes in the queue at any one time was %i" % maxSize
        print "The depth of the goal node was %d" % result.DEPTH

print '   Finish'