# Item 23: Accept functions for simple interfaces instead of classes
from collections import defaultdict


# Many of Python' built-in APIs allow you to customize behavior by passing
# in a function. These hooks are used by APIs to call back your code while
# they execute. For example, the list type's sort method takes an optional key
# argument that's used to determine each index's value for sorting. Here, I
# sort a list of names based on their lengths by providing a lambda expression
# as the key hook:


names = ['Socrates', 'Archimedes', 'Plato', 'Aristotle']
names.sort(key=lambda x: len(x))
print(names)
# ['Plato', 'Socrates', 'Aristotle', 'Archimedes']


# In other language, you might expect hooks to be defined by an abstract
# class. In Python, many hooks are just stateless functions with well-
# defined arguments and return values. Functions are ideal for hooks because
# they are easier to describe and simpler to define than classes. Functions
# work as hooks because Python has first-class functions: Functions and
# methods can be passed around and referenced like any other value in the
# language.

# For example, say you want to customize the behavior of the defaultdict class
# (see Item 46: "Use built-in algorithms and data structures" for details).
# This data structure allows you to supply a function that will be called each
# time a missing key is accessed. The function must return the default value
# the missing key should have in the dictionary. Here, I define a hook that
# logs each time a key is missing and return 0 for the default value:


def log_missing():
    print('Key added')
    return


# Given an initial dictionary and a set of desired increments, I can cause the
# log_missing function to run and print twice (for 'red' and 'orange').


current = {'green': 12, 'blue': 3}
increments = [
    ('red', 5),
    ('blue', 17),
    ('orange', 9),
]
result = defaultdict(log_missing, current)
print('Before:', dict(result))
for key, amount in increments:
    # result[key] += amount
    result[key] = amount
print('After:', dict(result))
# line 53, in <module>
#     result[key] += amount
# TypeError: unsupported operand type(s) for +=: 'NoneType' and 'int'
# Before: {'blue': 3, 'green': 12}
# After: {'blue': 17, 'green': 12, 'red': 5, 'orange': 9}


# Supplying functions like log_missing makes APIs easy to build and test
# because it separates side effects from deterministic behavior. For example,
# say you now want the default value hook passed to defaultdict to count the
# total number of keys that were missing. One way to achieve this is using
# a stateful closure (see Item 15: "Know how to closures interact with
# variable scope" for details). Here, I define a helper function that uses
# such a closure as the default value hook:


def increment_with_report(current, increments):
    added_count = 0

    def missing():
        nonlocal added_count  # Stateful closure
        added_count += 1
        return 0

    result = defaultdict(missing, current)
    for key, amount in increments:
        result[key] += amount

    return result, added_count


# Running this function produces the expected results (2), even though the
# defaultdict has no idea that the missing hook maintains state. This is
# another benefit of accepting simple functions for interfaces. It's easy to
# add functionality later by hiding state in a closure.


result, count = increment_with_report(current, increments)
assert count == 2
print('After:', dict(result))
# After: {'orange': 9, 'blue': 20, 'green': 12, 'red': 5}


# The problem with defining a closure for stateful hooks is that it's harder
# to read than the stateless function example. Another approach is to define
# a small class that encapsulates the state you want to track.


class CountMissing(object):
    def __init__(self):
        self.added = 0

    def missing(self):
        self.added += 1
        return 0


# In other languages, you might expect that now defaultdict would have to be
# modified to accommodate the interface of CountMissing. But in Python, thanks
# to first-class functions, you can reference the CountMissing.missing method
# directly on an object and pass it to defaultdict as the default value hook.
# it's trivial to have a method satisfy a function interface.


counter = CountMissing()
result = defaultdict(counter.missing, current)  # Method ref

for key, amount in increments:
    result[key] += amount
assert counter.added == 2
print('After:', dict(result))
# After: {'orange': 9, 'blue': 20, 'green': 12, 'red': 5}


# Using a helper class like this to provide the behavior of a stateful closure
# is clearer than increment_with_report function above. However, in isolation
# it's still not immediately obvious that the purpose of the CountMissing
# class is. Who constructs a CountMissing object? Who calls the missing
# method? Will the class need other public methods to be added in the future?
# Until you see its usage with defaultdict, the class is a mystery.

# To clarify this situation, Python allows classes to define the __call__
# special method, __call__ allows an object to be called just like a function.
# It also causes the callable built-in function to return True for such an
# instance.


class BetterCountMissing(object):
    def __init__(self):
        self.added = 0

    def __call__(self):
        self.added += 1
        return 0

counter = BetterCountMissing()
counter()
assert callable(counter)


# Here, I use a BetterCountMissing instance as the default value hook for a
# defaultdict to track the number of missing keys that were added:


counter = BetterCountMissing()
result = defaultdict(counter, current)  # Relies on __call__
for key, amount in increments:
    result[key] += amount
assert counter.added == 2
print('After:', dict(result))
# After: {'orange': 9, 'blue': 20, 'green': 12, 'red': 5}


# This is much clearer than the CountMissing.missing example. The __call__
# method indicates that a class's instances will be used somewhere a function
# argument would also be suitable (like API hooks). It directs new readers of
# the code to the entry point that's responsible for the class's primary
# behavior. It provides a strong hint that the goal of the class is to act as
# a stateful closure.

# Best of all, defaultdict still has no view into what's going on when you
# use __call__. All that defaultdict requires is a function for the default
# value hook. Python provides many different ways to satisfy a simple function
# interface depending on what you need to accomplish.


# Things to remember

# 1. Instead of defining and instantiating classes, functions are often all
#    you need for simple interfaces between components in Python.
# 2. References to functions and methods in Python are first class, meaning
#    they can be used in expressions like any other type.
# 3. The __call__ special method enables instances of a class to be called
#    like plain Python functions.
# 4. When you need a function to maintain state, consider defining a class
#    that provides the __call__ method instead of defining a stateful closure
#    (see Item 15: "Know how closures interact with variable scope").
