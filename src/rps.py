import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random, os, types, csv

from tensorflow.keras.models import load_model

ROCK = 0
PAPER = 1
SCISSORS = 2

class Game: pass

class Algorithm:
    def __init__(self, weights=np.ones(3)/3):
        self.name = ""
        self.weights = weights
    def make_move(self, game):
        return np.random.choice([ROCK, PAPER, SCISSORS], p=self.weights)

class WinStayLoseSwap(Algorithm):
    def __init__(self, weights=np.ones(3)/3):
        self.name = "Win-Stay Lose-Swap"
        self.weights = weights
    def make_move(self, game:Game):
        prev_moves = game.player1_moves if self == game.player1 else game.player2_moves
        if len(prev_moves) == 0:
            return np.random.choice([ROCK, PAPER, SCISSORS], p=self.weights)
        if game.winner_array[-1] == self:
            return prev_moves[-1]
        return (prev_moves[-1] + 1) % 3

class ActivePlayer(Algorithm):
    def __init__(self, name:str):
        self.name = name
    def make_move(self, game:Game):
        return int(input())

class FrequencyAnalysis(Algorithm):
    def __init__(self, weights):
        self.name = "Frequency Analysis"
        self.weights = weights
    
    def make_move(self, game:Game):
        '''
        choose what would defeat the opponent in the majority of the earlier games
        '''
        opp_prev_moves = game.player2_moves if self == game.player1 else game.player1_moves
        if len(opp_prev_moves) == 0:
            return np.random.choice([ROCK, PAPER, SCISSORS], p=self.weights)
        c = np.argmax(np.bincount(opp_prev_moves.astype(int)))
        return (c + 1) % 3

class AutoregressiveAlgorithm(Algorithm):
    def __init__(self):
        self.name = "Autoregressive Model"
        self.weights = weights

    def make_move(self, game:Game):
        pass

class Game:
    def __init__(self, player1:Algorithm, player2:Algorithm):
        self.player1 = player1
        self.player2 = player2
        self.winner_array = np.array([])
        self.player1_moves = np.array([])
        self.player2_moves = np.array([])

    def reset_game(self):
        self.winner_array = np.array([])
        self.player1_moves = np.array([])
        self.player2_moves = np.array([])

    def simulate_round(self):
        move_1 = self.player1.make_move(self)
        move_2 = self.player2.make_move(self)
        self.player1_moves = np.append(self.player1_moves, move_1)
        self.player2_moves = np.append(self.player2_moves, move_2)
        if move_1 == move_2:
            self.winner_array = np.append(self.winner_array, None) 
            return None
        if (move_1 == PAPER and move_2 == ROCK) or (move_1 == ROCK and move_2 == SCISSORS) or (move_1 == SCISSORS and move_2 == PAPER):
            self.winner_array = np.append(self.winner_array, self.player1) 
            return self.player1
        self.winner_array = np.append(self.winner_array, self.player2) 
        return self.player2

    def simulate_game(self, n_rounds:int):
        for i in range(n_rounds):
            self.simulate_round()

    def analyze_game(self):
        total = len(self.winner_array)
        p1_wins = np.sum(self.winner_array == self.player1)
        p2_wins = np.sum(self.winner_array == self.player2) 
        ties = np.sum(self.winner_array == None)
        
        print(f"{self.player1.name}: {p1_wins}/{total} ({p1_wins/total:.1%})")
        print(f"{self.player2.name}: {p2_wins}/{total} ({p2_wins/total:.1%})")
        print(f"Ties: {ties}/{total} ({ties/total:.1%})")