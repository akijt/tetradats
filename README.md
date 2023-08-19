# tetradats
block stacking game

## tetradats.py
- The main file of the game
- Calls all state_{}.py

## tetris.py
- Holds the Tetris class controlling all functions of the actual gameplay

## records.py
- Holds classes for saving game records
- Currently supports local CSV and local MySQL
- Online database to come

## accounts.py
- Holds classes for saving player data
- Currently supports local My SQL
- Online database to come

## animation.py
- Holds class for cool animation on the login screen

## utils.py
- Holds sprite classes for drawing on the screen

## state_{}.py
- Holds specific PyGame functions for a specific state
- Code in the order of:
  1. INIT STATE
  1. UPDATE SPRITES
  1. EVENT LOOP
  1. functions including ERROR HANDLING (if applicable)
  1. CLEAR SCREEN
  1. print stuff on screen
  1. DRAW SPRITES
  1. CLOCK