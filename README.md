# Hello

This is my command-line sudoku game. This is not an attempt to
create a game that will inspire awe, nor is it even really
supposed to be played, _per se_. Its primary purpose is to
be a fun programming exercise.

## Self-imposed requirements

The game should have:

1. Sudoku puzzle generation, including:
   - Difficulty
   - Unorthodox grid sizes (NxN)
   - Unorthodox box sizes (NxM) e.g. 4x5 boxes resulting in a
     20x20 grid
2. Sudoku puzzle solving, including:
   - Giving player parts of solution if they request a hint
   - Allowing player to enter their own grid, and giving the
     solution
3. Non-terrible interface.

The code should:

1. Be functional as far as is reasonable. I want to challenge my
   object-oriented ways of thinking, but not at the cost of
   readability/maintainability. State is for losers, but so is
   dogma.
2. Use an adapted form of the "wave function collapse
   [algorithm](https://github.com/mxgmn/WaveFunctionCollapse)" for
   both puzzle generation and solving. This is the real reason I'm
   making this game.

## How to run

If you'd like to play the game, just clone the repository and run
`main.py`. If you don't know how to do that... What are you doing
on github? I'll add something for you later.

## Notes

- In the code, all coordinates are in the form (y, x). This is
  because the grid is a matrix (or 2D array, if you prefer), and
  I find [row-major ordering](https://en.wikipedia.org/wiki/Row-_and_column-major_order)
  more intuitive.

## Evaluation

TODO: evaluate once requirements met.
