# Item 58: Profile before optimizing
from random import randint
from profile import Profile
from pstats import Stats
from bisect import bisect_left


# The dynamic nature of Python causes surprising behaviors in its runtime
# performance. Operations you might assume are slow are actually very fast
# (string manipulation, generators). Language features you might assume are
# fast are actually very slow (attribute access, function calls). The true
# source of slowdowns in a Python program can be obscure.

# The best approach is to ignore your intuition and directly measure the
# performance of a program before you try to optimize it. Python provides a
# built-in profiler for determining which parts of a program are responsible
# for its execution time. This lets you focus your optimization efforts on
# the biggest sources of trouble and ignore parts of the program that don't
# impact speed.

# For example, say you want to determine why an algorithm in your program is
# slow. Here, I define a function that sorts a list of data using an insertion
# sort.


def insertion_sort(data):
    result = []
    for value in data:
        insert_value(result, value)
    return result


# The core mechanism of the insertion sort is the function that finds the
# insertion point for each piece of data. Here, I define an extremely
# inefficient version of the insert_value function that does a linear scan
# over the input array:


def insert_value(array, value):
    for i, existing in enumerate(array):
        if existing > value:
            array.insert(i, value)
            return
    array.append(value)


# To profile insertion_sort and insert_value, I create a data set of random
# numbers and define a test function to pass to the profiler.

max_size = 10**4
data = [randint(0, max_size) for _ in range(max_size)]
print(data)
test = lambda: insertion_sort(data)

# Python provides two built-in profilers, one that is pure Python (profile)
# and another that is a C-extension module (cProfile). The cProfile built-in
# module is better because of its minimal impact on the performance of your
# program while it's being profiled. The pure-Python alternative imposes a
# high overhead that will skew the results.

# Note
# When profiling a Python program, be sure that what you're measuring is the
# code itself and not any external systems. Beware of functions that access
# the network or resources on disk. These may appear to have a large impact on
# your program's execution time because of the slowness of the underlying
# system. If your program uses a cache to mask the latency of slow resources
# like these, you should also ensure that it's properly warmed up before you
# start profiling.

# Here, I instantiate a Profile object from the cProfile module and run the
# test function through it suing the runcall method:

profiler = Profile()
profiler.runcall(test)

# Once the test function has finished running, I can extract statistics about
# its performance using the pstats built-in module and its Stats class.
# Various methods on a Stats object adjust how to select and sort the
# profiling information to show only the things you care about.

stats = Stats(profiler)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_stats()

# The output is a table of information organized by function. The data sample
# is taken only from the time the profiler was active, during the runcall
# method above.

# 20004 function calls in 1.495 seconds
#
#    Ordered by: cumulative time
#
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    0.000    0.000    1.495    1.495 profile:0(<function <lambda> at 0x7f0b2a8af048>)
#         1    0.000    0.000    1.495    1.495 item_58_profile_before_optimizing.py:52(<lambda>)
#         1    0.018    0.018    1.495    1.495 item_58_profile_before_optimizing.py:25(insertion_sort)
#     10000    1.454    0.000    1.477    0.000 item_58_profile_before_optimizing.py:38(insert_value)
#      9992    0.023    0.000    0.023    0.000 :0(insert)
#         1    0.000    0.000    0.000    0.000 :0(setprofile)
#         8    0.000    0.000    0.000    0.000 :0(append)
#         0    0.000             0.000          profile:0(profiler)

# Here's a quick guide to what the profiler statistics columns mean:
# 1. ncalls: The number of calls to the function during the profiling period.
# 2. tottime: The number of seconds spent executing the function, excluding
#    time spent executing other functions it calls.
# 3. totime percall: The average number of seconds spents in the function each
#    time it was called, executing time spent executing other functions it
#    calls. This is tottime divided by ncalls.
# 4. cumtime: The cumulative number of seconds spent executing the function,
#    including time spent in all other function it calls.
# 5. cumtime percall: The average number of seconds spent in the function each
#    time it was called, including time spent in all other functions it calls.
#    This is cumtime divided by ncalls.

# Looking at the profiler statistics table above, I can see that the biggest
# use of CPU in my test is the cumulative time spent in the insert_value
# function. Here, I redefine that function to use the bisect built-in module
# (see Item 46: "Use built-in algorithms and data structures"):


def insert_value_bi(array, value):
    i = bisect_left(array, value)
    array.insert(i, value)


# I can run the profiler again and generate a new table of profiler
# statistics. The new function is much faster, with a cumulative time spent
# that is nearly 100 times smaller than the previous insert_value function.


def insertion_sort_bi(data):
    result = []
    for value in data:
        insert_value_bi(result, value)
    return result


