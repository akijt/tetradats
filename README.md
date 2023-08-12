# tetradats
block stacking game

## tetradats.py
- The main file of the game

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

## state_{}.py
- Holds specific PyGame functions for a specific state
- Code in the order of:
  1. INIT STATE
  1. ADJUST DIM
  1. INIT INTERACTABLES
  1. EVENT LOOP
  1. functions (if applicable)
  1. CLEAR SCREEN
  1. print stuff on screen (can be a variety of things)
  1. ERROR HANDLING
  1. ACCOUNT TAB (if applicable)
  1. CLOCK