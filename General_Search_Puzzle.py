#This general_search.py is the most important part of the code
#In this file it has all 3 algorithms
#I use a heap for priority queuing
from heapq import heappop, heappush
import Create_Puzzle

#From the prompt you can deduce that if your puzzle is of size 15 or 25

if Create_Puzzle.Size_of_Puzzle == 9:

    diameter = 31

elif Create_Puzzle.Size_of_Puzzle == 15:

    diameter = 80

elif Create_Puzzle.Size_of_Puzzle == 25:

    diameter = 208

else:
    diameter = float('inf')

MAXSIZE_QUEUE = 0
TOTAL_NODES_EXPANDED = 0

#This is a helper function that prints each current state of the puzzle
def Print_Puzzle(state):
    j = 0
    for i in range(0, Create_Puzzle.edges_of_puzzle):
        print '      ',
        while j < Create_Puzzle.edges_of_puzzle:
            print state[j + Create_Puzzle.edges_of_puzzle * i],
            j += 1
        print ""
        j = 0


# expoand the node for you
# when it is expanding it is expanding the current node that it is on
#while operator is choosing the move on that current node
def expand(node, calculate):
    children = []
    zero_position = node.STATE.index(0)       #index of the blank tile aka the 0 tile that represents the blank tile
    for oper in calculate:
        child = oper(node, zero_position)    #will find the position of the child otherwise if it is not a child then an error will occur
        if child:
            children.append(child)
    return children


# Search function describe in the PDF prompt
def search(problem, function):
    #Global variables
    global diameter
    global TOTAL_NODES_EXPANDED
    global MAXSIZE_QUEUE

    # This is to check to see if you entered a solved puzzle already
    # Basically an error check.
    if problem.GOAL_TEST(problem.INITIAL_STATE.STATE):
        print "\n\nPuzzle have already been solved"

        return problem.INITIAL_STATE, TOTAL_NODES_EXPANDED, MAXSIZE_QUEUE

    nodes = []
    closed = {}
    heappush(nodes, [float('inf'), problem.INITIAL_STATE])


    while True:
        if not nodes: #when there is no solution
            return 0, 0, 0
        MAXSIZE_QUEUE = max(MAXSIZE_QUEUE, nodes.__len__())
        cost, node = heappop(nodes) # pop the highest priority because it is the least costly
        closed[tuple(node.STATE)] = True #if true it will close

        #The print is similar to the one found in the PDF of the individual assignment
        if function is 1:

            print "The best state to expand with a g(n) = %d and h(n) = %d is..." % (node.DEPTH, 0)

        elif function is 2:

            print "The best state to expand with a g(n) = %d and h(n) = %d is..." % (node.DEPTH, node.mis())

        else:

            print "The best state to expand with a g(n) = %d and h(n) = %d is..." % (node.DEPTH, node.man())

        Print_Puzzle(node.STATE)
        print '     Expanding this node...'

        # Check the state that we are moving on next to
        # in order to see if need expanding or not
        # We then push it to the priority queue
        # by the given heurisitic function aka the queue
        for child in expand(node, problem.OPERATORS):

            if tuple(child.STATE) not in closed:

                if child.DEPTH <= diameter:

                    if function is 1:

                        heappush(nodes, [child.DEPTH, child])

                    elif function is 2:

                        heappush(nodes, [child.DEPTH + child.mis(), child])

                    else:
                        heappush(nodes, [child.DEPTH + child.man(), child])

                    TOTAL_NODES_EXPANDED += 1

                    #Error check to not expand anymore unnecessary node
            if problem.GOAL_TEST(child.STATE):
                return child, TOTAL_NODES_EXPANDED, MAXSIZE_QUEUE