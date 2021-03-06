from puzzle import Puzzle


class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like the 15-puzzle, which may be solved, unsolved,
    or even unsolvable.
    """

    def __init__(self, from_grid, to_grid):
        """
        MNPuzzle in state from_grid, working towards
        state to_grid

        @param MNPuzzle self: this MNPuzzle
        @param tuple[tuple[str]] from_grid: current configuration
        @param tuple[tuple[str]] to_grid: solution configuration
        @rtype: None
        """
        # represent grid symbols with letters or numerals
        # represent the empty space with a "*"
        assert len(from_grid) > 0
        assert all([len(r) == len(from_grid[0]) for r in from_grid])
        assert all([len(r) == len(to_grid[0]) for r in to_grid])
        self.n, self.m = len(from_grid), len(from_grid[0])
        self.from_grid, self.to_grid = from_grid, to_grid


    def __eq__(self, other):
        sameFrom = self.from_grid == other.from_grid
        sameTo = self.to_grid == other.to_grid
        return sameFrom and sameTo


    def __str__(self):
        
        grid = self.from_grid
        s = ''

        def add_line(grid):
            
            '''[tuple[tuple[str]]] -> str
            
            This method adds horizontal lines to help
            with the visual representation.
            
            >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
            
            >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
            
            >>> solution = MNPuzzle(start_grid, target_grid)
            
            >>> print(solution)
            
            >>> ---------
                | * 2 3 |
                | 1 4 5 |
                ---------
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
        
        '''[tuple[tuple[str]] -> list[Puzzle Objects]
        
        This function returns the legal possible moves
        the puzzle can make.
        
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        
        >>> solution = MNPuzzle(start_grid, target_grid)
        
        >>> solution.extensions()
        
        >>> [<__main__.MNPuzzle object at 0x01CE1D50>, <__main__.MNPuzzle object at 0x01CE1AF0>]
        '''

        grid = self.from_grid
        extensions = []

        def rebuildGrid(grid, spaceX, spaceY, tileX, tileY):
            
            '''[tuple[tuple[str]] -> list[Puzzle Objects]
            
            This helper function creates the extension.
            '''
            
            tile = grid[tileY][tileX] # keeps track of tile value
            
            newGrid = (())

            for row in range(len(grid)):
                
                newRow = []

                # switches the tile and space values
                # append the same value otherwise
                for col in range(len(grid[row])):
                    if row == tileY and col == tileX:
                        newRow.append("*")
                    elif row == spaceY and col == spaceX:
                        newRow.append(tile)
                    else:
                        sameSymbol = grid[row][col]
                        newRow.append(sameSymbol)

                tupleRow = tuple([tuple(newRow)])
                newGrid += tupleRow

            return newGrid

        # finds empty space
        if any("*" in row for row in grid):

            y = 0 # row with empty position
            while "*" not in grid[y]:
                y += 1
            x = grid[y].index("*") # column with empty position

            # create new MNPuzzle object for each extension generated
            # LEFT (slide right)
            if (x-1) > 0:
                newGrid = rebuildGrid(grid, x, y, x-1, y)
                extension = MNPuzzle(newGrid, self.to_grid)
                extensions.append(extension)

            # RIGHT (slide left)
            if (x+1) < len(grid[y]):
                newGrid = rebuildGrid(grid, x, y, x+1, y)
                extension = MNPuzzle(newGrid, self.to_grid)
                extensions.append(extension)

            # UP (slide down)
            if (y-1) > 0:
                newGrid = rebuildGrid(grid, x, y, x, y-1)
                extension = MNPuzzle(newGrid, self.to_grid)
                extensions.append(extension)

            # DOWN (slide up)
            if (y+1) < len(grid):
                newGrid = rebuildGrid(grid, x, y, x, y+1)
                extension = MNPuzzle(newGrid, self.to_grid)
                extensions.append(extension)

        return extensions


    def is_solved(self):
        
        '''[tuple[tuple[str]] -> Bool
        
        This function checks whether the
        puzzle is in the solved state
        or not.
        
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        
        >>> solution = MNPuzzle(start_grid, target_grid)
        
        >>> solution.is_solved()
            False
        '''
        return self.from_grid == self.to_grid
'''
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    target_grid = (("1", "2", "3"), ("4", "5", "*"))
    start_grid = (("*", "2", "3"), ("1", "4", "5"))
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print("BFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
    start = time()   
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    current = solution
    while current:
        print(current)
        current = current.parent    
    end = time()
    print("DFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
        '''