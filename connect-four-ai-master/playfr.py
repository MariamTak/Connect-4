import random
import copy
import sys
import pygame
from pygame.locals import *
PLAYER1 = 'player1'
PLAYER2 = 'player2'
BOARDWIDTH = 7  # how many spaces wide the board is
BOARDHEIGHT = 6  # how many spaces tall the board is

SPACESIZE = 50  # size of the tokens and individual board spaces in pixels

FPS = 30  # frames per second to update the screen
WINDOWWIDTH = 640  # width of the program's window, in pixels
WINDOWHEIGHT = 480  # height in pixels

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * SPACESIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - BOARDHEIGHT * SPACESIZE) / 2)

WHITE = (255, 255, 255)
GRAY = (201, 201, 201)
BGCOLOR = GRAY
TEXTCOLOR = WHITE

BLUE = 'blue'
BLACK = 'black'
EMPTY = None

def run():
    global FPSCLOCK, DISPLAYSURF, BLUEPILERECT, BLACKPILERECT,BLUETOKENIMG
    global BLACKTOKENIMG, BOARDIMG, ARROWIMG, ARROWRECT, BLUEWINNERIMG
    global BLACKWINNERIMG, WINNERRECT, TIEWINNERIMG

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Connect Four')

    BLUEPILERECT = pygame.Rect(int(SPACESIZE / 2), WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE, SPACESIZE)
    BLACKPILERECT = pygame.Rect(WINDOWWIDTH - int(3 * SPACESIZE / 2), WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE,
                                SPACESIZE)
    BLUETOKENIMG = pygame.image.load('images/4row_blue.png')
    BLUETOKENIMG = pygame.transform.smoothscale(BLUETOKENIMG, (SPACESIZE, SPACESIZE))
    BLACKTOKENIMG = pygame.image.load('images/4row_black.png')
    BLACKTOKENIMG = pygame.transform.smoothscale(BLACKTOKENIMG, (SPACESIZE, SPACESIZE))
    BOARDIMG = pygame.image.load('images/4row_board.png')
    BOARDIMG = pygame.transform.smoothscale(BOARDIMG, (SPACESIZE, SPACESIZE))

    BLUEWINNERIMG = pygame.image.load('images/BLUE.jpg')
    BLACKWINNERIMG = pygame.image.load('images/BLACK.png')
    TIEWINNERIMG = pygame.image.load('images/TIE.jpg')
    WINNERRECT = BLUEWINNERIMG.get_rect()
    WINNERRECT.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))



def processGameOver(winner, board):
    winnerImg = BLUEWINNERIMG if winner == PLAYER1 else BLACKWINNERIMG if winner == PLAYER2 else TIEWINNERIMG

    while True:
        # Keep looping until the player clicks the mouse or quits.
        drawBoard(board)
        DISPLAYSURF.blit(winnerImg, WINNERRECT)
        pygame.display.update()
        FPSCLOCK.tick()
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                return

def getNewBoard():
    board = []
    for x in range(BOARDWIDTH):
        board.append([EMPTY] * BOARDHEIGHT)
    return board


def makeMove(board, player, column):
    lowest = getLowestEmptySpace(board, column)
    if lowest != -1:
        board[column][lowest] = player


def drawBoard(board, extraToken=None):
    DISPLAYSURF.fill(BGCOLOR)

    # draw tokens
    spaceRect = pygame.Rect(0, 0, SPACESIZE, SPACESIZE)
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            spaceRect.topleft = (XMARGIN + (x * SPACESIZE), YMARGIN + (y * SPACESIZE))
            if board[x][y] == BLUE:
                DISPLAYSURF.blit(BLUETOKENIMG, spaceRect)
            elif board[x][y] == BLACK:
                DISPLAYSURF.blit(BLACKTOKENIMG, spaceRect)

    # draw the extra token
    if extraToken is not None:
        if extraToken['color'] == BLUE:
            DISPLAYSURF.blit(BLUETOKENIMG, (extraToken['x'], extraToken['y'], SPACESIZE, SPACESIZE))
        elif extraToken['color'] == BLACK:
            DISPLAYSURF.blit(BLACKTOKENIMG, (extraToken['x'], extraToken['y'], SPACESIZE, SPACESIZE))

    # draw board over the tokens
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            spaceRect.topleft = (XMARGIN + (x * SPACESIZE), YMARGIN + (y * SPACESIZE))
            DISPLAYSURF.blit(BOARDIMG, spaceRect)

    # draw the BLUE and black tokens off to the side
    DISPLAYSURF.blit(BLUETOKENIMG, BLUEPILERECT)  # BLUE on the left
    DISPLAYSURF.blit(BLACKTOKENIMG, BLACKPILERECT)  # black on the right


