# Item 40: Consider coroutines to run many functions concurrently


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
#   ALIVE = '*'
#   EMPTY = '-'

# The game progress on trick of the clock at a time. At each tick, each cell
# counts how many of its neighboring eight cells are still alive. Based on its
# neighbor count, each cell decides if it will keep living, die, or
# regenerate. Here's an example of a $5\times5$ Game of Life grid after four
# generations with time going on the right. I'll explain the specific rules
# further below.
#   0     1     3     4     5
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


Query = nametuple('Query', ('y', 'x'))

# The coroutine yields a Query for each neighbor. The result of each yield
# expression will be the value ALIVE or EMPTY. That's the interface contract
# I've defined between the coroutine and its consuming code. The count_
# neighbors generator sees the neighbors's states and returns the count of
# living neighbors.


def count_neighbors(y, x):
    n_ = yield Query(y + 1, x + 0)  # North
    ne = yield Query(y + 1, x + 1)  # Northeast
    e_ = yield Query(y + 1, x + 0)  # East
    se = yield Query(y + 1, x + 1)  # Southeast
    s_ = yield Query(y + 1, x + 0)  # South
    sw = yield Query(y + 1, x + 1)  # Southwest
    w_ = yield Query(y + 1, x + 0)  # West
    nw = yield Query(y + 1, x + 1)  # Northwest

# Things to remember

# 1.
# 2.
# 3.
