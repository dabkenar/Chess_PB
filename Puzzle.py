from Fen import Fen

class Puzzle:
    def __init__(self, puzzleArray_LC):
        self.fen = Fen(puzzleArray_LC[1].split(' ')) #Fen as Fen object
        self.moves = puzzleArray_LC[2].split(' ') #Puzzle moves as Array
        self.currentMove = 0 #Index for move array
        self.movesToWin = 0
        self.complete = False
        #Determine Moves to win
        for i in range(len(self.moves)):
            if (i % 2 != 0):
                self.movesToWin += 1

        #Make Initial Move
        self.makeMove(self.moves[self.currentMove])

        #Determine Player Color
        if(self.fen.turn == 'w'):
            self.color = 'w'
        else:
            self.color = 'b'

        self.printPuzzle()

    def makeMove(self, move):
        self.fen.makeMove(move)
        self.currentMove += 1

    def printPuzzle(self):
        print('Puzzle FEN: ' + str(self.fen.fen_array))
        print('Puzzle Moves: ' + str(self.moves))
        print('Puzzle Moves to Win: ' + str(self.movesToWin))
        print('Next correct move: ' + str(self.moves[self.currentMove]))