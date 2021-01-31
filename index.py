import discord
from discord.ext import commands, tasks
import os, shutil
import subprocess
import csv
import boto3
import random
import pandas as pd
from Puzzle import Puzzle
from Fen import Fen
from main import mainFTP

# s3 = boto3.resource(
#     service_name='s3',
#     region_name='us-east-2',
#     aws_access_key_id='AKIA43ZRUWSVMFZYJVWG',
#     aws_secret_access_key='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'
# )
client = commands.Bot(command_prefix = '.')
tutorialPuzzle = Puzzle(['NgJOw', '8/p4P2/8/8/3B4/1R6/8/8 b - - 0 1', 'a7a6 b3b8 a6a5 d4g7 a5a4 f7f8q', '1303', '76', '86', '353', 'endgame mate mateIn2 short', 'https://lichess.org/sn1G465d#87'])
tutorialMode = False
# puzzleDB = s3.Bucket('chess-pb').Object('lichess_db_puzzle.csv').get()
# url = 'https://raw.githubusercontent.com/dabkenar/PUZZLE_FILE_HOST/main/lichess_db_puzzle.csv'
# puzzleDF = pd.read_csv(url, memory_map=True)
# col_names = ['Id',
#              'FEN',
#              'Moves',
#              'Popularity',
#              '1',
#              '2',
#              '3',
#              '4',
#              '5',]

# row = pd.read_csv(puzzleDB['Body'], skiprows=random.randint(0, 562312), nrows=1, header=None, names=col_names)
# print(row)

def getNewPuzzle():
    #Select a random Puzzle
    puzzle_num = random.randint(0, 562312)
    with open('./lichess_db_puzzle.csv', 'r') as file:
        reader = csv.reader(file)
        file_reader = enumerate(reader)
        for i, row in file_reader:
            if i == puzzle_num:
                while(row[1].split(' ')[1] == 'w'):
                    i, row = next(file_reader)
                return row

#Get a new dummy puzzle
print('hello')
newPuzzle = Puzzle(getNewPuzzle())
newPuzzle.complete = True

@client.event
async def on_ready():
    print('Bot is Ready')

