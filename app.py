import pygame
import sys
import numpy as np
import types
import time
import csv

from rps import *

# Initiates variables for Pygame
pygame.init()

FONT = pygame.font.Font("freesansbold.ttf", 32)

FPS = 60
HEIGHT, WIDTH = 0.8 * 1080, 0.8 * 1920
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")
bg = pygame.image.load("screen.jpg")
DEFAULT_IMAGE_SIZE = (WIDTH, HEIGHT)
bg = pygame.transform.scale(bg, DEFAULT_IMAGE_SIZE)


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 90, 200, 255)

def render_button(button_text, rect, x, y, text_colour, button_colour1, button_colour2):

    collide = False

    Rect = rect

    if Rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(WIN, button_colour1, Rect, border_radius=3)
        text = FONT.render(button_text, True, text_colour, button_colour1)
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        collide = True

    else:
        pygame.draw.rect(WIN, button_colour2, Rect, border_radius=3)
        text = FONT.render(button_text, True, text_colour, button_colour2)
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
    textRect = text.get_rect()
    textRect.center = (x,y,)
    WIN.blit(text, textRect)
    pygame.display.flip()

    return collide

def render_winner_text(text, x, y, text_colour=BLACK):
    text = FONT.render(text, True, text_colour)
    textRect = text.get_rect()
    textRect.center = (x,y)
    WIN.blit(text, textRect)
    pygame.display.flip()

def save_score(algorithm, game=None):
    if game.game_array != []:
        # value = game.render_games()

        amount_wins = 0
        amount_games = 0

        for winner, choice in game.game_array:
            if winner == -1:
                amount_wins += 1
            if winner != 0:
                amount_games += 1
        
        # percentage = round(100 * amount_wins/amount_games, 2)

        with open('text.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([algorithm.__name__, amount_games, amount_wins])


def main():
    # Initiate game variables
    run = True
    game = Game()
    player = Player(1)
    player.move = types.MethodType(active_player, player)
    bot = Player(-1)
    bot.move = types.MethodType(frequency_analysis, bot)
    clock = pygame.time.Clock()
    WIN.blit(bg, (0, 0))
    game_active = False
    alternatives = {'rock' : -1, 'paper' : 0, 'scissors' : 1}
    buttons = {'rock' : None, 'paper' : None, 'scissors' : None}
    # buttons = {alternative : None for alternative in alternatives}

    for i, name in enumerate(alternatives):
        Rect = pygame.Rect(0, 0, 200, 60)
        Rect.center = ((i + 0.5) * (WIDTH / 3), HEIGHT / 2)
        buttons[name] = Rect

    while run:

        clock.tick(FPS)

        if game_active:
            bot_move = game.round_winner(player, bot)
            for i in alternatives:
                if alternatives[i] == bot_move:
                    render_winner_text(f'The Computer chose {i}', WIDTH/2, 1/4*HEIGHT)
                    break
            if game.game_array[-1][0] == 1:
                render_winner_text('YOU WIN!', WIDTH/2, 1/3*HEIGHT)
            elif game.game_array[-1][0] == -1:
                render_winner_text(f'YOU LOSE!', WIDTH/2, 1/3*HEIGHT)
            else:
                render_winner_text(f'DRAW!', WIDTH/2, 1/3*HEIGHT)

            time.sleep(1)
            game_active = False

        for event in pygame.event.get():
            if game_active == False:
                for i, name in enumerate(buttons):
                    if render_button(name, buttons[name], (i + 0.5) * (WIDTH / 3), HEIGHT / 2, WHITE, BLUE, RED) and game_active == False:
                        pass
                for i, name in enumerate(buttons):
                    if buttons[name].collidepoint(pygame.mouse.get_pos()) and game_active == False:
                        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                        break
                    else:
                        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, name in enumerate(alternatives):
                        Rect = pygame.Rect(0, 0, 200, 60)
                        Rect.center = ((i + 0.5) * (WIDTH / 3), HEIGHT / 2)
                        if Rect.collidepoint(pygame.mouse.get_pos()):
                            WIN.blit(bg, (0, 0))
                            player.selected_move = alternatives[name]
                            game_active = True
                            break

            if event.type == pygame.KEYDOWN:
                pass
            if event.type == pygame.QUIT:
                pygame.quit()
                # name = input('To save, type name: ')
                save_score(algorithm=bot.move, game=game)
                sys.exit()

if __name__ == "__main__":
    main()