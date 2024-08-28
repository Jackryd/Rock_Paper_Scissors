# Rock Paper Scissors: A Game Theoretical Approach

This repository represents my endeavour of exploring how different algorithms can be implemented to play rock paper scissors. The ultimate goal of this project is to develop a mathematical model which has the ability to find complex patterns which human beings seem to follow when playing this very elementary game. This project is still a *work in progress* and many future algorithms are planned - with a special focus on machine learning algorithms. Bellow is a brief summary of what this project contains.

## The Actual Game

I have created a Pygame GUI which in a simple manner allows the player to play the game of rock paper scissors by chosing a move and getting a response promptly. The move which the computer plays is dependent on what algorithm the computer is currently using, something which is easily changed in the code. For every round which is played, the program saves both the winner of the round and what move that player used. It is from this data that the models infers decisions. For instance, one of the developed algorithms is called a first order historical. This algorithm looks at all previous games with similar outcomes (i.e. the same moves were played) and plays the move which would have won the subsequential game in that case. Finally, there is some code which can be used to make different algorithms face each other to decide which the **ultimate** algorithm is.

![Image](images/RPS_Screenshot1.png)  
![Image](images/RPS_Screenshot2.png)  
![Image](images/RPS_Screenshot3.png)  

## The *Regular* Algorithms

These algorithms are primarily based on **game theory** and I have for example implemented win-stay lose-switch. This algorithm works by simply basing the next move on the one before. If the bot has lost, it will play what would have won the last round, if he wins it will play the same move and in the case of a draw the algorithm simply performs a random move. This algorithm has been studied rather thoroughly and has in general been seen as one of the best strategies for rock paper scissors. Other algorithms include a frequency analysis, which looks at what would have worked most of the previous rounds, and a historical analysis which looks at the past game which looks exactly like this and plays the move which would have won then. I have also - in collaboration with some friends - implemented some more humorous algorithms.

## The Machine Learning Algorithms

Finally, I have also been working on implementing some machine learning algorithms. I have used data from this [https://osf.io/wmb2h/](experiment). This far, I have only implemented a simple feed forward neural network which processes the past 5 rounds and tries to find patterns in the way the players act. Currently, the best model has achieved a training accuracy of ~60%, but only an evaluation accuracy of ~38%, indicating that it is severely overfitting and is only *slightly* better than random guessing. However, the currently implemented model is **very** simple and merely serves as a proof of principle that the model can be implemented. Future plans include developing a LSTM and a random forest model which might actually find some more complex patterns in the data. This is due to these models' proficiency at complex sequential data.
