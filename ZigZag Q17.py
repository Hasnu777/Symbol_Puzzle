# Skeleton Program code for the AQA A Level Paper 1 Summer 2024 examination
# this code should be used in conjunction with the Preliminary Material
# written by the AQA Programmer Team
# developed in the Python 3.9.4 programming environment

import random
import os


def Main():
    Again = "y"
    Score = 0
    while Again == "y":
        Filename = input("Press Enter to start a standard puzzle or enter name of file to load: ")
        if len(Filename) > 0:
            MyPuzzle = Puzzle(Filename + ".txt")
        else:
            MyPuzzle = Puzzle(8, int(8 * 8 * 0.6))
        Score = MyPuzzle.AttemptPuzzle()
        print("Puzzle finished. Your score was: " + str(Score))
        Again = input("Do another puzzle? ").lower()


class Puzzle():
    def __init__(self, *args):
        # START CHANGE
        self.__WildCardsLeft = 2
        # END CHANGE
        if len(args) == 1:
            self.__Score = 0
            self.__SymbolsLeft = 0
            self.__GridSize = 0
            self.__Grid = []
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            self.__LoadPuzzle(args[0])
        else:
            self.__Score = 0
            self.__SymbolsLeft = args[1]
            self.__GridSize = args[0]
            self.__Grid = []
            for Count in range(1, self.__GridSize * self.__GridSize + 1):
                if random.randrange(1, 101) < 90:
                    C = Cell()
                else:
                    C = BlockedCell()
                self.__Grid.append(C)
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            QPattern = Pattern("Q", "QQ**Q**QQ")
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
                NoOfSymbols = int(f.readline().rstrip())
                for Count in range(1, NoOfSymbols + 1):
                    self.__AllowedSymbols.append(f.readline().rstrip())
                NoOfPatterns = int(f.readline().rstrip())
                for Count in range(1, NoOfPatterns + 1):
                    Items = f.readline().rstrip().split(",")
                    P = Pattern(Items[0], Items[1])
                    self.__AllowedPatterns.append(P)
                self.__GridSize = int(f.readline().rstrip())
                for Count in range(1, self.__GridSize * self.__GridSize + 1):
                    Items = f.readline().rstrip().split(",")
                    if Items[0] == "@":
                        C = BlockedCell()
                        self.__Grid.append(C)
                    else:
                        C = Cell()
                        C.ChangeSymbolInCell(Items[0])
                        for CurrentSymbol in range(1, len(Items)):
                            C.AddToNotAllowedSymbols(Items[CurrentSymbol])
                        self.__Grid.append(C)
                self.__Score = int(f.readline().rstrip())
                self.__SymbolsLeft = int(f.readline().rstrip())
        except:
            print("Puzzle not loaded")

    def AttemptPuzzle(self):
        Finished = False
        while not Finished:
            self.DisplayPuzzle()
            print("Current score: " + str(self.__Score))
            # START CHANGE
            print("Wild cards will allow two symbols to be placed on top of each other and still be matched for each pattern.")
            print("You currently have " + str(self.__WildCardsLeft) + " wild cards left.")
            # END CHANGE
            Row = -1
            Valid = False
            while not Valid:
                try:
                    Row = int(input("Enter row number: "))
                    Valid = True
                except:
                    pass
            Column = -1
            Valid = False
            while not Valid:
                try:
                    Column = int(input("Enter column number: "))
                    Valid = True
                except:
                    pass
            Symbol = self.__GetSymbolFromUser()
            self.__SymbolsLeft -= 1
            CurrentCell = self.__GetCell(Row, Column)
            if CurrentCell.CheckSymbolAllowed(Symbol):
                # START CHANGE
                if not CurrentCell.IsEmpty() and CurrentCell.GetSymbol() != "@":
                    if self.__WildCardsLeft > 0:
                        self.__Grid[(self.__GridSize - Row) * self.__GridSize + Column - 1] = WildCardCell()
                        self.__WildCardsLeft -= 1
                    else:
                        print("You have used both your wildcards for this puzzle.")
                        continue
                else:
                    CurrentCell.ChangeSymbolInCell(Symbol)
                # END CHANGE
                AmountToAddToScore = self.CheckforMatchWithPattern(Row, Column)
                if AmountToAddToScore > 0:
                    self.__Score += AmountToAddToScore
            if self.__SymbolsLeft == 0:
                Finished = True
        print()
        self.DisplayPuzzle()
        print()
        return self.__Score

    def __GetCell(self, Row, Column):
        Index = (self.__GridSize - Row) * self.__GridSize + Column - 1
        if Index >= 0:
            return self.__Grid[Index]
        else:
            raise IndexError()

    def CheckforMatchWithPattern(self, Row, Column):
        for StartRow in range(Row + 2, Row - 1, -1):
            for StartColumn in range(Column - 2, Column + 1):
                try:
                    # START CHANGE
                    for P in self.__AllowedPatterns:
                        PatternString = ""
                        PatternCells = []
                        PatternCells.append(self.__GetCell(StartRow, StartColumn))
                        PatternCells.append(self.__GetCell(StartRow, StartColumn + 1))
                        PatternCells.append(self.__GetCell(StartRow, StartColumn + 2))
                        PatternCells.append(self.__GetCell(StartRow - 1, StartColumn + 2))
                        PatternCells.append(self.__GetCell(StartRow - 2, StartColumn + 2))
                        PatternCells.append(self.__GetCell(StartRow - 2, StartColumn + 1))
                        PatternCells.append(self.__GetCell(StartRow - 2, StartColumn))
                        PatternCells.append(self.__GetCell(StartRow - 1, StartColumn))
                        PatternCells.append(self.__GetCell(StartRow - 1, StartColumn + 1))
                        WildCardInPattern = False
                        for C in PatternCells:
                            if C.IsWild():
                                WildCardInPattern = True
                            PatternString += C.GetSymbol()
                        if WildCardInPattern:
                            PatternString = PatternString.replace("W", P.GetPatternSymbol())
                        CurrentSymbol = self.__GetCell(Row, Column).GetSymbol()
                        if P.MatchesPattern(PatternString, CurrentSymbol):
                            self.__GetCell(StartRow, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            if WildCardInPattern:
                                return 15
                            else:
                                return 10
                # END CHANGE
                except:
                    pass
        return 0

    def __GetSymbolFromUser(self):
        Symbol = ""
        while not Symbol in self.__AllowedSymbols:
            Symbol = input("Enter symbol: ")
        return Symbol

    def __CreateHorizontalLine(self):
        Line = "  "
        for Count in range(1, self.__GridSize * 2 + 2):
            Line = Line + "-"
        return Line

    def DisplayPuzzle(self):
        print()
        if self.__GridSize < 10:
            print("  ", end='')
            for Count in range(1, self.__GridSize + 1):
                print(" " + str(Count), end='')
        print()
        print(self.__CreateHorizontalLine())
        for Count in range(0, len(self.__Grid)):
            if Count % self.__GridSize == 0 and self.__GridSize < 10:
                print(str(self.__GridSize - ((Count + 1) // self.__GridSize)) + " ", end='')
            print("|" + self.__Grid[Count].GetSymbol(), end='')
            if (Count + 1) % self.__GridSize == 0:
                print("|")
                print(self.__CreateHorizontalLine())


class Pattern():
    def __init__(self, SymbolToUse, PatternString):
        self.__Symbol = SymbolToUse
        self.__PatternSequence = PatternString

    def MatchesPattern(self, PatternString, SymbolPlaced):
        if SymbolPlaced != self.__Symbol:
            return False
        for Count in range(0, len(self.__PatternSequence)):
            try:
                if self.__PatternSequence[Count] == self.__Symbol and PatternString[Count] != self.__Symbol:
                    return False
            except Exception as ex:
                print(f"EXCEPTION in MatchesPattern: {ex}")
        return True

    def GetPatternSequence(self):
        return self.__PatternSequence

    # START CHANGE
    def GetPatternSymbol(self):
        return self.__Symbol
    # END CHANGE


class Cell():
    def __init__(self):
        self._Symbol = ""
        self.__SymbolsNotAllowed = []

    def GetSymbol(self):
        if self.IsEmpty():
            return "-"
        else:
            return self._Symbol

    def IsEmpty(self):
        if len(self._Symbol) == 0:
            return True
        else:
            return False

    def ChangeSymbolInCell(self, NewSymbol):
        self._Symbol = NewSymbol

    def CheckSymbolAllowed(self, SymbolToCheck):
        for Item in self.__SymbolsNotAllowed:
            if Item == SymbolToCheck:
                return False
        return True

    def AddToNotAllowedSymbols(self, SymbolToAdd):
        self.__SymbolsNotAllowed.append(SymbolToAdd)

    def UpdateCell(self):
        pass

    # START CHANGE
    def IsWild(self):
        return False
    # END CHANGE


class BlockedCell(Cell):
    def __init__(self):
        super(BlockedCell, self).__init__()
        self._Symbol = "@"

    def CheckSymbolAllowed(self, SymbolToCheck):
        return False


# START CHANGE
class WildCardCell(Cell):
    def __init__(self):
        super(WildCardCell, self).__init__()
        self._Symbol = "W"

    def IsWild(self):
        return True
# END CHANGE


if __name__ == "__main__":
    Main()