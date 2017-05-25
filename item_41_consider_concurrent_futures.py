# Item 41: Consider concurrent.futures for true parallelism
import time
from concurrent.futures import ThreadPoolExecutor


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


# Things to remember

# 1.
# 2.
# 3.
# 4.
