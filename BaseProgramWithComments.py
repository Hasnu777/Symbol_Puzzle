#Skeleton Program code for the AQA A Level Paper 1 Summer 2024 examination
#this code should be used in conjunction with the Preliminary Material
#written by the AQA Programmer Team
#developed in the Python 3.9.4 programming environment

import random # Used for randrange, during grid creation. Maybe other places, not sure
import os # Not being used currently, so I'm guessing we need to learn how to use os

# Below subroutine is the entry point to the program:
# Handles playing the game/choosing to play again
# Takes in file name to be loaded and then creates a Puzzle object
# Calls a Puzzle method to attempt the puzzle then gives the final score and asks to play again
def Main():
    Again = "y" # Starts so that game immediately occurs without needing to check.
    Score = 0 # Defines Score as integer variable. Outside of while loop so no flooring occurring here.
    while Again == "y": # Checks if user wants to play another puzzle
        Filename = input("Press Enter to start a standard puzzle or enter name of file to load: ")
        if len(Filename) > 0:
            MyPuzzle = Puzzle(Filename + ".txt") # Try block for file name is within the __LoadPuzzle method
        else:
            MyPuzzle = Puzzle(8, int(8 * 8 * 0.6)) # Checked if file name was given, else made default puzzle
        Score = MyPuzzle.AttemptPuzzle() # User starts playing via calling the AttemptPuzzle() method
        # TODO Hasnu: verify this theory - score is not actually getting floored and carries into other puzzles
        print("Puzzle finished. Your score was: " + str(Score)) # Displays final result
        Again = input("Do another puzzle? ").lower() # if anything but 'y' or 'Y' is entered the program stops

