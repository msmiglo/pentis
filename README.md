# pentris
A variation of tetris game in which blocks consist of 5 squares instead of 4, just to try if its playable.

Steering:
Arrows - moving piece (up arrow - rotate piece)
R - restart
Space - pause (still able to play, but stops pieces from auto-falling-down)
Esc - quit

The game with classic rules and even slow speed is almost unplayable for the beginners. There should be some aiding featurs like showing the queue of next pieces, highlighting placement clues that keep playfield clean and open, possibility to mirror the piece, enhanced rotation, and so on. The correction introduced burning lines even if there is 1 square missing.

Looking on the Internet - there are several games implementing the Pentris idea. Nevertheless the more apropriate name for the game should be Pentis, as the Greek prefix for 5 is "penta", not "pentra". But nevermind :)

I hope you will enjoy checking out how it is to play some unplayable game :)

Technical problems occur with the multithreading usage of tkinter canvas animation, that will not be fixed.