# solver.py
# Daniel Selmes 2021
# My first attempt at a sodoku solver program

from square import Square
from puzzle import Puzzle

def genHints(puzzle, box):
    """Generates the hints (and solves where possible) for a box.

    First, the unknowns for the box are generated. Then, go through each box,
    calculate the knowns based on the row and column. Take the difference
    between what is between the unknowns and the knowns, this gives the
    possibilities given the current state of the puzzle. Store this in the hints
    field of the squares."""
    full = set(range(1, puzzle.rank**2+1))
    boxKnown = Square.knowns(puzzle.at(box=box))
    boxUnknown = full.difference(boxKnown)
    # Loop through each empty square and fill in the hints
    for lRow in range(puzzle.rank):
        for lCol in range(puzzle.rank):
            # Generate the knowns for this square
            (row, col) = puzzle.localToPuzzle(box, lRow, lCol)
            square = puzzle.at(row=row, col=col)
            if (square.known() == None):
                rowKnowns = Square.knowns(puzzle.at(row=row))
                colKnowns = Square.knowns(puzzle.at(col=col))
                squareKnowns = rowKnowns.union(colKnowns)
                squareHints = boxUnknown.difference(squareKnowns)
                square.addHints(squareHints)

def refineHints(puzzle, box):
    """Uses the hints to attempt to solve part of the box locally.

    Using the previously generated hints, this checks for two things:

     - A single occurrance of a digit in the whole box: This implies it's the
       only available space for the digit, and so that must be the solution for
       that sqaure.
     - A square with a single hint: This implies that only one digit can be in
       that square, so it must be the solution. 

    If either of those occurs, then we can solve that particular digit / square.
    Then, two things need to happen:

     - The square's internal hints need to be updated.
     - The row and column of the solved digit need to be updated.

    Note that once a solve happens, we need to update before attempting to solve
    more. Otherwise, we may miss removing hints that have since been proven
    wrong.  
    """
    # First pass is to 

def __main__():
    # Load the puzzle
    p = Puzzle(rank=3)
    # p.readPuzzle(" 237 945 456123789789456123312978645 453 297 978645312231897564564231897 975 423 ")
    p.readPuzzle(".5..83.17...1..4..3.4..56.8....3...9.9.8245....6....7...9....5...729..861.36.72.4")
    # Draw the whole thing
    print("Full Puzzle: ")
    print(p)
    # Generate hints for the first box
    genHints(p, 0)
    pass


if __name__ == "__main__":
    __main__()