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

        # helper method to add horizontal line
        def add_line(grid):
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

    # TODO
    # implement __eq__, __str__ methods
    # __repr__ is up to you

    def extensions(self):

        grid = self._marker
        extensions = []

        for row in range(len(grid)):

            for column in range(len(grid[row])):

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

        grid = self._marker

        count = 0

        for row in range(len(grid)):

            for column in range(len(grid[row])):

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
