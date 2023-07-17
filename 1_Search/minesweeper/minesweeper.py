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

        # if all cells are mines and count is not 0 then return the cells
        if (len(self.cells) == self.count and self.count != 0):
            return self.cells
        else:  # else return an empty set denoting that there are no mines
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        if (self.count == 0):  # if count is 0 (meaning no mines) then return the cells
            return self.cells
        else:  # else return an empty set denoting that there are no safe cells
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        if cell in self.cells:  # if the cell is in the set of cells then remove it and decrement the count
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        if cell in self.cells:  # Again if the cell is in the set of cells then remove it
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

        # * 1-add the cell to the moves made
        self.moves_made.add(cell)
        # * 2-mark the cell as safe
        self.mark_safe(cell)

        # * 3-add a new sentence to the AI's knowledge base based on the value of cell and count
        new_sentence = set()  # create a new set to hold the new sentence
        Mines = 0  # keep track of the number of mines in the new sentence

        # loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) in (cell or self.safes):
                    continue

                if (i, j) in self.mines:
                    Mines += 1
                    continue

                # if the cell is in bounds then add it to the new sentence
                if 0 <= i < self.height and 0 <= j < self.width:
                    new_sentence.add((i, j))

        # if the new sentence is not empty then add it to the knowledge base
        if (len(new_sentence) != 0):
            self.knowledge.append(
                Sentence(new_sentence, count - Mines))

        # * 4-mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
        for sentence in self.knowledge:  # loop over all sentences in the knowledge base

            if sentence.known_mines():  # if there are known mines in the sentence then mark them
                for cell in sentence.known_mines().copy():
                    self.mark_mine(cell)

            if sentence.known_safes():  # if there are known safes in the sentence then mark them
                for cell in sentence.known_safes().copy():
                    self.mark_safe(cell)

        # * 5-add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge
        for sentence1 in self.knowledge:  # loop over all sentences in the knowledge base
            for sentence2 in self.knowledge:  # loop over all sentences in the knowledge base

                # if the two sentences are the same then continue
                if sentence1 == sentence2:
                    self.knowledge.remove(sentence2)

                # if the two sentences have the same cells then continue
                if sentence1 is sentence2:
                    continue

                # if sentence1 is a subset of sentence2 then infer
                elif sentence1.cells.issubset(sentence2.cells):

                    last_sentence = Sentence(
                        sentence2.cells - sentence1.cells, sentence2.count - sentence1.count)  # create a new sentence with the difference between the two sentences(not calling the new Sentence because it might conflict with the previous one)

                    if last_sentence not in self.knowledge:  # if the new sentence is not already in the knowledge base
                        # then add it to the knowledge base
                        self.knowledge.append(last_sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        for cell in self.safes:
            if cell not in self.moves_made:  # if the cell is safe and not already a move made then return the cell
                return cell

        return None  # else return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        Possible_Random_moves = []

        for i in range(self.height):
            for j in range(self.width):
                # if the cell is not already a move made and not a mine then append it to the list
                if (i, j) not in (self.moves_made and self.mines):
                    Possible_Random_moves.append((i, j))
                else:
                    continue

        if (len(Possible_Random_moves) == 0):  # if the list is empty then return None
            return None
        else:  # else return a random cell from the list using the random module
            return random.choice(Possible_Random_moves)
