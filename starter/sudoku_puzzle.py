from puzzle import Puzzle


class SudokuPuzzle(Puzzle):
    """
    A sudoku puzzle that may be solved, unsolved, or even unsolvable.
    """

    def __init__(self, n, symbols, symbol_set):
        """
        Create a new nxn SudokuPuzzle self with symbols
        from symbol_set already selected.

        @type self: SudokuPuzzle
        @type n: int
        @type symbols: list[list of str]
        @type symbol_set: set[str]
        """

        assert n > 0
        assert round(n ** (1 / 2)) * round(n ** (1 / 2)) == n
        for i in range(len(symbols)):
            assert all([d in (symbol_set | {"*"}) for d in symbols[i]])
        assert len(symbol_set) == n
        assert (len(symbols) * len(symbols[0])) == n ** 2
        assert all([len(symbols[i]) == n for i in range(len(symbols))])
        
        self._n, self._symbols, self._symbol_set = n, symbols, symbol_set

    def __eq__(self, other):
        """
        Return whether SudokuPuzzle self is equivalent to other.

        @type self: SudokuPuzzle
        @type other: SudokuPuzzle | Any
        @rtype: bool

        >>> r1 = ["A", "B", "C", "D"]
        >>> r2 = ["D", "C", "B", "A"]
        >>> r3 = ["*", "D", "*", "*"]
        >>> r4 = ["*", "*", "*", "*"]
        >>> s1 = SudokuPuzzle(4, [r1, r2, r3, r4], {"A", "B", "C", "D"})
        >>> r1_2 = ["A", "B", "C", "D"]
        >>> r2_2 = ["D", "C", "B", "A"]
        >>> r3_2 = ["*", "D", "*", "*"]
        >>> r4_2 = ["*", "*", "*", "*"]
        >>> s2 = SudokuPuzzle(4, [r1_2, r2_2, r3_2, r4_2], {"A", "B", "C", "D"})
        >>> s1.__eq__(s2)
        True
        >>> r1_3 = ["A", "B", "C", "D"]
        >>> r2_3 = ["D", "C", "B", "A"]
        >>> r3_3 = ["*", "D", "*", "*"]
        >>> r4_3 = ["*", "A", "*", "*"]
        >>> s3 = SudokuPuzzle(4, [r1_3, r2_3, r3_3, r4_3], {"A", "B", "C", "D"})
        >>> s1.__eq__(s3)
        False
        """
        return (type(other) == type(self) and
                self._n == other._n and self._symbols == other._symbols and
                self._symbol_set == other._symbol_set)

    def __str__(self):
        """
        Return a human-readable string representation of SudokuPuzzle self.

        >>> r1 = ["A", "B", "C", "D"]
        >>> r2 = ["D", "C", "B", "A"]
        >>> r3 = ["*", "D", "*", "*"]
        >>> r4 = ["*", "*", "*", "*"]
        >>> s = SudokuPuzzle(4, [r1, r2, r3, r4], {"A", "B", "C", "D"})
        >>> print(s)
        AB|CD
        DC|BA
        -----
        *D|**
        **|**
        """

        def row_pickets(row):
            """
            Return string of characters in row with | divider
            between groups of sqrt(n)

            @type row: list[str]
            @rtype: str
            """
            string_list = []
            r = round(self._n ** (1 / 2))
            for i in range(self._n):
                if i > 0 and i % r == 0:
                    string_list.append("|")
                string_list.append(row[i])
            return "".join(string_list)

        s = ''
        num = round(self._n ** (1 / 2))
        div = "-" * (self._n + 1) + "\n"
        for i in range(len(self._symbols)):
            if i > 0 and i % num == 0:
                s += div
            s += row_pickets(self._symbols[i])
            s += "\n"
        return s.rstrip()

    def is_solved(self):
        """
        Return whether SudokuPuzzle self is solved.

        @type self: SudokuPuzzle
        @rtype: bool

        >>> r1 = ["A", "B", "C", "D"]
        >>> r2 = ["C", "D", "A", "B"]
        >>> r3 = ["B", "A", "D", "C"]
        >>> r4 = ["D", "C", "B", "A"]
        >>> grid = [r1, r2, r3, r4]
        >>> s = SudokuPuzzle(4, grid, {"A", "B", "C", "D"})
        >>> s.is_solved()
        True
        >>> r3[1] = "D"
        >>> r3[2] = "A"
        >>> grid = [r1, r2, r3, r4]
        >>> s = SudokuPuzzle(4, grid, {"A", "B", "C", "D"})
        >>> s.is_solved()
        False
        """
        # convenient names
        n, symbols = self._n, self._symbols
        # no "*" left and all rows, column, subsquares have correct symbols
        return (not any("*" in row for row in symbols)) \
               and all([(self._row_set(i) == self._symbol_set and
                      self._column_set(j) == self._symbol_set and
                      self._subsquare_set(i, j) ==
                      self._symbol_set) for i in range(n) for j in range(n)])

    def extensions(self):
        """
        Return list of extensions of SudokuPuzzle self.

        @type self: SudokuPuzzle
        @rtype: list[SudokuPuzzle]

        >>> r1 = ["A", "B", "C", "D"]
        >>> r2 = ["C", "D", "A", "B"]
        >>> r3 = ["B", "A", "D", "C"]
        >>> r4 = ["D", "C", "B", "*"]
        >>> grid = [r1, r2, r3, r4]
        >>> s = SudokuPuzzle(4, grid, {"A", "B", "C", "D"})
        >>> L1 = list(s.extensions())
        >>> grid[-1][-1] = "A"
        >>> L2 = [SudokuPuzzle(4, grid, {"A", "B", "C", "D"})]
        >>> len(L1) == len(L2)
        True
        >>> all([s in L2 for s in L1])
        True
        >>> all([s in L1 for s in L2])
        True
        """
        # convenient names
        symbols, symbol_set, n = self._symbols, self._symbol_set, self._n
        if not any("*" in row for row in symbols):
            return []
        else:
            # get position of first empty position
            r = 0 # row with first empty position
            while "*" not in symbols[r]:
                r += 1
            c = symbols[r].index("*") # column with first empty position
            
            # allowed symbols at position (r, c)
            # A | B == A.union(B)
            allowed_symbols = (self._symbol_set -
                               (self._row_set(r) |
                                self._column_set(c) |
                                self._subsquare_set(r, c)))
            
            # list of SudokuPuzzles with each legal digit at position i
            return_lst = []
            for symbol in allowed_symbols:
                new_puzzle = SudokuPuzzle(n, symbols[:r] + \
                                          [symbols[r][:c] + [symbol] + symbols[r][c+1:]] + \
                                          symbols[r+1:], symbol_set)
                return_lst.append(new_puzzle)
            return return_lst
        
    # TODO
    # override fail_fast
    # Notice that it is not possible to complete a sudoku puzzle if there
    # is one open position that has no symbols available to put in it.  In
    # other words, if there is one open position where the symbols already used
    # in the same row, column, and subsquare exhaust the symbols available,
    # there is no point in continuing.
    def fail_fast(self):
        """
        Return whether some unfilled position has no allowable symbols
        remaining to choose from, and hence this SudokoPuzzle can never
        be completed.

        >>> s = SudokuPuzzle(4, \
        [["A", "B", "C", "D"], \
        ["C", "D", "*", "*"], \
        ["*", "*", "*", "*"], \
        ["*", "*", "*", "*"]], {"A", "B", "C", "D"})
        >>> s.fail_fast()
        False
        >>> s = SudokuPuzzle(4, \
        [["B", "D", "A", "C"], \
        ["C", "A", "B", "D"], \
        ["A", "B", "*", "*"], \
        ["*", "*", "*", "*"]], {"A", "B", "C", "D"})
        >>> s.fail_fast()
        True
        """

        # TODO: Complete this method
        pass
    
    # some helper methods
    def _row_set(self, r):
        #
        # Return set of symbols in row of SudokuPuzzle self's symbols
        # where position m occurs.
        #
        # @type self: SudokuPuzzle
        # @type r: int

        # set of elements from symbols[r]
        return set(self._symbols[r])

    def _column_set(self, c):
        # Return set of symbols in column of SudokuPuzzle self's symbols
        # where position m occurs.
        #
        # @type self: SudokuPuzzle
        # @type c: int
        
        # set of elements from symbols[0][c], symbols[1][c],
        # ... symbols[len(symbols)-1][c]
        return set([row[c] for row in self._symbols])

    def _subsquare_set(self, r, c):
        # Return set of symbols in subsquare of SudokuPuzzle self's symbols
        # where position m occurs.
        #
        # @type self: SudokuPuzzle
        # @type m: int

        # convenient names
        n, symbols = self._n, self._symbols
        # length of subsquares
        ss = round(n ** (1 / 2))
        # upper-left position of m's subsquare
        ul_row = (r // ss) * ss
        ul_col = (c // ss) * ss

        subsquare_symbols = []
        for i in range(ss):
            for j in range(ss):
                subsquare_symbols.append(symbols[ul_row + i][ul_col + j])
        return set(subsquare_symbols)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    s = SudokuPuzzle(9,
                     [["*", "*", "*", "7", "*", "8", "*", "1", "*"],
                      ["*", "*", "7", "*", "9", "*", "*", "*", "6"],
                      ["9", "*", "3", "1", "*", "*", "*", "*", "*"],
                      ["3", "5", "*", "8", "*", "*", "6", "*", "1"],
                      ["*", "*", "*", "*", "*", "*", "*", "*", "*"],
                      ["1", "*", "6", "*", "*", "9", "*", "4", "8"],
                      ["*", "*", "*", "*", "*", "1", "2", "*", "7"],
                      ["8", "*", "*", "*", "7", "*", "4", "*", "*"],
                      ["*", "6", "*", "3", "*", "2", "*", "*", "*"]],
                     {"1", "2", "3", "4", "5", "6", "7", "8", "9"})

    from time import time

    print("solving sudoku from July 9 2015 Star... \n\n{}\n\n".format(s))
    from puzzle_tools import depth_first_solve

    start = time()
    sol = depth_first_solve(s)
    print(sol)
    while sol.children:
        sol = sol.children[0]
    end = time()
    print("time to solve 9x9 using depth_first: "
          "{} seconds\n".format(end - start))
    print(sol)

    """
    s = SudokuPuzzle(9,
                     [["*", "*", "*", "9", "*", "2", "*", "*", "*"],
                      ["*", "9", "1", "*", "*", "*", "6", "3", "*"],
                      ["*", "3", "*", "*", "7", "*", "*", "8", "*"],
                      ["3", "*", "*", "*", "*", "*", "*", "*", "8"],
                      ["*", "*", "9", "*", "*", "*", "2", "*", "*"],
                      ["5", "*", "*", "*", "*", "*", "*", "*", "7"],
                      ["*", "7", "*", "*", "8", "*", "*", "4", "*"],
                      ["*", "4", "5", "*", "*", "*", "8", "1", "*"],
                      ["*", "*", "*", "3", "*", "6", "*", "*", "*"]],
                     {"1", "2", "3", "4", "5", "6", "7", "8", "9"})

    print("solving 3-star sudoku from \"That's Puzzling\","
          "November 14th 2015\n\n{}\n\n".format(s))
    start = time()
    sol = depth_first_solve(s)
    while sol.children:
        sol = sol.children[0]
    end = time()
    print("time to solve 9x9 using depth_first: {} seconds\n".format(
        end - start))
    print(sol)

    s = SudokuPuzzle(9,
                     [["5", "6", "*", "*", "*", "7", "*", "*", "9"],
                      ["*", "7", "*", "*", "4", "8", "*", "3", "1"],
                      ["*", "*", "*", "*", "*", "*", "*", "*", "*"],
                      ["4", "3", "*", "*", "*", "*", "*", "*", "*"],
                      ["*", "8", "*", "*", "*", "*", "*", "9", "*"],
                      ["*", "*", "*", "*", "*", "*", "*", "2", "6"],
                      ["*", "*", "*", "*", "*", "*", "*", "*", "*"],
                      ["1", "9", "*", "3", "6", "*", "*", "7", "*"],
                      ["7", "*", "*", "1", "*", "*", "*", "4", "2"]],
                     {"1", "2", "3", "4", "5", "6", "7", "8", "9"})

    print(
        "solving 4-star sudoku from \"That's Puzzling\", "
        "November 14th 2015\n\n{}\n\n".format(
            s))
    start = time()
    sol = depth_first_solve(s)
    while sol.children:
        sol = sol.children[0]
    end = time()
    print("time to solve 9x9 using depth_first: {} seconds\n".format(
        end - start))
    print(sol)
    """