def updateDisplay():
    pygame.display.update()
    FPSCLOCK.tick()

def getHumanInteraction(board, player_color):
    draggingToken = False
    tokenx, tokeny = None, None
    column = None

    while column is None:
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and not draggingToken:
                # start of dragging on token pile.
                if player_color == BLUE and BLUEPILERECT.collidepoint(event.pos):
                    draggingToken = True
                    tokenx, tokeny = event.pos
                elif player_color == BLACK and BLACKPILERECT.collidepoint(event.pos):
                    draggingToken = True
                    tokenx, tokeny = event.pos
            elif event.type == MOUSEMOTION and draggingToken:
                # update the position of the token being dragged
                tokenx, tokeny = event.pos
            elif event.type == MOUSEBUTTONUP and draggingToken:
                # let go of the token being dragged
                if tokeny < YMARGIN and tokenx > XMARGIN and tokenx < WINDOWWIDTH - XMARGIN:
                    # let go at the top of the screen.
                    column = int((tokenx - XMARGIN) / SPACESIZE)
                    draggingToken = False  # Reset the flag here

        if tokenx is not None and tokeny is not None:
            drawBoard(board, {'x': tokenx - int(SPACESIZE / 2), 'y': tokeny - int(SPACESIZE / 2), 'color': player_color})
        else:
            drawBoard(board)

        pygame.display.update()
        FPSCLOCK.tick()

    return column

def dropToken(board, column, color):
    lowest_empty = getLowestEmptySpace(board, column)
    if lowest_empty != -1:
        board[column][lowest_empty] = color


def getLowestEmptySpace(board, column):
    for y in range(BOARDHEIGHT - 1, -1, -1):
        if board[column][y] == EMPTY:
            return y
    return -1
def checkForWin(board, color):
    # Check horizontal spaces
    for y in range(BOARDHEIGHT):
        for x in range(BOARDWIDTH - 3):
            if board[x][y] == color and board[x + 1][y] == color and board[x + 2][y] == color and board[x + 3][y] == color:
                return True

    # Check vertical spaces
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT - 3):
            if board[x][y] == color and board[x][y + 1] == color and board[x][y + 2] == color and board[x][y + 3] == color:
                return True

    # Check diagonal spaces (from top-left to bottom-right)
    for x in range(BOARDWIDTH - 3):
        for y in range(BOARDHEIGHT - 3):
            if board[x][y] == color and board[x + 1][y + 1] == color and board[x + 2][y + 2] == color and board[x + 3][y + 3] == color:
                return True

    # Check diagonal spaces (from top-right to bottom-left)
    for x in range(BOARDWIDTH - 3):
        for y in range(3, BOARDHEIGHT):
            if board[x][y] == color and board[x + 1][y - 1] == color and board[x + 2][y - 2] == color and board[x + 3][y - 3] == color:
                return True

    return False

def isBoardFull(board):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == EMPTY:
                return False
    return True

if __name__ == "__main__":
    print("Welcome to Connect Four!")

    run()
    while True:
        # Set up a blank board data structure.
        game_board = getNewBoard()
        drawBoard(game_board)
        updateDisplay()

        while True:
            # Player 1's turn (BLUE)
            column = getHumanInteraction(game_board, BLUE)
            dropToken(game_board, column, BLUE)

            if checkForWin(game_board, BLUE):
                processGameOver(PLAYER1, game_board)
                break
            elif isBoardFull(game_board):
                processGameOver(None, game_board)
                break

            # Player 2's turn (BLACK)
            column = getHumanInteraction(game_board, BLACK)
            dropToken(game_board, column, BLACK)

            if checkForWin(game_board, BLACK):
                processGameOver(PLAYER2, game_board)
                break
            elif isBoardFull(game_board):
                processGameOver(None, game_board)
                break

            drawBoard(game_board)
            updateDisplay()