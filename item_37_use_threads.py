# Item 37: Use threads for blocking I/O, avoid for parallelism
import time
from threading import Thread
import select


# The standard implementation of Python is call CPython. CPython runs a Python
# program in two steps. First, it parses and compiles the source text into
# bytecode. Then, it runs the bytecode using a stack-based interpreter. The
# bytecode interpreter has state that must be maintained and coherent while
# the Python program executes. Python enforces coherence with a mechanism
# called the global interpreter lock (GIL).

# Essentially, the GIL is a mutual-exclusion lock (mutex) that prevents
# CPython from being affected by preemptive multi-threading, where one thread
# takes control of a program by interrupting state if it comes at an
# unexpected time. The GIL prevents these interruptions and ensures that every
# bytecode instruction works correctly with the CPython implementation and its
# C-extension modules.

# The GIL has an important negative side effect. With programs written in
# languages like C++ or Java, having multiple threads of execution means your
# program could utilize multiple CPU cores at the same time. Although Python
# supports multiple threads of execution, the GIL causes only one of them to
# make forward progress at a time. This means that when you reach for threads
# to do parallel computation and speed up your Python programs, you will be
# sorely disappointed.

# For example, say you want to do something computationally intensive with
# Python. I'll use a naive number factorization algorithm as a proxy.


def factorize(number):
    for i in range(1, number + 1):
        if number % i == 0:
            yield i

# Factoring a set of numbers in serial takes quite a long time.

numbers = [2139079, 1214759, 1516637, 1852285]
start = time.time()
for number in numbers:
    list(factorize(number))
end = time.time()
print('Took %.3f seconds' % (end - start))
# Took 0.624 seconds


# Using multiple threads to do this computation would make sense in other
# languages because you could take advantage of all the CPU cores of your
# computer. Let me try that in Python. Here, I define a Python thread for
# doing the same computation as before:


class FactorizeThread(Thread):
    def __init__(self, number):
        super().__init__()
        self.number = number
        self.factors = list([])

    def run(self):
        self.factors = list(factorize(self.number))


# Then, I start a thread for factorizing each number in parallel.


start = time.time()
threads = []
for number in numbers:
    thread = FactorizeThread(number)
    thread.start()
    threads.append(thread)

# Finally, I wait for all of the threads to finish.

for thread in threads:
    thread.join()
end = time.time()
print('Tool %.3f seconds' % (end - start))
# Tool 0.662 seconds

# What's surprising is that this takes even longer than running factorize in
# serial. With on thread per number, you may expect less than a n times
# speedup on the dual-core machine I used to run this code. But you would
# never expect the performance of these threads to be worse when you have
# multiple CPUs to utilize. This demonstrates the effect of the GIL on
# programs running in the standard CPython interpreter.

# There are ways to get CPython to utilize multiple cores, but it doesn't
# work with the standard Thread class (see Item 41:
# "Consider  concurrent.futures for true parallelism") and it can require
# substantial effort. Knowing these limitations you may wonder, why does
# Python support threads at all? There are two good reasons.

# First, multiple threads make it easy for your program to seem like it's
# doing multiple things at the same time. Managing the juggling act of
# simultaneous tasks is difficult to implement yourself (see Item 40:
# "Consider co-routines to run many functions concurrently" for an example).
# With threads, you can leave it to Python to run your functions seemingly in
# parallel. This works because CPython ensures a level of fairness between
# Python threads of execution, even though only one of them makes forward
# progress at a time due to the GIL.

# The second reason Python supports threads is to deal with blocking I/O,
# which happens when Python does certain types of system calls. System calls
# are how your Python program asks your computer's operating system to
# interact with the external environment on your behalf. Blocking I/O includes
# things like reading and writing files, interacting with networks,
# communicating with devices like displays, etc. Threads help you handle
# blocking I/O by insulating your program from the time it takes for the
# operating system to respond to your requests.

# For example, say you want to send a singal to a remote-controlled helicopter
# through a serial port. I'll use a slow system call (select) as a proxy for
# this activity. This function asks the operating system to block for 0.1
# second and then return control to my program, similar to what would happen
# when using a synchronous serial port.


def slow_systemcall():
    select.select([], [], [], 0.1)


# Running this system call in serial requires a linearly increasing amount of
# time.

start = time.time()
for _ in range(5):
    slow_systemcall()
end = time.time()
print('Took %.3f seconds' % (end - start))
# Took 0.501 seconds

# The problem is that while the slow_systemcall function is running, my
# program can't make any other progress. My program's main thread of execution
# is blocked on the select system call. This situation is awful in practice.
# You need to be able to compute your helicopter's next move while you're
# sending it a signal, otherwise it's crash. When you find yourself needing to
# do blocking I/O and computation simultaneously, it's time to consider moving
# your system calls to threads.

# Here, I run multiple invocation of the slow_systemcall function in separate
# threads. This would allow you to communicate with multiple serial ports (and
# helicopters) at the same time, while leaving the main thread to do whatever
# computation is required.


start = time.time()
threads = []
for _ in range(5):
    thread = Thread(target=slow_systemcall)
    thread.start()
    threads.append(thread)


# With the threads started, here I do some work to calculate the next
# helicopter move before waiting for the system call threads to finish.


def compute_helicopter_location(index):
    return index**2

for i in range(5):
    compute_helicopter_location(i)

for thread in threads:
    thread.join()
end = time.time()
print('Took %.3f seconds' % (end - start))
# Took 0.101 seconds

# The parallel time is 5 times less than the serial time. This shows that the
# system call will all run in parallel from multiple Python threads even
# though they're limited by the GIL. The GIL prevents my Python code from
# running in parallel, but it has no negative effect on system calls. This
# works because Python threads release the GIL just before they make system
# calls and reacquire the GIL as soon as the system calls are done.

# There are many other ways to deal with blocking I/O besides threads, such as
# the asyncio built-in module, and these alternatives have important benefits.
# But these options also require extra work in refactoring your code to fit a
# different model of execution (see Item 40: "Consider coroutines to run many
# functions concurrently"). Using threads is the simplest way to do blocking
# I/O in parallel with minimal changes to your program.


# Things to remember

# 1. Python threads can't bytecode in parallel on multiple CPU cores because
#     of the global interpreter lock (GIL).
# 2. Python threads are still useful despite the GIL because they provide an
#     easy way to do multiple things at seemingly the same time.
# 3. Use Python threads to make multiple system calls in parallel. This allows
#     you to do blocking I/O at the same time as computation.
