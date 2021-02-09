import moveHelperFunctions

class Fen:
    def __init__(self, fen_array):
        self.board = fen_array[0]
        self.turn = fen_array[1]
        self.castling = fen_array[2]
        self.enPassant = fen_array[3]
        self.halfMove = fen_array[4]
        self.fullMove = fen_array[5]
        self.fen_array = fen_array

    def makeMove(self, move):
        #Initialize Variable
        new_FEN_Board_ARR = []
        #Get FEN board representation
        orig_FEN_Board = self.board

        #Sepearate Move into Location and Destination
        move_LOC = move[0:2]
        move_DES = move[2:]

        #Identify segments in FEN related to move location and destination
        orig_FEN_LOC = orig_FEN_Board.split('/')[moveHelperFunctions.rankToIndex(int(move_LOC[1]))]
        orig_FEN_DES = orig_FEN_Board.split('/')[moveHelperFunctions.rankToIndex(int(move_DES[1]))]

        #Expand FEN segments into component 1 strings
        expanded_orig_FEN_LOC = moveHelperFunctions.intToCompOne(orig_FEN_LOC)
        expanded_orig_FEN_DES = moveHelperFunctions.intToCompOne(orig_FEN_DES)

        #Get moving Piece
        moving_piece = expanded_orig_FEN_LOC[moveHelperFunctions.letterToInt(move_LOC[0])]
        print('moving piece is:' + moving_piece)

        if (move_LOC[1] == move_DES[1]):
            print('same rank case')
            #Remove piece character from destination segment and replace with 1
            interm_expanded_orig_FEN_DES = expanded_orig_FEN_DES[:moveHelperFunctions.letterToInt(move_LOC[0])] + '1' + expanded_orig_FEN_DES[moveHelperFunctions.letterToInt(move_LOC[0]) + 1:]
            #Replace ‘1’ or piece character in DES with LOC piece character or PP character, if applicable
            new_expanded_orig_FEN_DES = interm_expanded_orig_FEN_DES[:moveHelperFunctions.letterToInt(move_DES[0])] + moving_piece + interm_expanded_orig_FEN_DES[moveHelperFunctions.letterToInt(move_DES[0]) + 1:]
            #Condense Component 1 strings to Integers
            condensed_new_FEN_DES = moveHelperFunctions.compOneToInt(new_expanded_orig_FEN_DES)
            #Update FEN Rank Segments
            new_FEN_Board_ARR = orig_FEN_Board.split('/')
            new_FEN_Board_ARR[moveHelperFunctions.rankToIndex(int(move_DES[1]))] = condensed_new_FEN_DES
        else:
            #Remove piece character from location segment and replace with 1
            new_expanded_orig_FEN_LOC = expanded_orig_FEN_LOC[:moveHelperFunctions.letterToInt(move_LOC[0])] + '1' + expanded_orig_FEN_LOC[moveHelperFunctions.letterToInt(move_LOC[0]) + 1:]

            #Replace ‘1’ or piece character in DES with LOC piece character or PP character, if applicable
            if (len(move_DES) == 3):
                print('pawn promotion')
                new_expanded_orig_FEN_DES = expanded_orig_FEN_DES[:moveHelperFunctions.letterToInt(move_DES[0])] + str(move_DES[2]).capitalize() + expanded_orig_FEN_DES[moveHelperFunctions.letterToInt(move_DES[0]) + 1:]
            else:
                print('normal move')
                new_expanded_orig_FEN_DES = expanded_orig_FEN_DES[:moveHelperFunctions.letterToInt(move_DES[0])] + moving_piece + expanded_orig_FEN_DES[moveHelperFunctions.letterToInt(move_DES[0]) + 1:]

            #Condense Component 1 strings to Integers
            condensed_new_FEN_LOC = moveHelperFunctions.compOneToInt(new_expanded_orig_FEN_LOC)
            condensed_new_FEN_DES = moveHelperFunctions.compOneToInt(new_expanded_orig_FEN_DES)

            #Update FEN Rank Segments
            new_FEN_Board_ARR = orig_FEN_Board.split('/')
            new_FEN_Board_ARR[moveHelperFunctions.rankToIndex(int(move_LOC[1]))] = condensed_new_FEN_LOC
            new_FEN_Board_ARR[moveHelperFunctions.rankToIndex(int(move_DES[1]))] = condensed_new_FEN_DES

        self.board = moveHelperFunctions.fenBoardArrToString(new_FEN_Board_ARR)
        
        #Invert side to move
        self.updateTurn()
        self.updateFenArray()
        #Modify Castling Permissions

        #Modify En Passant Square

        #Modify Halfmove/Fullmove values

    def updateTurn(self):
        if (self.turn == 'w'):
            self.turn = 'b'
        else:
            self.turn = 'w'

    def updateFenArray(self):
        self.fen_array = [
            self.board,
            self.turn,
            self.castling,
            self.enPassant,
            self.halfMove,
            self.fullMove
        ]



