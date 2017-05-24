# Item 40: Consider coroutines to run many functions concurrently
from collections import namedtuple


# Threads give Python programmers a way to run multiple functions seemingly at
# the same time (see "Use Threads for blocking I/O, avoid for parallelism" ).
# But there are three big problems with threads:

# 1. They require special tools to coordinate with each other safely (see
# Item 38: "Use lock to prevent data races in threads" and Item 39: "Use queue
# to coordinate work between threads"). This makes code that uses threads
# harder to reason about than procedural, single-threaded code. This
# complexity makes threaded code more difficult to extend and maintain over
# time.

# 2. Threads require a lot of memory, about 8 MB per executing thread. On many
# computers, that amount of memory doesn't matter for a dozen threads or so.
# But what if you want your program to run ten thousands of functions
# "simultaneously"? These functions may correspond to user requests to a
# server, pixels on a screen, particles in a simulation, etc. Running a thread
# per unique activity just won't work.

# 3. Threads are costly to start. If you want to constantly be creating new
# concurrent functions and finishing them, the overhead of using threads
# becomes large and slows everything down.

# Python can work around all these issues with coroutines. Coroutines let you
# have many seemingly simultaneous functions in your Python programs. They're
# implemented as an extension to generators (see Item 16: "Consider generator
# instead of returning lists"). The cost of starting a generator coroutine is
# a function call. Once active, they each use less than 1 KB of memory until
# they're exhausted.

# Coruntines work by enabling the code consuming a generator to send a value
# back into the generator function after each yield expression. The generator
# function receives the value passed to the send function as the result of the
# corresponding yield expression.


def my_corountine():
    while True:
        received = yield
        print('Received:', received)

it = my_corountine()
next(it)
it.send('First')
it.send('Second')
# Received: First
# Received: Second

# The initial call to next is required to prepare the generator for receiving
# the first send by advancing it to the first yield expression. Together,
# yield and send provide generators with a standard way to vary their next
# yielded value in response to external input.

# For example, say you want to implement a generator coroutine that yields the
# minmum value it's been sent so far. Here, the bare yield prepares the
# coroutine with the initial minimum value sent in from the outsize. Then the
# generator repeatedly yields the new minimum in exchange for the next value
# to consider.


def minimize():
    current = yield
    while True:
        value = yield current
        current = min(value, current)


# The code consuming the generator can run one step at a time and will output
# the minimum value seen after each input.

it = minimize()
next(it)             # Prime the generator
print(it.send(10))
print(it.send(4))
print(it.send(22))
print(it.send(-1))
# 10
# 4
# 4
# -1

# The generator function will seemingly run forever, making forward progress
# with each new call to send. Like threads, coroutines are independent
# functions that can consume inputs from their environment and produce
# resulting outputs. The difference is that coroutines pause at each yield
# expression in the generator function and resume after each call to send from
# the outside. This is the magical mechanism of coroutines.

# This behavior allows the code consuming the generator to take action after
# each yield expression in the coroutine. The consuming code can use the
# generator's output values to call other functions and update data
# structures. Most importantly, it can advance other generator functions until
# their next yield expressions. By advancing many separate generators in
# lockstep, they will all seem to be running simultaneously, mimicking the
# concurrent behavior of Python threads.


# The Game of Life

# Let me demonstrate the simultaneous behavior of coroutines with can example.
# Say you want to use corountines to implement Conway's Game of Life. The
# rules of the game are simple. You have a two-dimensional grid of an
# arbitrary size. Each cell in the grid can either be alive or empty.

ALIVE = '*'
EMPTY = '-'

# The game progress on trick of the clock at a time. At each tick, each cell
# counts how many of its neighboring eight cells are still alive. Based on its
# neighbor count, each cell decides if it will keep living, die, or
# regenerate. Here's an example of a $5\times5$ Game of Life grid after four
# generations with time going on the right. I'll explain the specific rules
# further below.
#   0  |  1  |  3  |  4  |  5
# -----|-----|-----|-----|-----
# -*---|--*--|--**-|--*--|-----
# --**-|--**-|-*---|-*---|-**--
# ---*-|--**-|--**-|--*--|-----
# -----|-----|-----|-----|-----

