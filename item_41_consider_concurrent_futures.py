# Item 41: Consider concurrent.futures for true parallelism
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor


# At some point in writing Python programs, you may hit the performance wall.
# Even after optimizing your code (see Item 58: "Profile before optimizing"),
# your program's execution may still be too slow for your needs. On modern
# computers that have an increasing number of CPU cores, it's reasonable to
# assume that one solution would be parallelism. What if you could split your
# code's computation into independent pieces of work that run simultaneously
# across multiple CPU cores?


# Unfortunately, Python's global interpreter lock (GIL) prevents true
# parallelism in threads (see Item 37: "Use threads for blocking I/O, avoid
# for parallelism"), so that option is out. Another common suggestion is to
# rewrite your most performance-critical code as an extension module using C
# language. C gets you closer to the bare metal and can run faster than
# Python, eliminating the need for parallelism. C-extensions can also start
# native threads that run in parallel and utilize multiple CPU cores. Python's
# API for C-extensions is well documented and a good choice for an escape
# hatch.

# But rewriting your code in C has a high cost. Code that is short and
# understandable in Python can become verbose and complicated in C. Such a
# port requires extensive testing to ensure that the functionality is
# equivalent to the original Python code and that no bugs have been
# introduced. Sometimes it's worth it, which explains the large ecosystem of
# C-extension modules in the Python community that speed up things like text
# parsing, image compositing, and matrix math. There are even open source
# tools such as Cython (http://cython.org/) and Numba (http://numba.pydata.org/)
# that can ease the transition to C.

# The problem is that moving one piece of your program to C isn't sufficient
# most of the time. Optimized Python programs usually don't have one major
# source of slowness, but rather, there are often many significant
# contributors. To get the benefits of C's bare metal and threads, you'd need
# to port large parts of your program, drastically increasing testing needs
# and risk. There must be a better way to preserve your investment in Python
# to solve difficult computational problems.

# The multiprocessing built-in module, easily accessed via the
# concurrent.futures built-in module, may be exactly what you need. It enables
# Python to utilize multiple CPU cores in parallel by running additional
# interpreters as child processes. These child processes are separate from the
# main interpreter, so their global interpreter locks are also separate. Each
# child can fully utilize one CPU core. Each child has a link to the main
# process where it receives instructions to do computation and returns results.

# For example, say you want to do something computationally intensive with
# Python and utilize multiple CPU cores. I'll use an implementation of finding
# the greatest common divisor of two numbers as proxy for a more
# computationally intense algorithm, like simulating fluid dynamics with the
# Navier_Stokes equation.


def gcd(pair):
    a, b = pair
    low = min(a, b)
    for i in range(low, 0, -1):
        if a % i == 0 and b % i == 0:
            return i


# Running this function in serial takes a linearly increasing amount of time
# because there is no parallelism.

numbers = [(1963309, 2265973), (2030677, 3814172),
           (1551645, 2229620), (2039045, 2020802)]
start = time.time()
results = list(map(gcd, numbers))
end = time.time()
print('Took %.3f seconds' % (end - start))
# Took 0.667 seconds

# Running this code on multiple Python threads will yield no speed improvement
# because the GIL prevents Python from using multiple CPU cores in parallel.
# Here, I do the same computation as above using the concurrent.futures
# modules with its ThreadPoolExecutor class and two worker threads (to match
# the number of CPU cores on my computer):

start = time.time()
pool = ThreadPoolExecutor(max_workers=2)
results = list(map(gcd, numbers))
end = time.time()
print('Took %.3f seconds' % (end - start))
# Took 0.680 seconds


# Running this code on multiple Python threads will yield no speed improvement
# because the GIL prevents Python from using multiple CPU cores in parallel.
# Here, I do the same computation as above using the concurrent.futures module
# with its ThreadPoolExecutor class and two worker threads (to match the
# number of CPU cores on my computer):

start = time.time()
pool = ThreadPoolExecutor(max_workers=2)
results = list(pool.map(gcd, numbers))
end = time.time()
print('Took %.3f seconds' % (end - start))
# Took 0.664 seconds


# It's even slower this time because of the overhead of starting and
# communicating with the pool of threads.

# Now for the surprising part: By changing a single line of code, something
# magical happens. If I replace the ThreadPoolExecutor with the
# ProcessPoolExecutor from the concurrent.futures module, everything speeds
# up.

start = time.time()
pool = ProcessPoolExecutor(max_workers=2)  # the one change
results = list(pool.map(gcd, numbers))
end = time.time()
print('Took %.3f seconds' % (end - start))
# Took 0.357 seconds

# Running on my dual-core machine, it's significantly faster! How is this
# possible? Here's what the ProcessPoolExecutor class actually does (via the
# low-level constructs provided by the multiprocessing module):
#    1. It takes each item from the numbers input data to map.
#    2. It serializes it into binary data using the pickle module (see Item 44:
#       "Make pickle reliable with copyreg").
#    3. It copies the serialized data from the main interpreter process to a
#       child interpreter process over a local socket.
#    4. Next, it de-serializes the data back into Python objects using pickle
#       in the child process.
#    5. It then imports the Python module containing the gcd function.
#    6. It runs the function on the input data in parallel with other child
#       processes.
#    7. It serializes the result back into bytes.
#    8. It copies those bytes back through the socket.
#    9. It de-serializes the bytes back into Python objects in the parent
#       process.
#   10. Finally, it merges the results from multiple children into a single
#       list to return.

# Although it looks simple to the programmer, the multiprocessing module and
# ProcessPoolExecutor class do a huge amount of work to make parallelism
# possible. In most other language, the only touch point you need to
# coordinate two threads is a single lock or atomic operation. The overhead of
# using multiprocessing is high because of all of the serialization and
# deserialization that must happen between the parent and child processes.

# This scheme is well suited to certain types of isolated, high-leverage
# tasks. By isolated, I mean function that don't need to share state with
# other parts of the program. By high-leverage, I mean situations in which
# only a small amount of data must be transferred between the parent and
# child processes to enable a large amount of computation. The greatest
# common denominator algorithm is one example of this, but many other
# mathematical algorithms work similarly.

# If your computation doesn't have these characteristics, then the overhead of
# multiprocessing may prevent it from speeding up your program through
# parallelization. When that happens, multiprocessing provides more advanced
# facilities for shared memory, cross-process locks, queues, and proxies. But
# all of these features are very complex. It's hard enough to reason about
# such tools in the memory space of a single process shared between Python
# threads. Extending that complexity to other processes and involving sockets
# makes this much more difficult to understand.

# I suggest avoiding all part of multiprocessing and using these features via
# the simpler concurrent.futures modules module. You can start by using the
# ThreadPoolExecutor class to run isolated, high-leverage functions in
# threads. Later, you can move to the ProcessPoolExecutor to get a speedup.
# Finally, once you've completely exhausted the other options, you can
# consider using the multiprocessing module directly.


# Things to remember

# 1. Moving CPU bottlenecks to C-extension modules can be an effective way to
#    improve performance while maximizing your investment in Python code.
#    However, the cost of doing so is high and may introduce bugs.
# 2. The multiprocessing module provides powerful tools that can parallelize
#    certain types of Python computation with minimal effort.
# 3. The power of multiprocessing is best accessed through the
#    concurrent.futures built-in module and its simple ProcessPoolExecutor
#    class.
# 4. The advanced parts of the multiprocessing module should be avoided
#    because they are so complex.
