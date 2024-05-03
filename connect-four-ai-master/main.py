import random, copy, sys, pygame
from pygame.locals import *
import subprocess

yellow = (241, 235, 144)
WHITE = (255, 255, 255)
red = (196, 0, 7, 255)
X = 640
Y = 480
run = True

TEXTCOLOR = WHITE
EMPTY = None
PLAYER1 = 'Player 1'
PLAYER2 = 'Player 2'

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((X, Y))
pygame.display.set_caption('Connect Four')

# Load images
PLAYA = pygame.image.load('images/playa.png')
PLAYF = pygame.image.load('images/playf.png')
PLAYFF = PLAYF.get_rect()
PLAYAA = PLAYA.get_rect()
PLAYFF.center = (int(X / 2), int(Y / 2))
PLAYAA.center = (int(X / 2), int(Y / 1.2))
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Connect four', True, yellow, red)
textRect = text.get_rect()
textRect.center = (X // 2, Y // 6)

# Define the button areas
button_rect_ff = PLAYFF
button_rect_aa = PLAYAA

# Game loop
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

        if event.type == MOUSEBUTTONDOWN:
            if button_rect_ff.collidepoint(event.pos) or button_rect_ff.collidepoint(event.pos):
                pygame.quit()

                process = subprocess.Popen(['python', 'playfr.py'])
                output, errors = process.communicate()
        if event.type == MOUSEBUTTONDOWN:
            if button_rect_aa.collidepoint(event.pos) or button_rect_aa.collidepoint(event.pos):
                pygame.quit()

                process = subprocess.Popen(['python', 'playai.py'])
                output, errors = process.communicate()

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((241, 235, 144))

    # Draw the background
    screen.blit(background, (0, 0))

    # Draw the text on top of the background
    screen.blit(text, textRect)
    screen.blit(PLAYF, PLAYFF)
    screen.blit(PLAYA, PLAYAA)
    pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()