class Puzzle(): # Used to create puzzles from files stored with the program, or makes a default puzzle
    def __init__(self, *args): # Arguments are all packed, so variable amount can be given. Acts as a tuple(?)
        if len(args) == 1: # This is true when a file name is given. Gives default
            self.__Score = 0
            self.__SymbolsLeft = 0
            self.__GridSize = 0
            self.__Grid = []
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            self.__LoadPuzzle(args[0]) # Method to take in filename given and load the puzzle
        else: # This is true when a file name is not given, so these are the defaults
            self.__Score = 0
            self.__SymbolsLeft = args[1] # Taking in int(8*8*0.6) so 38 letters available for board
            self.__GridSize = args[0] # Takes in length of each side of the board (square board so row/column are equal)
            self.__Grid = []
            for Count in range(1, self.__GridSize * self.__GridSize + 1): # Creating randomly generated grid
                if random.randrange(1, 101) < 90: # 90/101 odds of unblocked cells (90/100 if 101 is excl.)
                    C = Cell() # Empty cell object
                else:
                    C = BlockedCell() # blocked cell (@) object
                self.__Grid.append(C) #Not 2D list, so just puts all in. Assuming list splicing to take rows/columns.
            self.__AllowedPatterns = []  # Holds Pattern() objects that are created below
            self.__AllowedSymbols = []  # Holds letters, shown below (Q, X, T)
            QPattern = Pattern("Q", "QQ**Q**QQ")  # TODO Hasnu: understand purpose of the *, **
            self.__AllowedPatterns.append(QPattern)
            self.__AllowedSymbols.append("Q")
            XPattern = Pattern("X", "X*X*X*X*X")
            self.__AllowedPatterns.append(XPattern)
            self.__AllowedSymbols.append("X")
            TPattern = Pattern("T", "TTT**T**T")
            self.__AllowedPatterns.append(TPattern)
            self.__AllowedSymbols.append("T")

    def __LoadPuzzle(self, Filename):
        try:
            with open(Filename) as f:
                NoOfSymbols = int(f.readline().rstrip()) # rstrip removes any trailing characters at the end (e.g. \n)
                for Count in range (1, NoOfSymbols + 1): # reads from line 1 I guess?
                    self.__AllowedSymbols.append(f.readline().rstrip()) #TODO Hasnu: check how the file is read, and check formatting of the file
                NoOfPatterns = int(f.readline().rstrip()) # Depends on file formatting. Within the try block so I'm guessing they're catching with error types?
                for Count in range(1, NoOfPatterns + 1): # reading all patterns in the file, 1->Num+1 = 0->Num
                    Items = f.readline().rstrip().split(",") # TODO Hasnu: check format of pattern in file to see why this happens
                    P = Pattern(Items[0], Items[1])  # SymbolToUse, and then the PatternString
                    self.__AllowedPatterns.append(P) # Adds to list of allowed patterns
                self.__GridSize = int(f.readline().rstrip()) # from acceptable file format, should raise error if no worky
                for Count in range (1, self.__GridSize * self.__GridSize + 1): # Creating actual grid now I think
                    Items = f.readline().rstrip().split(",") # Taking info for each cell, check format
                    if Items[0] == "@": # Blocked cell
                        C = BlockedCell() # Creates blocked cell object
                        self.__Grid.append(C) # Adds blocked cell to grid
                    else:
                        C = Cell() # I'm guessing literally anything could represent this, incl. space or \n
                        C.ChangeSymbolInCell(Items[0]) # Must be empty space I guess then
                        for CurrentSymbol in range(1, len(Items)):
                            C.AddToNotAllowedSymbols(Items[CurrentSymbol])  # TODO Hasnu: check wtf this means
                        self.__Grid.append(C) # Adds empty cell to the grid
                self.__Score = int(f.readline().rstrip()) #
                self.__SymbolsLeft = int(f.readline().rstrip())
        except: #TODO Hasnu: find different error types in the above try block and figure out how to write their corresponding excepts
            print("Puzzle not loaded")

    def AttemptPuzzle(self):
        Finished = False
        while not Finished: #not False equates to True
            self.DisplayPuzzle() #method to show puzzle. Occurs at the start of each turn/round
            print("Current score: " + str(self.__Score)) #string manipulation, using Score attribute.
            #TODO Hasnu: check the purpose behind using underscores in the attributes and methods for the classes
            Row = -1 #starter value, gets changed in the below loop
            Valid = False
            while not Valid: #not False equates to True
                try:
                    Row = int(input("Enter row number: "))  #takes number only, no validity check on row range
                    Valid = True
                except:
                    pass  #if invalid value put in e.g. character
            Column = -1  #starter value, gets changed in the below loop
            Valid = False
            while not Valid: #not False equates to True
                try:
                    Column = int(input("Enter column number: ")) #takes number, no validity check on column range though
                    Valid = True
                except:
                    pass #if invalid value put in e.g. character
            Symbol = self.__GetSymbolFromUser() #method to input symbol from user
            self.__SymbolsLeft -= 1 #finite size for symbol pool, symbol usage occurs so num. of symbols decreases by 1
            CurrentCell = self.__GetCell(Row, Column) #checks with puzzle to see what's inside the user's chosen cell
            if CurrentCell.CheckSymbolAllowed(Symbol): #method to check if the symbol can be used/put in the cell
                CurrentCell.ChangeSymbolInCell(Symbol) #replaces whatever's in the cell (empty/space/another symbol)
                AmountToAddToScore = self.CheckforMatchWithPattern(Row, Column) #Checking if a pattern has been created
                if AmountToAddToScore > 0:
                    self.__Score += AmountToAddToScore #adds pattern score to total score for puzzle
            if self.__SymbolsLeft == 0: #once user uses all symbols
                Finished = True #breaks while loop: not True equates to False
        print()
        self.DisplayPuzzle() #displays final state of the puzzle
        print()
        return self.__Score #returns total score from the puzzle/patterns made

    def __GetCell(self, Row, Column):
        Index = (self.__GridSize - Row) * self.__GridSize + Column - 1
        # Rows in the default puzzle goes from 8 at the top to 1 at the bottom (same principle for puzzle files)
        # This is why the GridSize-Row thing is being done, to access the grid properly
        # Column increases left to right, so they just do -1 because it is a zero-indexed array
        if Index >= 0:  # if negative number's been input by user
            return self.__Grid[Index]  # Grid is a 1D array, Cell() objects are mashed in next to each other
        else:
            raise IndexError()  # index variable holds a value out of range of the Grid array
