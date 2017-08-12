from puzzle import Puzzle


class WordLadderPuzzle(Puzzle):
    """
    A word-ladder puzzle that may be solved, unsolved, or even unsolvable.
    """

    def __init__(self, from_word, to_word, ws):
        """
        Create a new word-ladder puzzle with the aim of stepping
        from from_word to to_word using words in ws, changing one
        character at each step.

        @type from_word: str
        @type to_word: str
        @type ws: set[str]
        @rtype: None
        """
        (self._from_word, self._to_word, self._word_set) = (from_word,
                                                            to_word, ws)
        # set of characters to use for 1-character changes
        self._chars = "abcdefghijklmnopqrstuvwxyz"


    def __str__(self):
        fromWord = "From Word = " + self._from_word
        toWord = "To Word   = " + self._to_word
        return fromWord + "\n" + toWord


    def __eq__(self, other):
        # checks to see if from and to words are the same
        sameFromWord = self._from_word == other._from_word
        sameToWord = self._to_word == other._to_word
        return sameFromWord and sameToWord


    def extensions(self):
        
        '''() -> list[Puzzle Objects]
        '''
        # setting up variables
        extensions = []
        word = self._from_word

        # loops by the number of letters in from_word
        for letter in range(len(word)):
            # loops through the alphabet
            for char in self._chars:

                # constructs new word from 3 parts
                first = word[:letter-len(word)]
                second = word[letter+1:]
                newWord = first + char + second

                # has to have contructed a NEW word in word set
                if newWord != word and newWord in self._word_set:
                    # cleaner naming
                    to_word, ws = self._to_word, self._word_set
                    # create all extensions via new puzzle objects which
                    # incorporate the new word constructed
                    extension = WordLadderPuzzle(newWord, to_word, ws)
                    extensions.append(extension)

        return extensions


    def is_solved(self):
        
        '''() -> Bool
        This function checks to see if objective word has been reached.
        
        >>>
        
        >>>
        
        >>>
        '''
        return self._from_word == self._to_word


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    with open("words", "r") as words:
        word_set = set(words.read().split())
    w = WordLadderPuzzle("same", "cost", word_set)
    start = time()
    sol = breadth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using breadth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
    start = time()
    sol = depth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using depth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
