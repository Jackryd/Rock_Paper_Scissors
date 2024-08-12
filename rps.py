import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import os
import types
import csv

from tensorflow.keras.models import load_model

class Game:
    def __init__(self):
        # Game array saves tuples of each round. As per: (WINNING PLAYER, WINNING MOVE)
        self.game_array = []
        _, _, files = next(os.walk("games"))
        self.game_number = len(files) + 1
        with open(os.path.join('games', f'game{self.game_number}.csv'), 'w') as file:
            pass

    def round_winner(self, player1, player2):
        move_1 = player1.move(self)
        move_2 = player2.move(self)

        print(f'You chose {move_1}')
        print(f'The bot chose {move_2}')

        if move_1 == move_2:
            self.game_array.append((0, move_1))

        elif move_1 == -1 and move_2 == 1:
            self.game_array.append((player1.index, move_1))
        elif move_1 == 0 and move_2 == -1:
            self.game_array.append((player1.index, move_1))
        elif move_1 == 1 and move_2 == 0:
            self.game_array.append((player1.index, move_1))
        else:
            self.game_array.append((player2.index, move_2))

        file_name = os.path.join('games', f'game{self.game_number}.csv')
        with open(file_name, 'a', newline='') as file:
            writer = csv.writer(file)

            outcome = self.game_array[-1][0]
            action = self.game_array[-1][1] if outcome in [0, 1] else self.game_array[-1][1] + 1 if self.game_array[-1][1] < 1 else -1

            writer.writerow([outcome, action])

        return move_2


    def render_games(self):
        value = 0
        x = []
        y = []
        for _, i in enumerate(self.game_array):
            value += i[0]
            x.append(_)
            y.append(value)

        plt.title("Comparison of Algorithms") 
        plt.xlabel("Games Played") 
        plt.ylabel("Score") 
        plt.plot(x,y) 
        plt.show()

        return value

def random_move(self, game):
    return random.choice([-1, 0, 1])

def wsls(self, game):
    if len(game.game_array) == 0:
        return random.choice([-1, 0, 1])
    if game.game_array[-1][0] == self.index:
        return game.game_array[-1][1]
    else:
        if game.game_array[-1][1] == -1:
            return 0
        if game.game_array[-1][1] == 0:
            return 1
        else:
            return -1


def last_winning_move(self, game):
    if game.game_array != []:
        amount = [0, 0, 0]
        for winner, move in game.game_array:
            if winner == 1:
                amount[move + 1] += 1

        return (amount.index(max(amount)) - 1)
    else:
        return random.choice([-1, 0, 1])
    
def tit_for_tat(self, game):
    '''
    Interpretation of the tit for tat algorithm
    
    If player lost, choose what would have won last round
    If player drew, choose a random move 
    If player won, choose the same move
    '''

    if len(game.game_array) == 0:
        return random.choice([-1, 0, 1])

    if game.game_array[-1][0] == self.index:
        value = game.game_array[-1][1] + 1 if game.game_array[-1][1] < 1 else -1
        return value
    elif game.game_array[-1][0] != self.index:
        return game.game_array[-1][1]
    else:
        return random.choice([-1, 0, 1])

def frequency_analysis(self, game):
    '''
    choose what would defeat the opponent in the majority of the earlier games
    '''
    moves = {'-1' : 0, '0' : 0, '1' : 1}

    for index, move in (game.game_array):
        if index == self.index:
            moves[str(move)] += 1
        elif index != self.index:
            if move == -1:
                 moves['0'] += 1
            elif move == 0:
                 moves['1'] += 1
            else:
                 moves['-1'] += 1

    print(moves)

    return int(max(moves, key=moves.get))


def first_order_historical(self, game):

    if len(game.game_array) == 0:
        return random.choice([-1, 0, 1])

    last_move = game.game_array[-1]

    moves = {'-1' : 0, '0' : 0, '1' : 1}

    for _, (index, move) in enumerate(game.game_array):
        if (index, move) == last_move:
            if index == self.index:
                moves[str(move)] += 1
            elif index != self.index:
                if move == 0:
                    moves['-1'] += 1
                elif move == 1:
                    moves['0'] += 1
                else:
                    moves['1'] += 1

    return int(max(moves, key=moves.get))


def daniels_algorithm(self, game):
    for index, move in (game.game_array):
        if index == 0:
            return move
        
    return random.choice([-1, 0, 1])


def naslunds_algorithm(self, game):
    if len(game.game_array) == 0:
        return -1
    
    if game.game_array[-1][0] == self.index:
        return -1
    elif 0 != game.game_array[-1][0] != self.index:
        return 0
    else:
        return game.game_array[-1][1] + 1 if game.game_array[-1][0] < 1 else -1

def fnn(self, game, sequence_length=5, model_name='FNN_v1.h5'):
    # Simple fnn only designated to work as proof of principle
    file_name = os.path.join('games', f'game{game.game_number}.csv')
    data = pd.read_csv(file_name, header=None, names=['winner', 'player_action'])
    data = data.apply(pd.to_numeric, errors='coerce')
    data.dropna(inplace=True) # If earlier models fuck up, remove this line

    X = np.array(data)
    X = X[-(sequence_length + 1):-1]
    X = X.flatten()

    print(X)

    if X.shape[0] < sequence_length + 4:
        print(X, 'Too short')
        return random.choice([-1, 0, 1])

    model = load_model(os.path.join('models', model_name))
    predictions = model.predict(np.array([X]))

    print(predictions)
    print(np.where(predictions == max(predictions[0]))[0][0])

    return np.where(predictions == max(predictions[0]))[0][0]

def active_player(self, game):
    return self.selected_move

class Player:
    def __init__(self, index):
        self.index = index
        self.selected_move = 0

''' For facing Algorithms against each other
player_1 = Player(1)
player_1.move = types.MethodType(daniels_algorithm, player_1)

player_2 = Player(-1)
player_2.move = types.MethodType(naslunds_algorithm, player_2)

game = Game()


for i in range(100):
    game.round_winner(player_1, player_2)
    pass
    
value = game.render_games()
print(value)
'''