# Below subroutine searches for patterns within a 5x5 grid (symbol entered being the center)
# Patterns fit in a 3x3 grid and 9 possible 3x3 grid positions in 5x5 grid, so 9 total checks
# Each check goes on the following path: top-left to top-right, to bottom-right, to bottom-left, to mid-left, to center
    def CheckforMatchWithPattern(self, Row, Column):
        for StartRow in range(Row + 2, Row - 1, -1):
            for StartColumn in range(Column - 2, Column + 1):
                try:  # 3x3 grid check
                    PatternString = ""  # gets reset each time
                    PatternString += self.__GetCell(StartRow, StartColumn).GetSymbol()  # top left
                    PatternString += self.__GetCell(StartRow, StartColumn + 1).GetSymbol()  # top mid
                    PatternString += self.__GetCell(StartRow, StartColumn + 2).GetSymbol()  # top right
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 2).GetSymbol()  # mid right
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 2).GetSymbol()  # bottom right
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 1).GetSymbol()  # bottom mid
                    PatternString += self.__GetCell(StartRow - 2, StartColumn).GetSymbol()  # bottom left
                    PatternString += self.__GetCell(StartRow - 1, StartColumn).GetSymbol()  # middle left
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 1).GetSymbol()  # center
                    for P in self.__AllowedPatterns: # P = Pattern
                        CurrentSymbol = self.__GetCell(Row, Column).GetSymbol()
                        if P.MatchesPattern(PatternString, CurrentSymbol): # TODO Hasnu: understand this and below
                            self.__GetCell(StartRow, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            return 10
                except:
                    pass
        return 0

    def __GetSymbolFromUser(self):  # Literally in the name
        Symbol = ""
        while not Symbol in self.__AllowedSymbols:  # Validation loop, making sure a valid symbol is entered
            Symbol = input("Enter symbol: ")
        return Symbol

    def __CreateHorizontalLine(self):  # Used in DisplayPuzzle() to create row separators
        Line = "  "  # For proper formatting of the grid creation
        for Count in range(1, self.__GridSize * 2 + 2): # Default is 8x8, 8*2 + 2 = 18.
            Line = Line + "-"  # This is creating the row line which gets returned and then printed
        return Line

    def DisplayPuzzle(self):  # Literally in the name
        print()
        if self.__GridSize < 10:  # __GridSize = length of row/column
            print("  ", end='')  # Space creation for formatting of the row numbers
            for Count in range(1, self.__GridSize + 1):
                print(" " + str(Count), end='')  # printing the column numbers, end occurs at last Count iteration(?)
        print()
        print(self.__CreateHorizontalLine())  # Prints a line of dashes, as a row separator
        for Count in range(0, len(self.__Grid)):  # Default __Grid length is 8*8=64
            if Count % self.__GridSize == 0 and self.__GridSize < 10:  # Checking
                print(str(self.__GridSize - ((Count + 1) // self.__GridSize)) + " ", end='')  # LHS column line
            print("|" + self.__Grid[Count].GetSymbol(), end='')  # Inner column line then prints Symbol from Cell
            if (Count + 1) % self.__GridSize == 0:
                print("|")  # RHS column lines
                print(self.__CreateHorizontalLine())  # Row separator line

class Pattern():  # Used in __init__ for Puzzle()
    def __init__(self, SymbolToUse, PatternString):
        self.__Symbol = SymbolToUse  # Default is Q, X, T
        self.__PatternSequence = PatternString  # Default is "QQ**Q**QQ", "X*X*X*X*X", "TTT**T**T"


    def MatchesPattern(self, PatternString, SymbolPlaced):  # Pattern object holds __Symbol as SymbolToUse
        if SymbolPlaced != self.__Symbol:  # Checking if symbol placed is the same symbol that's used for this pattern
            return False  # Tells you "no this isn't the right pattern" and method ends here
        for Count in range(0, len(self.__PatternSequence)):  # PatternSequence is the correct pattern string
            try:
                if self.__PatternSequence[Count] == self.__Symbol and PatternString[Count] != self.__Symbol:
                    # PatternString is what's been read from the Puzzle. If doesn't match PatternSequence return False
                    return False
            except Exception as ex:  # General catch-all. Exception can be any error type, then formats in the string
                print(f"EXCEPTION in MatchesPattern: {ex}")
        return True

    def GetPatternSequence(self):  # This isn't being used anywhere which is weird
      return self.__PatternSequence

class Cell():  # Regular cells which are editable
    def __init__(self):
        self._Symbol = ""  # Initially empty
        self.__SymbolsNotAllowed = []

    def GetSymbol(self):  # Returning symbol stored in the Cell() object
        if self.IsEmpty():
          return "-"  # No symbol in cell
        else:
          return self._Symbol  # Returning the symbol being stored

    def IsEmpty(self):  # Checking if Cell() object holds no symbol
        if len(self._Symbol) == 0:  # Checking for empty string
            return True  # This means Cell holds no symbol
        else:
            return False  # Symbol being held in Cell

    def ChangeSymbolInCell(self, NewSymbol):
        self._Symbol = NewSymbol  # Must be taking a string
        # TODO Hasnu: check if there's validation for this

    def CheckSymbolAllowed(self, SymbolToCheck):  # Relies on me checking what __SymbolsNotAllowed is used for
        for Item in self.__SymbolsNotAllowed:
            if Item == SymbolToCheck:
                return False
        return True

    def AddToNotAllowedSymbols(self, SymbolToAdd):  # Also relies on me checking what __SymbolsNotAllowed is used for
        self.__SymbolsNotAllowed.append(SymbolToAdd)  # Adding to __SymbolsNotAllowed list

    def UpdateCell(self):  # TODO Hasnu: see if there's any possible usage for this
        pass

class BlockedCell(Cell):  # Uneditable cells, inheriting the Cell() class
    def __init__(self):
        super(BlockedCell, self).__init__()  # the __init__() of Cell() is being used to instantiate BlockedCelL()
        self._Symbol = "@"  # Denoting blocked cells by the @ symbol

    def CheckSymbolAllowed(self, SymbolToCheck):  # TODO Hasnu: check where this is being used (I don't remember)
        return False

if __name__ == "__main__":  # Used to check if this is the main program running. If imported, the program will not run.
    Main()