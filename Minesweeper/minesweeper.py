import itertools
import random


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
        # Checks if the number of spots = number of mines. If it matches, then all are mines and that will be returned.
        if self.count == len(self.cells):
            return self.cells

        # If it is not all mines then None is returned.
        return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        # If the count for mines is 0, then there are no mines at all within this sentence.
        if self.count == 0:
            return self.cells

        # If its not all safe spaces, None is returned.
        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        # If the cell is in this sentence, then remove it and the count goes down 1 since the mine has been marked (one less mine in sentence).
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        # If the cell is in this sentence, it is removed since it is marked safe.
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width.
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on.
        self.moves_made = set()

        # Keep track of cells known to be safe or mines.
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true.
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """

        # The cell is marked as a mine in every sentence in knowledge base and added to the mines variable within this object.
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """

        # The cell is marked safe in every sentence in knowledge base and added to the safes variable within this object.
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
        #1
        self.moves_made.add(cell)

        #2
        self.mark_safe(cell)

        #3: Checks for surrounding tiles (if possible) then adds them as a statement with count.
        moves = []
        for i in range(max(0, cell[0] - 1), min(self.width, cell[0] + 2)):
            for j in range(max(0,cell[1] - 1), min(self.height, cell[1] + 2)):
                if (i,j) != cell:
                    moves.append((i,j))
        self.knowledge.append(Sentence(moves, count))

        #4: Finds safe moves from all sentences then marks them safe.
        safeMoves = []
        for sentence in self.knowledge:
            if sentence.known_safes() is not None:
                for cell in sentence.known_safes():
                    safeMoves.append(cell)
        for cell in safeMoves:
            self.safes.add(cell)
            sentence.mark_safe(cell)

            mineMoves = []
            for sentence in self.knowledge:
                if sentence.known_mines() is not None:
                    for cell in sentence.known_mines():
                        mineMoves.append(cell)
        for cell in mineMoves:
            self.mines.add(cell)
            sentence.mark_mine(cell)


        #5: Makes new sentences which shorten/simplify to provide more useful info.
        newCells = []
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1.cells.issubset(sentence2.cells) and sentence1 != sentence2:
                    newSet = sentence2.cells.difference(sentence1.cells)
                    newCount = sentence2.count - sentence1.count
                    newCells.append(Sentence(newSet,newCount))

        #Sentence is not directly added due to error occurring, which is why it is added from a list after.
        for cell in newCells:
            if cell not in self.knowledge:
                self.knowledge.append(cell)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        #Does its intended function.
        for cell in self.safes:
            if cell in self.safes and cell not in self.mines and cell not in self.moves_made:
                return cell

        return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        #Makes a list of all possible spots that are within condition.
        possibleSpots = []
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    possibleSpots.append((i, j))

        #A random spot is chosen then returned.
        randspot = random.randint(0, len(possibleSpots))
        try:
            return possibleSpots[randspot]
        except:
            return None

