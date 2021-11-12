# Puzzle.py
# Daniel Selmes 2021
# Implements a model for a sodoku puzzle.

from os import linesep

from square import Square

class Puzzle:

    """Models a sodoku-like grid containing digits in squares.

Rank:

The rank is basically the "size" of the grid fundamentally. Traditional sodoku
grids have rank 3, since they are a 3x3 grid of 3x3 grids. The general sodoku
puzzle is an NxN grid with N boxes, where each row, column and box contains the
values 1-N where N is the rank squared. Unless explicitly mentioned, the puzzle
is assumed to be a traditional 3x3.

Structures: 

There are a few different ways to structure a puzzle, I'll define them here. The
general trend is that squares are ordered left-to-right and then top-to-bottom:

- Linear: All squares are in a single linear array, row by row. The top left
  square is at index 0, the top right square is at index 8, the bottom left
  square is at index 72, and the bottom right square is at index 80.
- Row / Column / Box: A nested array, with the outer array grouping by the
  indicated method (e.g. the 9 rows in order would be by row).
- Fully Nested: A nested array, where the outer is indicated first, and the
  inner is indicated second, e.g. Box-Row would be the boxes for the outer
  array, the rows for the inner array, and the columns for the elements
  themselves.
    """

    def __init__(self, rank=3):
        "Initialises a new puzzle of rank N (default 3). All squares are empty."
        self.rank = rank
        self.linear = [Square() for x in range (rank**4)]

    def readPuzzle(self, puzzleString):
        """Reads in a puzzle and sets it to the given string. 

        All previous data is erased, including hints solved squares."""
        # Check string length
        if len(puzzleString) < self.rank**4:
            raise ValueError("The puzzle string is less than {} elements long.".format(self.rank**4))
        # Begin parsing the puzzle
        trimmed = puzzleString[:self.rank**4]
        rowI = 0
        colI = 0
        self.linear = []
        for ch in trimmed:
            if ch in "123456789":
                self.linear.append(Square(clue=int(ch)))
            else:
                self.linear.append(Square())
            colI += 1
            if (colI >= self.rank**2):
                colI = 0
                rowI += 1

    def at(self, box=None, row=None, col=None):
        """Obtains a subset of the puzzle, based on the given parameters.

        This will filter out a subsection of the puzzle based on the given
        parameters. If a box is specified, then the result will be constrained
        to that box, but otherwise filtered only by the other parameters. For
        example, if `box=2`, only values from the top right box will be
        provided, and only row indices 0-2 and column indices 6-8 are valid.

        If row is provided, an individual row will be selected, and likewise
        with column. Note that selecting column will still return a
        single-dimension array. If neither are specified, the linear form of the
        the selected box is returned. In this case, if a box is *also* not
        specified, then the entire puzzle is returned in a linear form.

        If both a row and a column are specified, then a single square will be
        returned. Otherwise the output is a linear array of the requested
        values. 
        """
        # Alias rank since we use it a lot
        rank = self.rank
        # Filter by box if needed
        linearised = []
        if (box != None):
            # Validate box number
            if box >= rank**2:
                raise ValueError("Invalid box specified ({} not valid for rank {}".format(box, rank))
            # Calculate box position
            boxRow = int(box / rank)
            boxCol = box % rank
            # Calculate bounds of box
            rMin = boxRow * rank
            rMax = (boxRow + 1) * rank
            cMin = boxCol * rank
            cMax = (boxCol + 1) * rank
            # Check if the row and column specifiers are within the box
            if ((row != None) and (row < rMin or row >= rMax)):
                raise ValueError("Invalid row specified ({} not valid for box {})".format(row, box))
            if ((col != None) and (col < cMin or col >= cMax)):
                raise ValueError("Invalid col specified ({} not valid for col {})".format(col, box))
            # Get just the elements in that box
            for sRow in range(rMin, rMax):
                linearised += self.linear[
                    sRow * rank**2 + cMin :
                    sRow * rank**2 + cMax
                ]
        else:
            # No filtering required
            linearised = self.linear
        # Convert the row and column specifiers to local if required
        lRow = row % rank if (box != None and row != None) else row
        lCol = col % rank if (box != None and col != None) else col
        # Return row, possibly a single cell
        if (row != None):
            # Get correct size of row to sample
            size = rank if (box != None) else rank**2
            out = linearised[lRow*size:(lRow+1)*size]
            return out[lCol] if (col != None) else out
        if (col != None):
            # Just column was specified
            size = 1 if (box != None) else rank
            gap = size * rank
            out = []
            for rowI in range(size * rank):
                out.append(linearised[(gap) * rowI + lCol])
            return out
        # If neither, then we must want to just return the whole thing
        return linearised


    def localToPuzzle(self, box, lRow, lCol):
        "Converts a pair of (row,column) indices from local (just in the box) to Puzzle-wide."
        rank = self.rank
        return (int(box / 3) * rank + lRow, box * rank + lCol)

    def __str__(self) -> str:
        """Converts the puzzle to a string representation."""
        out = ""
        for rowI in range(self.rank**2):
            # Row Header
            if rowI % self.rank == 0:
                out += (('+' + '-' * self.rank) * self.rank) + '+' + linesep
            for colI in range(self.rank**2):
                # Square side borders
                if colI % self.rank == 0:
                    out += '|'
                # Actual value of the square
                out += str(self.linear[rowI*(self.rank**2) + colI])
            out += '|' + linesep
        out+= ('+' + '-' * self.rank) * self.rank + '+'
        return out
