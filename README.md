# Rock Paper Scissors: A Game Theoretical Approach

This repository represents my endeavour of exploring how different algorithms can be implemented to play rock paper scissors. The ultimate goal of this project is to develop a mathematical model which has the ability to find complex patterns which human beings seem to follow when playing this very elementary game. This project is still a *work in progress* and many future algorithms are planned - with a special focus on machine learning algorithms. Bellow is a brief summary of what this project contains.

## The Actual Game

I have created a simple Pygame GUI which in a simple manner allows the player to play the game of rock paper scissors by chosing a move and getting response to what the opposite player choses. Here, the player has the ability to chose what algorithm he wants to face. For every round which is played, the program saves both the winner of the round and what move that player used. It is from this data that the models infer there decisions. I have also developed a framework which allows the user to make different algorithms face each other to decide which the ultimate algorithm is.


## The *Regular* Algorithms

These algorithms are primarily based on **game theory** and I have for example implemented tit-for-tat and win-stay lose-switch. Other algorithms include a frequency analysis, which looks at what would have worked most of the previous rounds, and a historical analysis which looks at the past game which looks exactly like this and plays the move which would have won then. I have also - in collaboration with some friends - implemented some more humorous algorithms.

## The Machine Learning Algorithms

Finally, I have also been working on implementing some machine learning algorithms. I have used data from this [https://osf.io/wmb2h/](experiment).This far, I have only implemented a simple feed forward neural network which processes the past 5 rounds and tries to find patterns in the players ability. Currently, the best model has achieved a training accuracy of ~60%, but only an evaluation accuracy of ~38%, indicating that it is severely overfitting and is only *slightly* better than random guessing. However, the currently implemented model is *very* simple and merely serves as a proof of principle that the model can be implemented. Future plans include developing a LSTM and a random forest model which might actually find some more complex patterns in the data. 