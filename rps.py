import matplotlib.pyplot as plt
import numpy as np
import random

class Game:
    def __init__(self):
        self.game_array = []

    def round_winner(self, player1, player2):
        move_1 = player1.move(self)
        move_2 = player2.move(self)

        print(move_1, move_2)

        if move_1 == move_2:
            self.game_array.append((0, move_1))

        elif move_1 == 1 and move_2 == -1:
            self.game_array.append((player1.index, move_1))
        elif move_1 == -1 and move_2 == 0:
            self.game_array.append((player1.index, move_1))
        elif move_1 == 0 and move_2 == 1:
            self.game_array.append((player1.index, move_1))
        else:
            self.game_array.append((player2.index, move_2))


    def render_games(self):
        value = 0
        x = []
        y = []
        for _, i in enumerate(self.game_array):
            value += i[0]
            x.append(_)
            y.append(value)

        plt.title("Matplotlib demo") 
        plt.xlabel("x axis caption") 
        plt.ylabel("y axis caption") 
        plt.plot(x,y) 
        plt.show()


class Bot:
    def __init__(self, index):
        self.index = index

    def happiness_function(self):
        pass

    def move(self, game):
        '''
        if game.game_array != []:
            return game.game_array[-1][1]
        else:
            return random.choice([-1, 0, 1])
        '''
        if game.game_array != []:
            amount = [0, 0, 0]
            for winner, move in game.game_array:
                if winner == 1:
                    amount[move + 1] += 1

            return (amount.index(max(amount)) - 1)
        else:
            return random.choice([-1, 0, 1])


class Player:
    def __init__(self, index):
        self.index = index

    def move(self, game):
        # choice = int(input('move: (-1, 0, 1): '))
        return random.choice([-1, 0, 1])


player = Player(1)
bot = Bot(-1)

game = Game()

for i in range(1000):
    game.round_winner(player, bot)

game.render_games()


