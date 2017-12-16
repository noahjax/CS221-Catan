# CS221-Catan

Project for CS221 

AI for settlers of Catan.

This project should be used through two main modes.
1. Training / evaluating AI performance against each other. The commenting in train.py and eval.py should help here, but essentially you should run python train.py [AI type] [numIters]. This will output five files to the src folder, one of which will be labeled bestWeights.txt, representing the weights of the most successful AI player in the training. To evaluate the effectiveness of this AI, run python eval.py [Base AI Type] [Test AI type] bestWeights.txt [-w baseline weights]. The last argument is optional, and should only be used in the event that you are supplying some weights ahead of time, possibly to provide a better baseline etc. Alternately, you can call python train.py -p, which will run one AI of each type against each other. The program will look for certain kinds of weights files, which are detailed in the documentation.
2. Playing games using trained AI weights. Can be executed by running humanGame.py. Requires that qAIWinBest.txt is located in the src folder, and should contain weights learned by training. In this mode, you should set DISPLAY_ON to be true in display.py, and uncomment the calls to time.sleep(). 


Current bugs:
Robber movement for human player is incorrect. Too many nodes are being checked as neighbors, so it sees that one or more of the 'neighbors' is occupied with less than 3 points, and declares that tile invalid even when it should be valid.

Link to insert math equations in README
https://www.codecogs.com/latex/eqneditor.php
