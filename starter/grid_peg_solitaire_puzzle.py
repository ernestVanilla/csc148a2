from puzzle import Puzzle


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
        return (self.marker == other.marker)
    
    def __str__(self):
        pass

    # TODO
    # implement __eq__, __str__ methods
    # __repr__ is up to you
    
    def extentions(self):
        
        grid = self.marker_set
        
        for row in range(len(grid)):
            
            for column in range(len(grid[row])):
                
                if grid[row][column] == "*":
                    
                    # Check for top if inbounds & if the item directly above it is a peg
                    if grid[row - 2][column] > 0 and grid[row - 1][column] == "*":
                        
                        if grid[row - 2][column] ==".":
                            
                            grid[row - 2][column] = "*"
                            grid[row - 1][column] = "."
                            grid[row][column] = "."
                    
                    # Check for bottom if inbounds & if the item directly below it is a peg
                    if grid[row + 2][column] < len(grid) and grid[row + 1][column] == "*":
                        
                        if grid[row + 2][column] == ".":
                            
                            grid[row + 2][column] = "*"
                            grid[row + 1][column] = "."
                            grid[row][column] = "."
                            
                    # Check for left if inbounds & if the item directly beside it is a peg
                    if grid[row][column - 2] > 0 and grid[row][column - 1] == "*":
                        
                        if grid[row][column - 2] == ".":
                            
                            grid[row][column - 2] = "*"
                            grid[row][column - 1] = "."
                            grid[row][column] = "."
                            
                    # Check for right if inbounds & if the item directly beside it is a peg
                    if grid[row][column + 2] < len(grid[row]) and grid[row][column + 1] == "*":
                        
                        if grid[row][column + 2] == ".":
                            
                            grid[row][column + 2] = "*"
                            grid[row][column + 1] = "."
                            grid[row][column] == "."
                            
    def is_solved(self):
        pass

    # TODO
    # override is_solved
    # A configuration is solved when there is exactly one "*" left


#if __name__ == "__main__":
    #import doctest

    #doctest.testmod()
    #from puzzle_tools import depth_first_solve

    #grid = [["*", "*", "*", "*", "*"],
            #["*", "*", "*", "*", "*"],
            #["*", "*", "*", "*", "*"],
            #["*", "*", ".", "*", "*"],
            #["*", "*", "*", "*", "*"]]
    #gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    #import time

    #start = time.time()
    #solution = depth_first_solve(gpsp)
    #end = time.time()
    #print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    #print("Using depth-first: \n{}".format(solution))