# I can model this game by representing each cell as a generator coroutine
# running in lockstep with all the others.

# To implement this, first I need a way to retrieve the status of neighboring
# cells. I can do this with a coroutine named count_neighbors that works by
# yielding Query objects. The Query class I define myself. Its purpose is to
# provide the generator coroutine with a way to ask its surrounding
# environment for information.


Query = namedtuple('Query', ('y', 'x'))


# The coroutine yields a Query for each neighbor. The result of each yield
# expression will be the value ALIVE or EMPTY. That's the interface contract
# I've defined between the coroutine and its consuming code. The count_
# neighbors generator sees the neighbors's states and returns the count of
# living neighbors.


def count_neighbors(y, x):
    n_ = yield Query(y + 1, x + 0)  # North
    ne = yield Query(y + 1, x + 1)  # Northeast
    e_ = yield Query(y + 0, x + 1)  # East
    se = yield Query(y - 1, x + 1)  # Southeast
    s_ = yield Query(y - 1, x + 0)  # South
    sw = yield Query(y - 1, x - 1)  # Southwest
    w_ = yield Query(y + 0, x - 1)  # West
    nw = yield Query(y + 1, x - 1)  # Northwest

    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    return count


# I can drive the count_neighbors coroutine with fake data to test it. Here, I
# show how Query objects will be yielded for each neighbor. count_neighbors
# expects to receive cell states corresponding to each Query through the
# coroutine's send method. The final count is returned in the StopIteration
# exception that is raised when the generator is exhausted by the return
# statement.

it = count_neighbors(10, 5)
q1 = next(it)                  # Get the first query
print('First yield:  ', q1)
q2 = it.send(ALIVE)            # Send q1 state, get q2
print('Second yield: ', q2)
q3 = it.send(EMPTY)            # Send q2 stete, get q3
print('Third yield:  ', q3)
q4 = it.send(ALIVE)            # Send q3 state, get q4
print('Fourth yield: ', q4)
q5 = it.send(EMPTY)            # Send q4 stete, get q5
print('Fifth yield:  ', q5)
q6 = it.send(EMPTY)            # Send q5 stete, get q6
print('Sixth yield:  ', q6)
q7 = it.send(EMPTY)            # Send q6 state, get q7
print('Seventh yield:', q7)
q8 = it.send(EMPTY)            # Send q7 stete, get q8
print('Eighth yield: ', q8)

try:
    count = it.send(EMPTY)
except StopIteration as e:
    print('Count: ', e.value)
# First yield:   Query(y=11, x=5)
# Second yield:  Query(y=11, x=6)
# Third yield:   Query(y=10, x=6)
# Fourth yield:  Query(y=9, x=6)
# Fifth yield:   Query(y=9, x=5)
# Sixth yield:   Query(y=9, x=4)
# Seventh yield: Query(y=10, x=4)
# Eighth yield:  Query(y=11, x=4)
# Count:  2


# Now I need the ability to indicate that a cell will transition to a new
# state in response to the neighbor count that it found from count_neighbors.
# To do this, I define another coroutine called step_cell. This generator will
# indicate transitions in a cell's state by yielding Transition objects. This
# is another class that I define, just like the Query class.


Transition = namedtuple('Transition', ('y', 'x', 'state'))


# The step_cell coroutine receives its coordinates in the grid as arguments.
# It yields a Query to get the initial state of those coordinates. It runs
# count_neighbors to inspect the cells around it. It runs the game logic to
# determine what state the cell should have for the next clock tick. Finally,
# it yields a Transition object to cell the environment the cell's next state.


# def game_logic(state, neighbors):
#     return state

