# Dice Roll Game

import pygame
import random
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# store player names
players = int(input("Enter number of players (2-6): "))
player_names = []
for i in range(players):
    name = input(f"Enter name for Player {i+1}: ")
    player_names.append(name)

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dice Roll Game')
font = pygame.font.Font(None, 74)

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Function to roll a dice
def roll_dice():
    return random.randint(1, 6)

# Function to display text
def draw_text(text,x,y):
    image = font.render(text, True, BLACK)
    screen.blit(image, (x, y))
    pygame.display.flip()


def draw_button(text,x,y,w,h):
    pygame.draw.rect(screen, BLUE, (x, y, w, h))
    button_font = pygame.font.Font(None, 36)
    button_text = button_font.render(text, True, BLACK)
    screen.blit(button_text, (x + 10, y + 10))
    pygame.display.flip()
    
def is_button_clicked(x,y,w,h,mouse_pos):
    mx,my = mouse_pos
    return x <= mx <= x + w and y <= my <= y + h

# Main game loop
def main():
    global players, player_names
    #players = int(input("Enter number of players (2-6): "))
    rolls = [roll_dice() for _ in range(players)]
    winner = rolls.index(max(rolls)) + 1
   
    # Game loop
    running = True
    while running:
        screen.fill(WHITE)# Clear screen

        for i,roll in enumerate(rolls):
            draw_text(f"{player_names[i]}: {roll}", 250, 50 + i*60)# Display each player's roll

        draw_text(f"Winner: {player_names[winner-1]}!", 250, 50 + players*60)# Display winner

        for event in pygame.event.get():# Event handling
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if is_button_clicked(350, 500, 100, 50, event.pos):
                    rolls = [roll_dice() for _ in range(players)]
                    winner = rolls.index(max(rolls)) + 1
        draw_button("Roll Dice", 350, 500, 100, 50)# Draw roll button
