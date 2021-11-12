# Square.py
# Daniel Selmes 2021
# Class implementing a square in a sodoku puzzle


from os import linesep
import typing


class Square:
    """
    Maintains the state of an individual square.

    A square can have three states: Clue, where the number inside is defined in
    the initial puzzle, Solved, where the number inside has been deduced with
    certainty, and unsolved, where the contents of the square is not yet known.
    The `state` property defines which of these conditions the square is
    currently in: `'c'` for clue, `'s'` for solved or `'u'` for unsolved.

    If a square's contents is not known, then it will have a series of "pencil"
    hints indicating which possibilities remain. If a square has no pencil
    hints, then it is either not-yet examined, or there is a problem with the
    solution.
    """

    def __init__(self, hints=(), clue=None, solved=None):
        "Initialises a new square, optionally with a clue or solution."

        self.hints = ()

        if clue:
            self.value = clue
            self.hints = (clue,)
            self.state = 'c'
        elif solved:
            self.value = solved
            self.hints = (solved,)
            self.state = 's'
        else:
            self.value = None
            self.state = 'u'
            self.hints = hints

    def __str__(self):
        "Returns the known value of this square, or the space character if unknown."
        if self.state == 'c' or self.state == 's':
            return str(self.value)
        else:
            return ' '
    
    def __repr__(self):
        "Returns an expression which can reconstruct this square, as a string."
        if self.state == 'c':
            return "{}(clue={})".format(self.__class__.__name__, self.value)
        elif self.state == 's':
            return "{}(solved={})".format(self.__class__.__name__, self.value)
        else:
            return "{}(hints={})".format(self.__class__.__name__, self.hints)
    
    @staticmethod
    def stringSubset(squares, format_='b', rank=3):
        """Converts a subset of squares to a string, based on the desired format.
        
        Format is specified by a character: 
         - `'b'` for box (simple 3x3)
         - `'r'` for row (including dividers)
         - `'c'` for column (including dividers)"""
        # Check input
        if len(squares) < rank**2:
            raise ValueError("Array size and rank not compatible: Array Size = {}, Rank^2 = {}".format(len(squares), rank**2))
        outs = ""
        if format_ == 'b':
            # Top border
            outs += '+' + '-' * rank + '+' + linesep
            # Rows with borders
            for rowI in range(rank):
                # Left Border
                outs += '|'
                for colI in range(rank):
                    outs += str(squares[rowI*rank+colI])
                # Right border & newline
                outs += '|' + linesep
            # Bottom Border
            outs += '+' + '-' * rank + '+'
            return outs
        elif format_ == 'r':
            for colI in range(rank**2):
                # Left Borders
                if colI % rank == 0:
                    outs += '|'
                outs += str(squares[colI])
            # Right Border
            outs += '|'
            return outs
        elif format_ == 'c':
            for rowI in range(rank**2):
                if rowI % rank == 0:
                    # Top Borders
                    outs += '-' + linesep
                outs += str(squares[rowI]) + linesep
            # Bottom Border
            outs += '-'
            return outs
        else:
            raise ValueError("Unknown output format specified: {}".format(format_))
    
    def solve(self, value):
        """Marks the square as solved with a specific value.

        As a matter of courtesy, we set the pencil hints to the value so that we
        can assume it contains the solved value."""
        self.value = value
        self.state = 's'
        self.hints = (value)

    def known(self):
        """Gets the value of this square if known, or `None` otherwise."""
        return self.value if self.state != 'u' else None

    @staticmethod
    def knowns(squares):
        """Class method, returns the known value of an array of squares."""
        # The map basically just checks if the square is clue/solved
        # The difference is used to trim out the Nones (for unsolved squares)
        return set(map(Square.known, squares)).difference({None})

    def hintsAt(self, check):
        "Checks if a given square hints at a potential value."
        return check in self.hints

    def addHint(self, hint):
        "Adds a value to the hint list."
        self.hints += (hint,)

    def addHints(self, hints):
        "Adds a list of values to the hint list"
        self.hints += tuple(hints)
    
    def removeHintBlind(self, hint):
        """Removes a hint from a square, if it is present in that sqaure.
        
        If the hint is not present in that square, there is no effect."""
        try:
            newHints = list(self.hints)
            newHints.remove(hint)
            self.hints = tuple(newHints)
        except ValueError:
            pass
    
    def removeHint(self, hint):
        """Removes a hint from a square. 

        Will raise ValueError if that hint is not in this square."""
        try:
            newHints = list(self.hints)
            newHints.remove(hint)
            self.hints = tuple(newHints)
        except ValueError:
            raise ValueError("Tried to remove hint {} which was not in this square's hints.".format(hint))