def game_logic(state, neighbors):
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY          # Die: Too few
        elif neighbors > 3:
            return EMPTY          # Die: Too many
    else:
        if neighbors == 3:
            return ALIVE          # Regenerate
    return state


def step_cell(y, x):
    state = yield Query(y, x)
    neighbors = yield from count_neighbors(y, x)
    next_state = game_logic(state, neighbors)
    yield Transition(y, x, next_state)


# Importantly, the call to count_neighbors uses the yield from expression.
# This expression allows Python to compose generator coroutines together,
# making it easy to reuse smaller pieces of functionality and build complex
# coroutines from simpler ones. When count_neighbors is exhausted, the final
# value it returns (with the return statement) will be passed to step_cell as
# the result of the yield from expression.


# def game_logic(state, neighbors):
#     if state == ALIVE:
#         if neighbors < 2:
#             return EMPTY          # Die: Too few
#         elif neighbors > 3:
#             return EMPTY          # Die: Too many
#     else:
#         if neighbors == 3:
#             return ALIVE          # Regenerate
#     return state


# I can drive the step_cell coroutine with fake data to test it.


it = step_cell(10, 5)
q0 = next(it)
print('Me         ', q0)
q1 = it.send(ALIVE)
print('Q1:        ', q1)
# ...
# t0 = it.send(EMPTY)
# print('T0:        ', t0)
t1 = it.send(EMPTY)
print('Outcome:   ', t1)
# Me          Query(y=10, x=5)
# Q1:         Query(y=11, x=5)
# Outcome:    Query(y=11, x=6)


# The goal of the game is to run this logic for a whole grid of cells in
# lockstep. To do this, I can further compose the step_cell coroutine into a
# simulate coroutine. This coroutine progresses the grid of cells forward by
# yielding from step_cell many times. After progressing every coordinate, it
# yields a TICK object to indicate that the current generation of cells have
# all transitioned.


TICK = object()


def simulate(height, width):
    while True:
        for y in range(height):
            for x in range(width):
                yield from step_cell(y, x)
        yield TICK


# What's impressive about simulate is that it's completely disconnected from
# the surrounding environment. I still haven't defined how the grid is
# represented in Python objects, how Query, Transition, and TICK values are
# handled on the outside, nor how the game gets its initial state. But the
# logic is clear. Each cell will transition by running step_cell. Then the
# game clock will tick. This will continue forever, as long as the simulate
# coroutine is advanced.


# This is the beauty of coroutines. They help you focus on the logic of what
# you're trying to accomplish. They decouple your code's instructions for the
# environment from the implementation that carries out your wishes. This also
# allows you to improve the implementation of following those instructions
# over time without changing the coroutines.

# Now, I want to run simulate in a real environment. To do that, I need to
# represent the state of each cell in the grid. Here, I define a class to
# contain the grid:


class Grid(object):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = []
        for _ in range(self.height):
            self.rows.append([EMPTY] * self.width)

    def __str__(self):
        str = ''
        for i in range(self.height):
            for j in range(self.width):
                str += self.query(i, j)
                # print(self.query(i, j))
            str += '\n'
            # print('\n')
        return str

# The grid allows you to get and set the value of any coordinate. Coordinates
# that are out of bounds will wrap around, making the grid act like infinite
# looping space.

    def query(self, y, x):
        return self.rows[y % self.height][x % self.width]

    def assign(self, y, x, state):
        self.rows[y % self.height][x % self.width] = state

# At last, I can define the function that interprets the values yielded from
# simulate and all of its interior coroutines. This function turns the
# instructions from the coroutines into interactions with the surrounding
# environment. It progress the whole grid of cells forward a single step and
# then returns a new grid containing the next state.


def live_a_generation(grid, sim):
    progeny = Grid(grid.height, grid.width)
    item = next(sim)
    while item is (not TICK):
        if isinstance(item, Query):
            state = grid.query(item.y, item.x)
            item = sim.send(state)
        else:
            progeny.assign(item.y, item.x, item.state)
            item.next(sim)
    return progeny


