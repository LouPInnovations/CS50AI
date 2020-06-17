import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        for variable in self.domains:
            removelist = []
            for word in self.domains[variable]:
                if variable.length != len(word):
                    #self.domains[variable].remove(word)
                    removelist.append(word)
            for word1 in removelist:
                #print(word1)
                self.domains[variable].remove(word1)



    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        change = False
        rmwords = []
        spot = self.crossword.overlaps[(x, y)]
        if spot is None:
            return change
        #print(spot)
        for word1 in self.domains[x]:
            rmword = True
            for word2 in self.domains[y]:
                #print(word1[spot[0]])
                #print(word2[spot[1]])
                #try:
                if word1[spot[0]] == word2[spot[1]]: # and word1 != word2
                    rmword = False
                    break
                #except:
                    #continue

            if rmword == True:
                #self.domains[x].remove(word1)
                rmwords.append(word1)
                change = True

        for word in rmwords:
            self.domains[x].remove(word)

        #print("Change")
        #print(change)
        return change


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        queue = set()

        if arcs is not None:
            queue = arcs
            #print(queue)

        else:
            for var1 in self.domains:
                for var2 in self.crossword.neighbors(var1):
                    #if (var1, var2) not in queue: # and (var2, var1) not in queue
                    queue.add((var1, var2))

        #print(queue)

        while queue is not None and len(queue) is not 0:
            #print(queue)
            #print('QUEUE1 *****')
            pair = list(queue)[0]
            #print(pair)
            queue.remove(list(queue).pop(0))
            #print(queue)
            #print('QUEUE2 *****')

            revised = self.revise(pair[0], pair[1])
            if revised:
                if len(self.domains[pair[0]]) == 0:
                    return False
                for neighbour in self.crossword.neighbors(pair[0]):
                    if neighbour != pair[1]:
                        queue.add((neighbour, pair[0]))

        return True





    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        if len(assignment) == len(self.domains):
            #print('TRUE')
            return assignment

        #filled = True

        #for key in assignment.keys():
            #if key is not None: #idk if i check if its filled or if it has a list size of 1 or smth or need to do the len thing
                #filled = False
               # break

       # return filled

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        #print('reached')
        for var1 in assignment:
            if var1.length != len(assignment[var1]):
                #print('FALSE')
                return False

            for var2 in assignment:
                if var1 == var2:
                    continue

                if assignment[var1] == assignment[var2]:
                    return False

                #print(self.crossword.overlaps)
                overlap = self.crossword.overlaps[(var1, var2)]
                if overlap is None:
                    #print("FALSE")
                    return False
                if assignment[var1][overlap[0]] != assignment[var2][overlap[1]]:
                    #print("FALSE")
                    return False


        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        rulenum = []

        for value1 in self.domains[var]:
            count = 0
            for neighbour in self.crossword.neighbors(var):
                spot = self.crossword.overlaps((var, neighbour))
                for value2 in self.domains[neighbour]:
                    if value1[spot[0]] != value2[spot[1]]:
                        count += 1
            rulenum.append((value1, count))


        rulenum = sorted(rulenum, key=lambda l:l[1])
        #print(rulenum)

        return rulenum

        #return self.domains[var] #implement order later

    def select_unassigned_variable(self, assignment): #Do i need to use sort?
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        minvar = None
        #print(minvar)
        minval = 10000

        for var in self.domains:
            if var not in assignment:
                if len(self.domains[var]) < minval:
                    minval = len(self.domains[var])
                    minvar = var

                elif len(self.domains[var]) == minval:
                    neighbours1 = len(self.crossword.neighbors(minvar))
                    neighbours2 = len(self.crossword.neighbors(var))
                    if neighbours2 > neighbours1:
                        minvar = var

                #print(minvar)
        #print(minvar)
        return minvar


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """


        if len(assignment) == len(self.domains):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.domains[var]:
            newassign = assignment.copy()
            newassign[var] = value
            if self.consistent(newassign):
                result = self.backtrack(newassign)
                if result is not None:
                    return result
            #self.domains[var].remove(value)

        return None



def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