data = [randint(0, max_size) for _ in range(max_size)]
print(data)
test_bi = lambda: insertion_sort_bi(data)
profiler_bi = Profile()
profiler_bi.runcall(test_bi)
stats_bi = Stats(profiler_bi)
stats_bi.strip_dirs()
stats_bi.sort_stats('cumulative')
stats_bi.print_stats()
# 30004 function calls in 0.075 seconds
#
#    Ordered by: cumulative time
#
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    0.000    0.000    0.075    0.075 profile:0(<function <lambda> at 0x7f6dbd4861e0>)
#         1    0.000    0.000    0.075    0.075 item_58_profile_before_optimizing.py:142(<lambda>)
#         1    0.014    0.014    0.075    0.075 item_58_profile_before_optimizing.py:133(insertion_sort_bi)
#     10000    0.028    0.000    0.061    0.000 item_58_profile_before_optimizing.py:123(insert_value_bi)
#     10000    0.019    0.000    0.019    0.000 :0(insert)
#     10000    0.014    0.000    0.014    0.000 :0(bisect_left)
#         1    0.000    0.000    0.000    0.000 :0(setprofile)
#         0    0.000             0.000          profile:0(profiler)

# Sometimes, when you're profiling an entire program, you'll find that a
# common utility function is responsible for the majority of execution time.
# The default output from the profiler makes this situation difficult to
# understand because it doesn't show how the utility function is called by
# many different parts of your program.

# For example, here the my_utility function is called repeatedly by two
# different functions in the program:


def my_utility(a, b):
    if a > b:
        return a + b
    else:
        return a * b


def first_func():
    for _ in range(100000):
        my_utility(4, 5)


def second_func():
    for _ in range(1000):
        my_utility(3, 1)


def my_program():
    for _ in range(20):
        first_func()
        second_func()


# Profiling this code and using the default print_stats output will generate
# output statistics that are confusing.

profiler_my = Profile()
profiler_my.runcall(my_program)
stats_my = Stats(profiler_my)
stats_my.strip_dirs()
stats_my.sort_stats('cumulative')
stats_my.print_stats()
# 2020043 function calls in 3.648 seconds
#
#    Ordered by: cumulative time
#
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    0.000    0.000    3.648    3.648 profile:0(<function my_program at 0x7fbbebba8400>)
#         1    0.000    0.000    3.648    3.648 item_58_profile_before_optimizing.py:190(my_program)
#        20    2.005    0.100    3.612    0.181 item_58_profile_before_optimizing.py:180(first_func)
#   2020000    1.623    0.000    1.623    0.000 item_58_profile_before_optimizing.py:173(my_utility)
#        20    0.020    0.001    0.035    0.002 item_58_profile_before_optimizing.py:185(second_func)
#         1    0.000    0.000    0.000    0.000 :0(setprofile)
#         0    0.000             0.000          profile:0(profiler)

# The my_utility function is clearly the source of most execution time, but
# it's not immediately obvious why that function is called so much. If you
# search through the program's code, you'll find multiple call sites for
# my_utility and still be confused.

# To deal with this, the Python profiler provides a way of seeing which
# callers contributed to the profiling information of each function.

stats_my.print_callers()

# This profiler statistics table shows functions called on the left and who
# was responsible for making the call on the right. Here, it's clear that
# my_utility is most used by first_func:

# Ordered by: cumulative time
#
# Function                                               was called by...
# profile:0(<function my_program at 0x7f2b11841400>)     <- profile:0(profiler)(1)    0.000
# item_58_profile_before_optimizing.py:190(my_program)   <- profile:0(<function my_program at 0x7f2b11841400>)(1)    3.869
# item_58_profile_before_optimizing.py:180(first_func)   <- item_58_profile_before_optimizing.py:190(my_program)(20)    3.869
# item_58_profile_before_optimizing.py:173(my_utility)   <- item_58_profile_before_optimizing.py:180(first_func)(2000000)    3.831
#                                                           item_58_profile_before_optimizing.py:185(second_func)(20000)    0.037
# item_58_profile_before_optimizing.py:185(second_func)  <- item_58_profile_before_optimizing.py:190(my_program)(20)    3.869
# :0(setprofile)                                         <- profile:0(<function my_program at 0x7f2b11841400>)(1)    3.869
# profile:0(profiler)                                    <-

# Things to remember

# 1. It's import to profile Python programs before optimizing because the
#    source of slowdowns is often obscure.
# 2. Use the cProfile module instead of the profile module because it provides
#    more accurate profiling information.
# 3. The Profile object's runcall method provides everything you need to
#    profile a tree of function calls in isolation.
# 4. The Stats object lets you select and print the subset of profiling
#    information you need to see to understand your program's performance.
