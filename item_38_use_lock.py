# Item 38: Use lock to prevent data races in threads
from threading import Thread
from threading import Lock


# After learning about the global interpreter lock (GIL) (see Item 37: "Use
# threads for blocking I/O, Avoid for parallelism"), many new Python
# programmers assume they can forgo using mutual-exclusion locks () in their
# code altogether. If the GIL is already preventing Python threads form
# running on multiple CPU cores in parallel, it must also act as a lock for a
# program's data structure, right? Some testing on types like lists and
# dictionaries may even show that this assumption appears to hold.

# But beware, this is truly not the case. The GIL will not protect you.
# Although only one Python thread runs at a time, a thread's operations on
# data structures can be interrupted between any two bytecode instructions in
# the Python interpreter. This is dangerous if you access the same objects
# from multiple threads simultaneously. The invariants of your data structures
# could be violated at practically any time because of these interruptions,
# leaving your program in a corrupted state.

# For example, say you want to write a program that counts many things in
# parallel, like sampling light levels from a whole network of sensors. If you
# want to determine the total number of light samples over time, you can
# aggregate them with a new class.


class Counter(object):
    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset


# Imagine that each sensor has its own worker thread because reading from the
# sensor requires blocking I/O. After each sensor measurement, the worker
# thread increments the counter up to a maximum number of desired readings.


def worker(sensor_index, how_many, counter):
    for _ in range(how_many):
        # Read from the sensor
        counter.increment(1)


# Here, I define a function that starts a worker thread for each sensor and
# waits for them all to finish their readings:


def run_threads(func, how_many, counter):
    threads = []
    for i in range(5):
        args = (i, how_many, counter)
        thread = Thread(target=func, args=args)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


# Running five threads in parallel seems simple, and the outcome should be
# abvious.


how_many = 10**5
counter = Counter()
run_threads(worker, how_many, counter)
print('Counter should be %d, found %d' % (5 * how_many, counter.count))
# Counter should be 500000, found 468713


# But this result is way off!  What happened here? How could something so
# simple go so wrong, especially since only one Python interpreter thread can
# run at a time?

# The Python interpreter enforces fairness between all of the threads that
# are executing to ensure they get a roughly equal amount of processing time.
# To do this, Python will suspend a thread as it's running and will resume
# another thread in turn. The problem is that you don't know exactly when
# Python will suspend your threads. A thread can even be paused seemingly
# halfway through what looks like an atomic operation. That's what happened
# in this case.

# The Counter object's increment method looks simple.
#     counter.count += offset
# But the += operator used on an object attribute actually instructs Python to
# do three separate operations behind the scenes. The statement above is
# equivalent to this:
#     value = getattr(counter, 'count')
#     result = value + offset
#     setattr(counter, 'count', result)

# Python threads incrementing the counter can be suspended between any two of
# these of these operations. This is problematic if the way the operations
# interleave causes old versions of value to be assigned to the counter. Here
# is an example of bad interaction between two threads, A and B:


# Running in thread A
value_a = getattr(counter, 'count')
# context switch to thread B
value_b = getattr(counter, 'count')
result_b = value_b + 1
setattr(counter, 'count', result_b)
# context switch back to Thread A
result_a = value_a + 1
setattr(counter, 'count', result_a)


# Thread A stomped on thread B, erasing all of its progress incrementing the
# counter. This is exactly what happened in the right sensor example above.

# To prevent data races like these and other forms of data structure
# corruption, Python includes a robust set of tools in the threading built-in
# module. The simplest and most useful of them is the Lock class, a
# mutual-exclusion lock (mutex).

# By using a lock, I can have the Counter class protect its current value
# against simultaneous access from multiple threads. Only one thread will be
# able to acquire the lock at a time. Here, I use a with statement to acquire
# and release the lock; this makes it easier to see which code is executing
# while the lock is held (see Item 43: "Consider contextlib and with
# statements for reusable try/finally behavior" for details):


class LockingCounter(object):
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        with self.lock:
            self.count += offset


# Now I run the worker threads as before, but use a LockingCounter instead.

counter = LockingCounter()
run_threads(worker, how_many, counter)
print('Counter should be %d, found %d' % (5 * how_many, counter.count))
# Counter should be 500000, found 500000

# The result is exactly what I expect. The Lock solved the problem.


# Things to remember

# 1. Even though Python has a global interpreter lock, you're still
#     responsible for protecting against objects without locks.
# 2. Your programs will corrupt their data structures if you allow multiple
#     threads to modify the same objects without locks.
# 3. The lock class in the threading built-in module is Python's standard
#     mutual exclusion lock implementation.
