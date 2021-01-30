import argparse
import os

from constants import *
from fen2png import Board, DrawImage

parser = argparse.ArgumentParser(description=DESC)
parser.add_argument(dest="FEN", nargs=6, default=None, help=FEN_HELP)
parser.add_argument("-f", dest="fmt", metavar="format", default="png", help=FORMAT_HELP)
parser.add_argument(
    "-o", dest="filename", metavar="output file", default="result", help=FILE_HELP
)
parser.add_argument(
    "-dir", dest="folder", metavar="output folder", default=OUTPUT, help=FOLDER_HELP
)


def mainFTP(fen_array):
    fen = Board(fen_array)
    if fen.isvalid:
        boardGrid = fen.board
        boardImg = DrawImage(boardGrid, 'png', 'output', 'result')
        boardImg.create()
        boardImg.to_image()
    else:
        print("Invalid FEN. No Image file was generated.")

if __name__ == "__main__":
    main()
