# Hello

This is my command-line sudoku game. This is not an attempt to create a game
that will inspire awe, nor is it even really supposed to be played, _per se_.
Its primary purpose is to be a fun programming exercise.

**Contents:**

- [1. Self-imposed requirements](#1-self-imposed-requirements)
- [2. How to run](#2-how-to-run)
  - [2.1. Requirements](#21-requirements)
  - [2.2. Installation](#22-installation)
  - [2.3. Running](#23-running)
- [3. New things learned](#3-new-things-learned)
  - [3.1. Python set creation](#31-python-set-creation)
  - [3.2. Python version management with `pyenv`](#32-python-version-management-with-pyenv)
    - [3.2.1. Note](#321-note)
- [4. Evaluation](#4-evaluation)
- [5. Important Notes](#5-important-notes)

## 1. Self-imposed requirements

The game should have:

1. Sudoku puzzle generation, including:
   - Difficulty
   - Unorthodox grid sizes (NxN)
   - Unorthodox box sizes (NxM) e.g. 4x5 boxes resulting in a 20x20 grid
2. Sudoku puzzle solving, including:
   - Giving player parts of solution if they request a hint
   - Allowing player to enter their own grid, and giving the solution
3. Non-terrible interface.

The code should:

1. Be functional as far as is reasonable. I want to challenge myobject-oriented
   ways of thinking, but not at the cost of readability/maintainability. State
   is for losers, but so is dogma.
2. Use an adapted form of the "wave function collapse
   [algorithm](https://github.com/mxgmn/WaveFunctionCollapse)" for both puzzle
   generation and solving. This is the real reason I'm making this game.

## 2. How to run

### 2.1. Requirements

- [Poetry](https://python-poetry.org)

All that should be needed to run this is poetry, although I'd recommend having
pyenv with Python 3.10 installed if you're messing about with the code.  I'm
using type hints extensively, and some of the more recent syntax may require
a later version of Python.

### 2.2. Installation

```shell
> make requirements-base
# Or, if you're messing about with the code
> make requirements-dev
```

### 2.3. Running

```shell
> make run
```

If you don't know how to do that... What are you doing on github? I'll add
something for you later.

## 3. New things learned

These projects are essentially coding practice, so it's good to keep track of
new stuff. So here's that:

### 3.1. Python set creation

I hadn't often used sets in Python until this project, so I wasn't familiar
with the curly-brace notation. In short, you can create a set like you would an
array:

```python
# Set literal
set1: set[int] = {0, 1, 2, 3}
# Set comprehension
set2: set[int] = {int(num) for num in "1331302001302002"}
# Set literal with iterable unpacking
set3: set[int] = {*range(4)}
# For below, note that set4 = {} would create an empty dictionary, not set.
# Empty set populated in for loop
set4: set[int] = set()
for i in range(4):
   set4.add(i)
assert set1 == set2 and set2 == set3 and set3 == set4
```

### 3.2. Python version management with `pyenv`

When I was hurriedly setting up my mac for Python development, I believe I
installed Python 3.10 with homebrew. This worked fine right up until I decided
I wanted to use [Poetry](https://python-poetry.org), and the installation
script failed due to missing certificates in my Python installation.  Whilst
researching the fix for this, I came across
[`pyenv`](https://github.com/pyenv/pyenv). It's a Python version manager,
similar to [`nvm`](https://github.com/nvm-sh/nvm) for node. Simply put, it
helps install multiple Python versions on your system, and allows you to set
which version to use globally, for a specific directory, or just for the
current session. For example, presuming you normally use Python 3.8 but want to
set up this repo:

```shell
> pyenv install 3.8.13
> pyenv global 3.8.13
> python --version
Python 3.8.13

> pyenv install 3.10.4
> cd wave_function_collapse_sudoku
> pyenv local 3.10.4
> python --version
Python 3.10.4
> cd ..
> python --version
Python 3.10.4
```

#### 3.2.1. Note

I uninstalled all of my previously-installed Python versions before installing
`pyenv`, which may not be required, but I'd imagine it's best so that all
Python packages are managed by it.

## 4. Evaluation

TODO: evaluate once requirements met.

Things to mention

- Skipping box checking during fill_free_boxes drastically improved create_grid
  performance
- Collapsing cell with least options improved success rates
- If I just took more time to learn things before trying to jump in, I'd create
  less tech debt.

## 5. Important Notes

- In the code, all coordinates are in the form (y, x). This is because the grid
  is a matrix (or 2D array, if you prefer), and I find
  [row-major ordering](https://en.wikipedia.org/wiki/Row-_and_column-major_order)
  more intuitive.