# To see this function in action, I need to create a grid and set its initial
# state. Here, I make a classic shape called a glider.


grid = Grid(5, 9)
grid.assign(0, 3, ALIVE)
grid.assign(1, 4, ALIVE)
grid.assign(2, 2, ALIVE)
grid.assign(2, 3, ALIVE)
grid.assign(2, 4, ALIVE)
print(grid)
# ---*-----
# ----*----
# --***----
# ---------
# ---------


# Now I can progress this grid forward one generation at a time. You can see
# how the glider moves down and to the right on the grid based on the simple
# rules from the game_logic function.

class ColumnPrinter(object):
    def __init__(self):
        self.height = 0
        self.width = 0
        self.string = []
        self.times = 0

    def append(self, str_grid):
        if self.string == []:
            self.string = str_grid.split('\n')
            self.height = len(self.string) - 1
            self.width = len(self.string[0])
        else:
            str_grid_ = str_grid.split('\n')
            height_ = len(str_grid_) - 1
            width_ = len(str_grid_[0])
            assert height_ == self.height
            assert width_ == self.width
            for i in range(self.height):
                self.string[i] += '|'
                self.string[i] += str_grid_[i]

        self.times += 1

    def __str__(self):
        # head
        head = ""
        for i in range(self.width * self.times + (self.times - 1)):
            number = int(i + (self.width+1)/2 + 1)
            if (i+1) % (self.width + 1) == 0 and i > 0:
                head += '|'
            elif number % (self.width + 1) == 0:
                head += str(int(number/self.width))
            else:
                head += ' '
        # body
        printer = head + '\n'
        for i in range(self.height):
            printer += (self.string[i] + '\n')
        return printer


colums = ColumnPrinter()
sim = simulate(grid.height, grid.width)
for i in range(5):
    colums.append(str(grid))
    grid = live_a_generation(grid, sim)

print(colums)
#     1    |    2    |    3    |    4    |    5
# ---*-----|---------|---------|---------|---------
# ----*----|---------|---------|---------|---------
# --***----|---------|---------|---------|---------
# ---------|---------|---------|---------|---------
# ---------|---------|---------|---------|---------


# The best part about this approach is that I can change the game_logic
# function without having to update the code that surrounds it. I can change
# the rules or add larger spheres of influence with the existing machanics of
# Query, Transition, and TICK. This demonstrates how coroutines enable the
# separation of concerns, which is an important design principle.


# Coroutines in Python 2

# Unfortunately, Python 2 is missing some of the syntactical sugar that makes
# coroutines so elegant in Python 3. There are two limitations. Fist, there is
# no yield from expression. That means that when you want to compose generator
# coroutines in Python 2, you need to include an additional loop at the
# delegation point.


# Python 2
def delegated():
    yield 1
    yield 2


def composed():
    yield 'A'
    for value in delegated():  # yield from in Python 3
        yield value
    yield 'B'

print(list(composed()))
# ['A', 1, 2, 'B']


# The second limitation is that there is no support for the return statement
# in Python 2 generators. To get the same behavior that interacts correctly
# with try/except/finally blocks, you need to define your own exception type
# and raise it when you want to return a value.


# Python 2
class MyReturn(Exception):
    def __init__(self, value):
        self.value = value


def delegated():
    yield 1
    raise MyReturn(2)  # return 2 in Python 3


def composed():
    try:
        for value in delegated():
            yield value
    except MyReturn as e:
        output = e.value
    yield output * 4

print(list(composed()))
# [1, 8]


# Things to remember

# 1. Coroutines provide an efficient way to run tens of thousands of functions
#    seemingly at the same time.
# 2. Within a generator, the value of the yield expression will be whatever
#    value was passed to the generator's send method from the exterior code.
# 3. Coroutines give you a powerful tool for separating the core logic of your
#    program from its interaction with the surrounding environment.
# 4. Python 2 doesn't support yield from or returning values from generators.