@client.event
async def on_message(message):
    global newPuzzle
    global tutorialMode
    global tutorialPuzzle
    if (message.content.startswith('.help')):
        tutorialMode = True
        await message.channel.send('Hello, I am the Chess Puzzle of the Day Discord bot. Everyday I will provide this channel with a chess Puzzle.')
        await message.channel.send('To play this puzzle you must suggest moves with the .move command and provide the initial square of the piece you would like to move, followed by its destination square. Remember, each square of the board can be identified using an alphanumerical system. Here is an image for reference:')
        await message.channel.send(file=discord.File('images/tutorial_board.png'))
        await message.channel.send('You can try this out with this puzzle right here. You can move your rook to b8 with the move command. The current location is b3 and the desired destination is b8 so your move command should look like: ".move b3b8" Try executing that command now')
        # newPuzzle = Puzzle(tutorialPuzzle)
        mainFTP(tutorialPuzzle.fen.fen_array)
        await message.channel.send(file=discord.File('./output/result.png'))

        #Directory cleanup
        os.system('rm -rf ./output/result.png')

    if (message.content.startswith('.hint')):
        await message.channel.send('Try looking at the ' + str(newPuzzle.moves[newPuzzle.currentMove][0:2]) + ' square')

    if (message.content.startswith('.chess')):
        if (not newPuzzle.complete):
            await message.channel.send('You still have a puzzle to complete')
        else:
            #Generate New Puzzle
            newPuzzle = Puzzle(getNewPuzzle())
        
        #Send Puzzle image and info
        mainFTP(newPuzzle.fen.fen_array)
        if (newPuzzle.color == 'w'):
            await message.channel.send('White to Move')
        else:
            await message.channel.send('Black to Move')
        await message.channel.send('Find ' + str(newPuzzle.movesToWin) + ' ' + pluralMoves(newPuzzle.movesToWin) + ' to complete the puzzle')
        await message.channel.send(file=discord.File('./output/result.png'))

        #Directory cleanup
        os.system('rm -rf ./output/result.png')

    if (message.content.startswith('.move')):
        move = message.content.split(' ')[1]

        if (tutorialMode):
            if (processTutorialMove(move) == 1):
                await message.channel.send('Nice job. As you can see you have moved your rook to b8 and your opponent has moved their pawn to a5. Whenever you enter the correct move, I will execute it and your opponents response move. Then I will send you a new image of the board. Now try moving your bishop to g7. This time you\'ll have to figure out the command on your own.')
                #Execute User Move
                tutorialPuzzle.makeMove(tutorialPuzzle.moves[tutorialPuzzle.currentMove])
                #Execute Counter Move
                tutorialPuzzle.makeMove(tutorialPuzzle.moves[tutorialPuzzle.currentMove])
                #Process and send new board image
                mainFTP(tutorialPuzzle.fen.fen_array)
                await message.channel.send(file=discord.File('./output/result.png'))
                #Directory cleanup
                os.system('rm -rf ./output/result.png')
                return
            elif (processTutorialMove(move) == 2):
                await message.channel.send('A brilliant move! You\'ll be a grandmaster in no time. Now for the final lesson. In chess when a pawn makes it to the other side of the board you can promote it to be a Queen (Q/q), a Rook (R/r), a Bishop (B/b) or a Knight (N/n). In order to execute a pawn promotion, you must use the move command to move your pawn 1 square forward, but add the corresponding letter of the piece you would like to promote to at the end of the command (ex. a7a8N) If you are playing the white pieces, the letter should be Upper Case. If you\'e playing the black pieces, it should be lower case. Now try promoting your Pawn to a Queen!')
                #Execute User Move
                tutorialPuzzle.makeMove(tutorialPuzzle.moves[tutorialPuzzle.currentMove])
                #Execute Counter Move
                tutorialPuzzle.makeMove(tutorialPuzzle.moves[tutorialPuzzle.currentMove])
                #Process and send new board image
                mainFTP(tutorialPuzzle.fen.fen_array)
                await message.channel.send(file=discord.File('./output/result.png'))
                #Directory cleanup
                os.system('rm -rf ./output/result.png')
                return
            elif (processTutorialMove(move) == 3):
                await message.channel.send(message.author.name + ' Win!')
                tutorialPuzzle.complete = True
                tutorialMode = False
                await message.channel.send('Great Job you have completed the Tutorial Puzzle! I have queued up a new puzzle for you to complete now. From here on out use the .chess command to get a new puzzle, and use the .help command if you want to replay the tutorial.')
                newPuzzle = Puzzle(getNewPuzzle())
                mainFTP(newPuzzle.fen.fen_array)
                if (tutorialPuzzle.color == 'w'):
                    await message.channel.send('White to Move')
                else:
                    await message.channel.send('Black to Move')
                await message.channel.send('Find ' + str(newPuzzle.movesToWin) + ' ' + pluralMoves(newPuzzle.movesToWin) + ' to complete puzzle')
                await message.channel.send(file=discord.File('./output/result.png'))
                #Directory cleanup
                os.system('rm -rf ./output/result.png')
                return
            elif (processTutorialMove(move) == 4):
                await message.channel.send('Incorrect move, try again crelbis')
                return
            elif (processTutorialMove(move) == 5):
                await message.channel.send('Invalid Move Syntax')
                return

        if (newPuzzle.complete):
            await message.channel.send('No Active puzzle, use the .chess command to request another')
            return
        if (not isValidMove(move)):
            await message.channel.send('Invalid Move Syntax')
            return
        elif (isValidMove(move) and move == newPuzzle.moves[newPuzzle.currentMove]):
            #Update Moves to win
            newPuzzle.movesToWin -= 1
            #Execute User Move
            newPuzzle.makeMove(newPuzzle.moves[newPuzzle.currentMove])
            #Check if Puzzle is complete
            if (newPuzzle.currentMove == len(newPuzzle.moves)): 
                await message.channel.send(message.author.name + ' Win!')
                newPuzzle.complete = True
                return
            #Execute Counter Move
            newPuzzle.makeMove(newPuzzle.moves[newPuzzle.currentMove])
            #Check if Puzzle is complete
            if (newPuzzle.currentMove == len(newPuzzle.moves)): 
                await message.channel.send(message.author.name + ' Win!')
                newPuzzle.complete = True
                return
            
            #Give remaining moves and resend puzzle
            await message.channel.send('Correct, Find ' + str(newPuzzle.movesToWin) + ' ' + pluralMoves(newPuzzle.movesToWin) + ' to complete the puzzle')
            mainFTP(newPuzzle.fen.fen_array)

            await message.channel.send(file=discord.File('./output/result.png'))

            #Directory cleanup
            os.system('rm -rf ./output/result.png')
        else:
            await message.channel.send('Incorrect move, try again')

def isValidMove(move):
    legal_files = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'}
    legal_ranks = { '1', '2', '3', '4', '5', '6', '7', '8'}
    if (newPuzzle.color == 'w'):
        legal_promotions = {'Q', 'R', 'B', 'N'}
    else:
        legal_promotions = {'q', 'r', 'b', 'n'}
    
    if (len(move)== 4):
        if(move[0] in legal_files and move[2] in legal_files):
            if (move[1] in legal_ranks and move[3] in legal_ranks):
                return True
            else:
                return False
        else:
            return False
    elif (len(move) == 5):
        if(move[0] in legal_files and move[2] in legal_files):
            if (move[1] in legal_ranks and move[3] in legal_ranks):
                if (move[4] in legal_promotions):
                    return True
                return False
            else:
                return False
        else:
            return False
    else:
        return False

def processTutorialMove(move):
    global tutorialPuzzle
    if (not isValidMove(move)):
        return 5
    elif (isValidMove(move)):
        if (move == 'b3b8' and tutorialPuzzle.currentMove == 1):
            return 1
        elif (move == 'd4g7' and tutorialPuzzle.currentMove == 3):
            return 2
        elif (move == 'f7f8Q' and tutorialPuzzle.currentMove == 5):
            return 3
        else:
            return 4
    else:
        return 4

def pluralMoves(moves):
    if (moves == 1):
        return 'move'
    return 'moves'

client.run('ODAxODY3NzI3NDcxNzcxNjk4.YAm7hA.bj5rVkYl9LczVgh3pXmMt3IMM6o')