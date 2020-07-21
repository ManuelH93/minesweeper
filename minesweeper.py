import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


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

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        known_safes = set()
        if self.count == 0:
            for cell in self.cells:
                known_safes.add(cell)
        return known_safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count += -1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)
        # 2) mark the cell as safe and update any sentence with cell
        self.safes.add(cell)
        self.mark_safe(cell)
        # 3) add new sentence to knowledge base
        #   create list with all surrounding cells
        surrounding_cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                # Add to sentence_cells if in bound
                if 0 <= i < self.height and 0 <= j < self.width:
                    surrounding_cells.add((i,j))
        #   create counter for mines in sentence_cells
        sentence_count = count
        # create information for sentence
        sentence_cells = copy.deepcopy(surrounding_cells)
        for cell in surrounding_cells:
            if cell in self.mines:
                sentence_cells.remove(cell)
                sentence_count += -1
            if cell in self.safes:
                sentence_cells.remove(cell)
        self.knowledge.append(Sentence(sentence_cells, sentence_count))
        # 4) mark any additional cells as safe or as mines
        counter = 0
        while counter == 0:
            # Keep track of cells marked as mines or as safes
            cells_changed = set()
            for sentence in self.knowledge:
                for cell in sentence.known_mines():
                    self.mark_mine(cell)
                    cells_changed.add(cell)
                for cell in sentence.known_safes():
                    self.mark_safe(cell)
                    cells_changed.add(cell)
        # 5) add new sentences to knowledge base    
            new_sentences = []
            for sentence1 in self.knowledge:
                cells1 = sentence1.cells
                for sentence2 in self.knowledge:
                    cells2 = sentence2.cells
                    if cells1.issubset(cells2) and cells1 != cells2:
                        cells = cells2 - cells1
                        count = sentence2.count - sentence1.count
                        new_sentences.append(Sentence(cells, count))
            # Kepp track of new sentences added to knowledge
            changes_made = 0
            for sentence in new_sentences:
                if sentence in self.knowledge:
                    continue
                else:
                    self.knowledge.append(sentence)
                    changes_made += 1
            # Only if no more changes made to knowledge do we break the loop
            if len(cells_changed) == 0 and changes_made == 0:
                counter += 1
        # remove empty sentences to keep knowledge base tidy
        tracker = 0
        for sentence in self.knowledge:
            if len(sentence.cells) == 0:
                tracker += 1
        while tracker != 0:
            for sentence in self.knowledge:
                if len(sentence.cells) == 0:
                    self.knowledge.remove(sentence)
                    tracker += -1
        # remove duplicates in knowledge base
        no_duplicates = []
        for sentence in self.knowledge:
            if sentence not in no_duplicates:
                no_duplicates.append(sentence)
        self.knowledge = no_duplicates

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        moves_made = self.moves_made
        safe_cells = self.safes
        safe_moves = safe_cells - moves_made
        if len(safe_moves) == 0:
            return None
        else:
            return random.choice(tuple(safe_moves))

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        all_cells = set()
        for i in range(self.height):
            for j in range(self.width):
                all_cells.add((i,j))
        moves_made = self.moves_made
        mines = self.mines
        possible_moves = all_cells - moves_made - mines
        if len(possible_moves) == 0:
            return None
        else:
            return random.choice(tuple(possible_moves))
