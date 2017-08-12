from puzzle import Puzzle
import copy


class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved,
    unsolved, or even unsolvable.
    """

    def __init__(self, marker, marker_set):
        """
        Create a new GridPegSolitairePuzzle self with
        marker indicating pegs, spaces, and unused
        and marker_set indicating allowed markers.

        @type marker: list[list[str]]
        @type marker_set: set[str]
                          "#" for unused, "*" for peg, "." for empty
        """
        assert isinstance(marker, list)
        assert len(marker) > 0
        assert all([len(x) == len(marker[0]) for x in marker[1:]])
        assert all([all(x in marker_set for x in row) for row in marker])
        assert all([x == "*" or x == "." or x == "#" for x in marker_set])
        self._marker, self._marker_set = marker, marker_set

    
    def __eq__(self, other):
        return (self._marker == other._marker)


    def __str__(self):
        grid = self._marker
        s = ''

        def add_line(grid):
            
            '''(list[list[str]]) -> str
            
            This method adds horizontal lines to help
            with the visual representation.
            
            >>> grid = [["*", "*", "*", "*", "*"],
                ["*", "*", "*", "*", "*"],
                ["*", "*", "*", "*", "*"],
                ["*", "*", ".", "*", "*"],
                ["*", "*", "*", "*", "*"]]
            
            >>> gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
                
            >>> print(gpsp)
                
            >>> -------------
                | * * * * * |
                | * * * * * |
                | * * * * * |
                | * * . * * |
                | * * * * * |
                -------------
                    
                
            >>> grid = [["*", "*", "*", "*", "*"],
                    ["*", "*", "*", "*", "*"],
                    ["*", "*", "*", ".", "*"],
                    ["*", ".", "*", "*", "*"],
                    ["*", "*", "*", "*", "*"]]
        
            >>> gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
                
            >>> print(gpsp)
                
            >>> -------------
                | * * * * * |
                | * * * * * |
                | * * * . * |
                | * . * * * |
                | * * * * * |
                -------------

            '''
            string = ''
            for i in range(len(grid[0])*2 + 3): # accounts for space alignment
                string += '-'
            string += '\n'
            return string

        s += add_line(grid)
        for y in range(len(grid)):
            s += '|'
            for x in range(len(grid[y])):
                s += ' '
                s += grid[y][x]
            s += ' |\n'
        s += add_line(grid)
        return s


    def extensions(self):
        
        '''(list[Puzzle]) -> list[Puzzle Objects]
        
        This function returns a list of the possible 
        solutions for Peg Solitaire puzzle.
        
        
    >>> grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]
            
    >>> gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    
    >>> gpsp.extensions()
    
    >>> [<__main__.GridPegSolitairePuzzle object at 0x01CE1C70>, <__main__.GridPegSolitairePuzzle object at 0x01CE1AB0>, <__main__.GridPegSolitairePuzzle   object at 0x01CE1950>]
    
    
    >>> grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", ".", "*"],
            ["*", ".", "*", "*", "*"],
            ["*", "*", "*", "*", "*"]]
            
    >>> gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    
    >>> gpsp.extensions()
    
    >>> [<__main__.GridPegSolitairePuzzle object at 0x01CE1A50>, <__main__.GridPegSolitairePuzzle object at 0x01CE1910>, <__main__.GridPegSolitairePuzzle object at 0x01CE17D0>, <__main__.GridPegSolitairePuzzle object at 0x019E5D10>, <__main__.GridPegSolitairePuzzle object at 0x01CE19B0>]
        '''

        grid = self._marker
        extensions = []

        for row in range(len(grid)):

            for column in range(len(grid[row])):

                # Checking the indexs of each row + column if there is a existing peg
                if grid[row][column] == "*":

                    # Check for top if inbounds & if the item directly above it is a peg
                    if (row - 2) > 0 and grid[row - 1][column] == "*":

                        if grid[row - 2][column] ==".":

                            dup = copy.deepcopy(grid)

                            dup[row - 2][column] = "*"
                            dup[row - 1][column] = "."
                            dup[row][column] = "."
                            extension = GridPegSolitairePuzzle(dup, self._marker_set)
                            extensions.append(extension)
                            dup = None


                    # Check for bottom if inbounds & if the item directly below it is a peg
                    if (row + 2) < (len(grid)) and grid[row + 1][column] == "*":

                        if grid[row + 2][column] == ".":

                            dup = copy.deepcopy(grid)

                            dup[row + 2][column] = "*"
                            dup[row + 1][column] = "."
                            dup[row][column] = "."
                            extension = GridPegSolitairePuzzle(dup, self._marker_set)
                            extensions.append(extension)
                            dup = None


                    # Check for left if inbounds & if the item directly beside it is a peg
                    if (column - 2) > 0 and grid[row][column - 1] == "*":

                        if grid[row][column - 2] == ".":

                            dup = copy.deepcopy(grid)

                            dup[row][column - 2] = "*"
                            dup[row][column - 1] = "."
                            dup[row][column] = "."
                            extension = GridPegSolitairePuzzle(dup, self._marker_set)
                            extensions.append(extension)
                            dup = None


                    # Check for right if inbounds & if the item directly beside it is a peg
                    if (column + 2) < (len(grid[row])) and grid[row][column + 1] == "*":

                        if grid[row][column + 2] == ".":

                            dup = copy.deepcopy(grid)

                            dup[row][column + 2] = "*"
                            dup[row][column + 1] = "."
                            dup[row][column] = "."
                            extension = GridPegSolitairePuzzle(dup, self._marker_set)
                            extensions.append(extension)
                            dup = None

        return extensions


    def is_solved(self):
        
        ''' (Puzzle) -> Bool
        
        The purpose of this function is to check
        whether there exist at most 1 peg remaining
        on the grid; if the condition holds then the
        player has won the game.
        
    >>> grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]
    
    >>> gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    
    >>> gpsp.is_solved()
        False
     
     
    >>> grid = [[".", ".", ".", ".", "."], 
            [".", ".", "*", ".", "."], 
            [".", ".", ".", ".", "."], 
            [".", ".", ".", ".", "."], 
            [".", ".", ".", ".", "."]]  
            
    >>> gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    
    >>> gpsp.is_solved()
        True
        '''

        grid = self._marker

        count = 0
        
        # Nested loop to traverse across the grid indexes
        for row in range(len(grid)):

            for column in range(len(grid[row])):
                
                # Checks for any remaining pegs on the grid
                if grid[row][column] == "*":

                    count = count + 1

        if count == 1:
            return True
        else:
            return False


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    from puzzle_tools import depth_first_solve

    grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]
    gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    import time

    start = time.time()
    solution = depth_first_solve(gpsp)
    end = time.time()
    print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    print("Using depth-first: \n{}".format(solution))
