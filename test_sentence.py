import itertools
import random

class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        known_mines = set()
        if len(self.cells) == self.count:
            for cell in self.cells:
                known_mines.add(cell)
        return known_mines


sentence1 = Sentence(((4,7),(0,3),(0,1),(0,2),(0,4)),1)
sentence2 = Sentence(((0,2),(0,4)),1)

sentence3 = Sentence(((0,2),(0,4)),1)
sentence4 = Sentence(((0,2),(0,4)),1)

cells1 = sentence3.cells
cells2 = sentence4.cells

print(cells2.issubset(cells1))

#cells = cells1 - cells2
#count = sentence1.count - sentence2.count
#sentence3 = Sentence(cells, count)
#print(sentence3)


