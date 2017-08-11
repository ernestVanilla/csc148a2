"""
Some functions for working with puzzles
"""
from puzzle import Puzzle
from collections import deque
# set higher recursion limit
# which is needed in PuzzleNode.__str__
#import resource
import sys
#resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
sys.setrecursionlimit(10**6)


# TODO
# implement depth_first_solve
# do NOT change the type contract
# you are welcome to create any helper functions
# you like
def depth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent. Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode
    """
    root = puzzle.parent
    
    children = puzzle.extention
    
    #Creating a stack using a deque; putting the root as the first element in the stack
    stack = deque([PuzzleNode(puzzle, [])])
    
    tracker = set()   
    
    # while loop is use to 
    while len(stack) > 0:
        
        new_node = stack.popleft()
        
        for n in new_node.puzzle.extention():
            
            node_child = PuzzleNode(n)
            
            if node_child.puzzle.is_solved():
                
                return node_child

# TODO
# implement breadth_first_solve
# do NOT change the type contract
# you are welcome to create any helper functions
# you like
# Hint: you may find a queue useful, that's why
# we imported deque
def breadth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode
    """
    # instantiating queue using new PuzzleNode (root)
    queue = deque([PuzzleNode(puzzle, [])])

    # while puzzle still has moves to make (or is not solved yet)
    while len(queue) > 0:

        current = queue.popleft() # update current node
        extensions = current.puzzle.extensions() # gather moves to make

        # loop through extensions (breadth)
        for i in range(len(extensions)):
            newNode = PuzzleNode(extensions[i], [], current)

            # do not include already traversed nodes
            if newNode not in queue:
                current.children.append(newNode) # add as child of current node
                queue.append(newNode) # add to queue

                # if child node is solved, return it
                if newNode.puzzle.is_solved():
                    return newNode


    return None # no solution was found



# Class PuzzleNode helps build trees of PuzzleNodes that have
# an arbitrary number of children, and a parent.
class PuzzleNode:
    """
    A Puzzle configuration that refers to other configurations that it
    can be extended to.
    """

    def __init__(self, puzzle=None, children=None, parent=None):
        """
        Create a new puzzle node self with configuration puzzle.

        @type self: PuzzleNode
        @type puzzle: Puzzle | None
        @type children: list[PuzzleNode]
        @type parent: PuzzleNode | None
        @rtype: None
        """
        self.puzzle, self.parent = puzzle, parent
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other):
        """
        Return whether Puzzle self is equivalent to other

        @type self: PuzzleNode
        @type other: PuzzleNode | Any
        @rtype: bool

        >>> from word_ladder_puzzle import WordLadderPuzzle
        >>> pn1 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "no", "oo"}))
        >>> pn2 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "oo", "no"}))
        >>> pn3 = PuzzleNode(WordLadderPuzzle("no", "on", {"on", "no", "oo"}))
        >>> pn1.__eq__(pn2)
        True
        >>> pn1.__eq__(pn3)
        False
        """
        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self):
        """
        Return a human-readable string representing PuzzleNode self.

        # doctest not feasible.
        """
        return "{}\n\n{}".format(self.puzzle,
                                 "\n".join([str(x) for x in self.children]))
