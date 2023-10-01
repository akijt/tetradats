# tetradats
block stacking game in Python 3.7.9 and PyGame 2.4.0

## tetradats.py
- The main file of the game
- Calls all state_{}.py

## tetris.py
- Holds the Tetris class controlling all functions of the actual gameplay

## records.py
- Holds classes for saving game records
- Supports local CSV, local MySQL, and MS Azure MySQL

## accounts.py
- Holds classes for saving player data
- Supports local CSV, local MySQL, and MS Azure MySQL

## animation.py
- Holds class for cool animation on the login screen

## utils.py
- Holds sprite classes for drawing on the screen

## state_{}.py
- Holds specific PyGame functions for a specific state
- Code in the order of:
  1. INIT STATE
  1. EVENT LOOP
  1. functions (if applicable)
  1. CLEAR SCREEN
  1. print stuff on screen
  1. DRAW SPRITES
  1. CLOCK
  1. INPUT FUNCTIONS AND ERROR HANDLING (if applicable)