# Dice Roll Game

import pygame
import random
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dice Roll Game')
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 48)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

# Function to roll a dice
def roll_dice():
    return random.randint(1, 6)

# Function to draw dice face
def draw_dice_face(value, x, y, size=50):
    pygame.draw.rect(screen, WHITE, (x, y, size, size))
    pygame.draw.rect(screen, BLACK, (x, y, size, size), 2)
    dot_size = 8
    if value == 1:
        pygame.draw.circle(screen, BLACK, (x + size//2, y + size//2), dot_size)
    elif value == 2:
        pygame.draw.circle(screen, BLACK, (x + size//4, y + size//4), dot_size)
        pygame.draw.circle(screen, BLACK, (x + 3*size//4, y + 3*size//4), dot_size)
    elif value == 3:
        pygame.draw.circle(screen, BLACK, (x + size//4, y + size//4), dot_size)
        pygame.draw.circle(screen, BLACK, (x + size//2, y + size//2), dot_size)
        pygame.draw.circle(screen, BLACK, (x + 3*size//4, y + 3*size//4), dot_size)
    elif value == 4:
        pygame.draw.circle(screen, BLACK, (x + size//4, y + size//4), dot_size)
        pygame.draw.circle(screen, BLACK, (x + 3*size//4, y + size//4), dot_size)
        pygame.draw.circle(screen, BLACK, (x + size//4, y + 3*size//4), dot_size)
        pygame.draw.circle(screen, BLACK, (x + 3*size//4, y + 3*size//4), dot_size)
    elif value == 5:
        pygame.draw.circle(screen, BLACK, (x + size//4, y + size//4), dot_size)
        pygame.draw.circle(screen, BLACK, (x + 3*size//4, y + size//4), dot_size)
        pygame.draw.circle(screen, BLACK, (x + size//2, y + size//2), dot_size)
        pygame.draw.circle(screen, BLACK, (x + size//4, y + 3*size//4), dot_size)
        pygame.draw.circle(screen, BLACK, (x + 3*size//4, y + 3*size//4), dot_size)
    elif value == 6:
        pygame.draw.circle(screen, BLACK, (x + size//4, y + size//4), dot_size)
        pygame.draw.circle(screen, BLACK, (x + 3*size//4, y + size//4), dot_size)
        pygame.draw.circle(screen, BLACK, (x + size//4, y + size//2), dot_size)
        pygame.draw.circle(screen, BLACK, (x + 3*size//4, y + size//2), dot_size)
        pygame.draw.circle(screen, BLACK, (x + size//4, y + 3*size//4), dot_size)
        pygame.draw.circle(screen, BLACK, (x + 3*size//4, y + 3*size//4), dot_size)

# Function to display text
def draw_text(text, x, y, color=BLACK, font=font):
    image = font.render(text, True, color)
    screen.blit(image, (x, y))

# Function to draw button
def draw_button(text, x, y, w, h, color=BLUE):
    pygame.draw.rect(screen, color, (x, y, w, h))
    pygame.draw.rect(screen, BLACK, (x, y, w, h), 2)
    button_text = font.render(text, True, BLACK)
    text_rect = button_text.get_rect(center=(x + w//2, y + h//2))
    screen.blit(button_text, text_rect)

def is_button_clicked(x, y, w, h, mouse_pos):
    mx, my = mouse_pos
    return x <= mx <= x + w and y <= my <= y + h

# Main game setup
def setup_game():
    players = 0
    player_names = []
    setup_done = False
    input_text = ""
    current_player = 0

    while not setup_done:
        screen.fill(GREEN)
        draw_text("Enter number of players (2-6):", 200, 200, BLACK, large_font)
        draw_text(input_text, 200, 250, BLACK, large_font)
        draw_button("Confirm", 350, 350, 100, 50)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == K_RETURN:
                    try:
                        players = int(input_text)
                        if 2 <= players <= 6:
                            setup_done = True
                        else:
                            input_text = ""
                    except ValueError:
                        input_text = ""
                else:
                    input_text += event.unicode
            if event.type == MOUSEBUTTONDOWN:
                if is_button_clicked(350, 350, 100, 50, event.pos):
                    try:
                        players = int(input_text)
                        if 2 <= players <= 6:
                            setup_done = True
                        else:
                            input_text = ""
                    except ValueError:
                        input_text = ""

        pygame.display.flip()

    # Now get names
    for i in range(players):
        input_text = ""
        name_done = False
        while not name_done:
            screen.fill(GREEN)
            draw_text(f"Enter name for Player {i+1}:", 200, 200, BLACK, large_font)
            draw_text(input_text, 200, 250, BLACK, large_font)
            draw_button("Confirm", 350, 350, 100, 50)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == K_RETURN:
                        if input_text.strip():
                            player_names.append(input_text.strip())
                            name_done = True
                        else:
                            input_text = ""
                    else:
                        input_text += event.unicode
                if event.type == MOUSEBUTTONDOWN:
                    if is_button_clicked(350, 350, 100, 50, event.pos):
                        if input_text.strip():
                            player_names.append(input_text.strip())
                            name_done = True
                        else:
                            input_text = ""

            pygame.display.flip()

    return players, player_names

# Main game loop
def main():
    players, player_names = setup_game()
    scores = [0] * players
    rounds = 5  # Play 5 rounds
    current_round = 1

    running = True
    while running and current_round <= rounds:
        screen.fill(WHITE)

        # Display round
        draw_text(f"Round {current_round}", WIDTH//2 - 50, 20, BLACK, large_font)

        # Display scores
        for i in range(players):
            draw_text(f"{player_names[i]}: {scores[i]}", 50, 80 + i*40)

        # Roll dice
        rolls = [roll_dice() for _ in range(players)]

        # Display dice
        for i, roll in enumerate(rolls):
            draw_text(f"{player_names[i]}:", 300, 80 + i*80)
            draw_dice_face(roll, 450, 80 + i*80)

        # Determine winner of round
        max_roll = max(rolls)
        winners = [i for i, r in enumerate(rolls) if r == max_roll]
        if len(winners) == 1:
            winner = winners[0]
            scores[winner] += 1
            draw_text(f"Round Winner: {player_names[winner]}!", 300, 80 + players*80, GREEN, large_font)
        else:
            draw_text("It's a tie!", 300, 80 + players*80, YELLOW, large_font)

        draw_button("Next Round", 350, 500, 120, 50)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    waiting = False
                if event.type == MOUSEBUTTONDOWN:
                    if is_button_clicked(350, 500, 120, 50, event.pos):
                        waiting = False
                        current_round += 1

    # Game over, show final scores
    screen.fill(WHITE)
    draw_text("Game Over!", WIDTH//2 - 100, 100, RED, large_font)
    max_score = max(scores)
    overall_winners = [i for i, s in enumerate(scores) if s == max_score]
    if len(overall_winners) == 1:
        winner = overall_winners[0]
        draw_text(f"Overall Winner: {player_names[winner]} with {scores[winner]} points!", WIDTH//2 - 200, 200, GREEN, large_font)
    else:
        draw_text("It's a tie!", WIDTH//2 - 50, 200, YELLOW, large_font)

    draw_button("Play Again", 350, 400, 120, 50)
    draw_button("Quit", 350, 470, 120, 50)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                waiting = False
            if event.type == MOUSEBUTTONDOWN:
                if is_button_clicked(350, 400, 120, 50, event.pos):
                    main()  # Restart game
                elif is_button_clicked(350, 470, 120, 50, event.pos):
                    waiting = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
