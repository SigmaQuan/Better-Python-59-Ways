# Item 59: Use tracemalloc to understand memory usage and leaks


# Memory management in the default implementation of Python, CPython, uses
# reference counting. This ensures that as soon as all references to an
# object have expired, the referenced object is also cleared. CPython also
# has a built-in cycle detector to ensure that self-referencing objects are
# eventually garbage collected.

# In theory, this means that most Python programmers don't have to worry about
# allocating or deallocating memory in their programs. It's taken care of
# automatically by the language and the CPython runtime. However, in practice,
# programs eventually do run out of memory due to held reference. Figuring out
# where your Python programs are using or leaking memory proves to be a
# challenge.

# The first way to debug memory usage is to ask the gc built-in module to list
# every object currently known by the garbage collector. Although it's quite
# a blunt tool, this approach does let you quickly get a sense of where your
# program's memory is being used.

# Here, I run a program that wastes memory by keeping references. It prints
# out how many objects were created during execution and a small sample of
# allocated objects.

# item_59_use_tracemalloc_using_pc.py
import item_59_use_tracemalloc_using_gc
# 4944 objects before
# 4955 objects after
# {'_loaders': [('.cpython-35m-x86_64-linux-gnu.so', <class '_frozen_importlib_external.ExtensionFileL
# set()
# {'imageio', 'mujoco_py-0.5.7-py3.5.egg-info', 'pip', 'keras_tqdm', 'pyglet-1.2.4.dist-info', 'easy-i

# The problem with gc.get_objects is that it doesn't tell you anything about
# how the objects were allocated. In complicated programs, a specific class
# of object could be allocated many different ways. The overall number of
# objects isn't nearly as important as identifying the code responsible for
# allocating the objects that are leaking memory.

# Python 3.4 introduces a new tracemalloc built-in module for solving this
# problem. tracemalloc makes it possible to connect an object back to where
# it was allocated. Here, I print out the top three memory usage offenders in
# a progam using tracemalloc:

# item_59_use_tracemalloc_top_n.py
import item_59_use_tracemalloc_top_n
# /home/robot/Documents/PycharmProjects/BetterPython59Ways/item_59_use_tracemalloc_waste_memory.py:7: size=3539 KiB (+3539 KiB), count=100000 (+100000), average=36 B
# /home/robot/Documents/PycharmProjects/BetterPython59Ways/item_59_use_tracemalloc_top_n.py:6: size=1264 B (+1264 B), count=2 (+2), average=632 B
# <frozen importlib._bootstrap_external>:476: size=485 B (+485 B), count=6 (+6), average=81 B

# It's immediately clear which objects are dominating my program's memory
# usage and where in the source code they were allocated.

# The tracemalloc module can also print out the full stack trace of each
# allocation (up to the number of frames passed to the start method). Here, I
# print out the stack trace of the biggest source of memory usage in the
# program:

# item_59_use_tracemalloc_with_trace.py
import item_59_use_tracemalloc_with_trace
# File "/home/robot/Documents/PycharmProjects/BetterPython59Ways/item_59_use_tracemalloc_waste_memory.py", line 7
#     a.append(10 * 230 * i)
#   File "/home/robot/Documents/PycharmProjects/BetterPython59Ways/item_59_use_tracemalloc_with_trace.py", line 6
#     x = waste_memory.run()

# A stack trace like this is most valuable for figuring out which particular
# usage of a common function is responsible for memory consumption in a
# program.

# Unfortunately, Python 2 doesn't provide the tracemalloc built-in module.
# There are open source packages for tracking memory usage in Python 2 (such
# as heapy), though they do not fully replicate the functionality of
# tracemalloc.


# Things to remember

# 1. It can be difficult to understand how Python programs use and leak
#    memory.
# 2. The gc module can help you understand which objects exist, but it has no
#    information about how they were allocated.
# 3. The tracemalloc built-in module provides powerful tools for understanding
#    the source of memory usage.
# 4. tracemalloc is only available in Python 3.4 and above.
