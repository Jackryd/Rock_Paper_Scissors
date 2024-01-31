import pygame
import sys
import numpy as np
import types
import time

from rps import Player, Game, random_move, active_player

# Initiates variables for Pygame
pygame.init()

FONT = pygame.font.Font("freesansbold.ttf", 32)

FPS = 60
HEIGHT, WIDTH = 1080, 1920
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")
bg = pygame.image.load("screen.jpg")
DEFAULT_IMAGE_SIZE = (WIDTH, HEIGHT)
bg = pygame.transform.scale(bg, DEFAULT_IMAGE_SIZE)


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 90, 200, 255)

def render_button(button_text, x, y, text_colour, button_colour1, button_colour2):

    collide = False

    Rect = pygame.Rect(0, 0, 200, 60)
    Rect.center = (
        x,
        y,
    )

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

def main():
    # Initiate game variables
    run = True
    game = Game()
    player = Player(1)
    player.move = types.MethodType(active_player, player)
    bot = Player(-1)
    bot.move = types.MethodType(random_move, bot)
    clock = pygame.time.Clock()
    WIN.blit(bg, (0, 0))
    game_active = False
    buttons = {'rock' : -1, 'paper' : 0, 'scissors' : 1}

    # Create a loop that will run until the game is exited
    while run:
        # Change the FPS of the game

        clock.tick(FPS)
        # Check every event which occurs in the game

        if game_active:
            bot_move = game.round_winner(player, bot)
            for i in buttons:
                if buttons[i] == bot_move:
                    render_winner_text(f'The Computer chose {i}', WIDTH/2, 1/4*HEIGHT)
                    break
            if game.game_array[-1][0] == 1:
                render_winner_text('YOU WIN!', WIDTH/2, 1/3*HEIGHT)
            elif game.game_array[-1][0] == -1:
                render_winner_text(f'YOU LOSE', WIDTH/2, 1/3*HEIGHT)
            else:
                render_winner_text(f'DRAW!', WIDTH/2, 1/3*HEIGHT)
            

            time.sleep(1)
            game_active = False

        for event in pygame.event.get():
            if game_active == False:
                for i, name in enumerate(buttons):
                    if render_button(name, (i + 0.5) * (WIDTH / 3), HEIGHT / 2, WHITE, BLUE, RED) and game_active == False:
                        # break
                        pass

                # If the game isn't active
                if event.type == pygame.MOUSEBUTTONDOWN:
                    WIN.blit(bg, (0, 0))
                    for i, name in enumerate(buttons):
                        Rect = pygame.Rect(0, 0, 200, 60)
                        Rect.center = ((i + 0.5) * (WIDTH / 3), HEIGHT / 2)
                        if Rect.collidepoint(pygame.mouse.get_pos()):
                            player.selected_move = buttons[name]
                            game_active = True
                            break

            if event.type == pygame.KEYDOWN:
                pass
            if event.type == pygame.QUIT:
                sys.exit()

if __name__ == "__main__":
    main()