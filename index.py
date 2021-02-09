import discord
from discord.ext import commands, tasks
import os, shutil
import subprocess
import csv
import random
from operator import itemgetter
from Puzzle import Puzzle
from Fen import Fen
from Blast import Blast
from main import mainFTP

client = commands.Bot(command_prefix = '.')
tutorialPuzzle = Puzzle(['NgJOw', '8/p4P2/8/8/3B4/1R6/8/8 b - - 0 1', 'a7a6 b3b8 a6a5 d4g7 a5a4 f7f8q', '1303', '76', '86', '353', 'endgame mate mateIn2 short', 'https://lichess.org/sn1G465d#87'])
newBlast = Blast(0)
tutorialMode = False
blastMode = False

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
newPuzzle = Puzzle(getNewPuzzle())
newPuzzle.complete = True

@client.event
async def on_ready():
    print('Bot is Ready')

@client.event
async def on_message(message):
    global newPuzzle
    global tutorialPuzzle
    global newBlast
    global tutorialMode
    global blastMode
    if (message.content.startswith('.help')):
        blastMode = False
        tutorialMode = True
        await message.channel.send('Hello, I am the Chess Puzzle Blaster Discord bot.')
        await message.channel.send('To play my puzzles you must suggest moves with the .move command and provide the initial square of the piece you would like to move, followed by its destination square. Remember, each square of the board can be identified using an alphanumerical system. Here is an image for reference:')
        await message.channel.send(file=discord.File('images/tutorial_board.png'))
        await message.channel.send('You can try this out with this puzzle right here. You can move your rook to b8 with the move command. The current location is b3 and the desired destination is b8 so your move command should look like: ".move b3b8" Try executing that command now')
        mainFTP(tutorialPuzzle.fen.fen_array)
        await message.channel.send(file=discord.File('./output/result.png'))

        #Directory cleanup
        os.system('rm -rf ./output/*')

    if (message.content.startswith('.hint')):
        await message.channel.send('Try looking at the ' + str(newPuzzle.moves[newPuzzle.currentMove][0:2]) + ' square')

    if (message.content.startswith('.chess')):
        if (blastMode):
            await message.channel.send('There is an active puzzle blast with ' + str(newBlast.puzzleMax - newBlast.currentPuzzle) + ' puzzles to go')
        elif (not newPuzzle.complete):
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
        os.system('rm -rf ./output/*')
    
    if (message.content.startswith('.blast')):
        try:
            blastSize = int(message.content.split(' ')[1])
        except:
            await message.channel.send('Invalid blast command: Use syntax .blast X to specify the number of puzzles in your blast')
            return
        if (blastSize < 3):
            await message.channel.send('Minimum blast size is 3 puzzles, try again')
            return
        #Enter the Puzzle Blasting Realm
        blastMode = True
        #Get number of puzzles and Initialize blast Session
        newBlast = Blast(blastSize)
        await message.channel.send('Entering the Blasting Realm: ' + str(newBlast.puzzleMax) + ' Puzzle Blast')
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
        os.system('rm -rf ./output/*')

    if (message.content.startswith('.move')):
        try:
            move = message.content.split(' ')[1]
        except:
            await message.channel.send('No Move specified: Use syntax .move a1b2')
            return
        if (tutorialMode):
            if (processTutorialMove(move) == 1):
                await message.channel.send('Nice job. As you can see you have moved your rook to b8 and your opponent has moved their pawn to a5. Whenever you enter the correct move, I will execute it and your opponents response move, then I will send you a new image of the board. Now try moving your bishop to g7. This time you\'ll have to figure out the command on your own.')
                #Execute User Move
                tutorialPuzzle.makeMove(tutorialPuzzle.moves[tutorialPuzzle.currentMove])
                #Execute Counter Move
                tutorialPuzzle.makeMove(tutorialPuzzle.moves[tutorialPuzzle.currentMove])
                #Process and send new board image
                mainFTP(tutorialPuzzle.fen.fen_array)
                await message.channel.send(file=discord.File('./output/result.png'))
                #Directory cleanup
                os.system('rm -rf ./output/*')
                return
            elif (processTutorialMove(move) == 2):
                await message.channel.send('A brilliant move! You\'ll be a grandmaster in no time. Now for the final lesson. In chess when a pawn makes it to the other side of the board you can promote it to be a Queen (q), a Rook (r), a Bishop (b) or a Knight (n). In order to execute a pawn promotion, you must use the move command to move your pawn 1 square forward, but add the corresponding letter of the piece you would like to promote to at the end of the command (ex. a7a8n). Now try promoting your Pawn to a Queen!')
                #Execute User Move
                tutorialPuzzle.makeMove(tutorialPuzzle.moves[tutorialPuzzle.currentMove])
                #Execute Counter Move
                tutorialPuzzle.makeMove(tutorialPuzzle.moves[tutorialPuzzle.currentMove])
                #Process and send new board image
                mainFTP(tutorialPuzzle.fen.fen_array)
                await message.channel.send(file=discord.File('./output/result.png'))
                #Directory cleanup
                os.system('rm -rf ./output/*')
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
                os.system('rm -rf ./output/*')
                return
            elif (processTutorialMove(move) == 4):
                await message.channel.send('Incorrect move')
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
            if (blastMode):
                userIndex = next((index for (index, scoreCard) in enumerate(newBlast.scoreBoard) if scoreCard['name'] == message.author.name), None)
                if userIndex == None:
                    #Entry does not exist
                    newBlast.scoreBoard.append({
                        'name': message.author.name,
                        'score': 1
                    })
                else:
                    newBlast.scoreBoard[userIndex]['score'] += 1
                print(newBlast.scoreBoard)
            #Update Moves to win
            newPuzzle.movesToWin -= 1
            #Execute User Move
            newPuzzle.makeMove(newPuzzle.moves[newPuzzle.currentMove])
            #Check if Puzzle is complete
            if (newPuzzle.currentMove == len(newPuzzle.moves)):
                if (blastMode):
                    if (newBlast.currentPuzzle == newBlast.puzzleMax):
                        #Blast complete announce winners
                        blastMode = False
                        await message.channel.send('Blast complete, Post Game Summary:')
                        sortedScoreBoard = sorted(newBlast.scoreBoard, key=itemgetter('score'), reverse=True)
                        summary = ''
                        for i, scoreCard in enumerate(sortedScoreBoard):
                            summary += '{position}. {user} found {score} {moves} \n'.format(position=str(i + 1), user=scoreCard['name'], score=scoreCard['score'], moves=pluralMoves(scoreCard['score']))
                        await message.channel.send(summary) 
                        return
                    else:
                        #Puzzle complete, blast continues
                        await message.channel.send('Puzzle ' + str(newBlast.currentPuzzle) + ' complete, Next Puzzle: ')
                        #Update Blast
                        newBlast.currentPuzzle += 1
                        #Get New Puzzle
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
                        os.system('rm -rf ./output/*')
                        return
                await message.channel.send(message.author.name + ' Win!')
                mainFTP(newPuzzle.fen.fen_array)
                await message.channel.send(file=discord.File('./output/result.png'))
                #Directory cleanup
                os.system('rm -rf ./output/*')
                newPuzzle.complete = True
                return
            #Execute Counter Move
            newPuzzle.makeMove(newPuzzle.moves[newPuzzle.currentMove])
            #Check if Puzzle is complete
            if (newPuzzle.currentMove == len(newPuzzle.moves)):
                if (blastMode):
                    if (newBlast.currentPuzzle == newBlast.puzzleMax):
                        #Blast complete announce winners
                        blastMode = False
                        await message.channel.send('Blast complete, Post Game Summary:')
                        sortedScoreBoard = sorted(newBlast.scoreBoard, key=itemgetter('score'), reverse=True)
                        summary = ''
                        for i, scoreCard in enumerate(sortedScoreBoard):
                            summary += '{position}. {user} found {score} {moves} \n'.format(position=str(i + 1), user=scoreCard['name'], score=scoreCard['score'], moves=pluralMoves(scoreCard['score']))
                        await message.channel.send(summary) 
                        return
                    else:
                        #Puzzle complete, blast continues
                        await message.channel.send('Puzzle ' + str(newBlast.currentPuzzle) + ' complete, Next Puzzle: ')
                        #Update Blast
                        newBlast.currentPuzzle += 1
                        #Get New Puzzle
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
                        os.system('rm -rf ./output/*')
                        return
                await message.channel.send(message.author.name + ' Win!')
                mainFTP(newPuzzle.fen.fen_array)
                await message.channel.send(file=discord.File('./output/result.png'))
                #Directory cleanup
                os.system('rm -rf ./output/*')
                newPuzzle.complete = True
                return
            
            #Give remaining moves and resend puzzle
            await message.channel.send('Correct, Find ' + str(newPuzzle.movesToWin) + ' ' + pluralMoves(newPuzzle.movesToWin) + ' to complete the puzzle')
            mainFTP(newPuzzle.fen.fen_array)

            await message.channel.send(file=discord.File('./output/result.png'))

            #Directory cleanup
            os.system('rm -rf ./output/*')
        else:
            await message.channel.send('Incorrect move, try again')

def isValidMove(move):
    legal_files = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'}
    legal_ranks = { '1', '2', '3', '4', '5', '6', '7', '8'}
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
        elif (move == 'f7f8q' and tutorialPuzzle.currentMove == 5):
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