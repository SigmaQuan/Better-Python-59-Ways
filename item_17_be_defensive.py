# Item 17: Be defensive when iterating over arguments


# When a function takes a list of objects as a parameter, it's often important
# to iterate over that list multiple times. For example, say you want to
# analyze tourism number for the U.S. state of Texas. Imagine the data set is
# the number of visitors to each city (in millions per year). You'd like to
# figure out what percentage of overall tourism each city receives.

# To do this you need a normalization function. It sums the inputs to
# determine the total number of tourists per year. Then it divides each city's
# individual visitor count by the total to find that city's contribution to
# the whole.


def normalize(numbers):
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result


# This function works when given a list of visits.


visits = [15, 35, 80]
percentages = normalize(visits)
print(percentages)
# [11.538461538461538, 26.923076923076923, 61.53846153846154]


# To scale this up, I need to read the data from a file that contains every
# city in all of Texas. I define a generator to do this because then I can
# reuse the same function later when I want to compute tourism numbers for the
# whole world, a much larger data set (see Item 16: "Consider generators
# instead of returning lists").


def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)


# Surprisingly, calling normalize on the generator's return value produces no
# results.


path = 'item_17_my_numbers.txt'
it = read_visits(path)
percentages = normalize(it)
print(percentages)
# []


# The cause of this behavior is that an iterator only produces results a
# single time. If you iterate over an iterator or generator that has
# already raised a StopIteration exception, you won't get any results the
# second time around.


it = read_visits(path)
print(list(it))
print(list(it))
# [15, 35, 80]
# []


# What's confusing is that you also won't get any errors when you iterate over
# an already exhausted iterator. for loops, the list constructor, and many
# other throughout the Python standard library expect the StopIteration
# exception to be raised during normal operation. These functions can't tell
# the difference between an iterator that has no output and an iterator that
# hand output and is now exhausted.

# To solve this problem, you can explicitly exhaust an input iterator and keep
# a copy of its entire contents in a list. You can then iterate over the list
# version of the data as many times as you need to. Here's the same function
# as before, but it defensively copies the input iterator:


def normalize_copy(numbers):
    numbers = list(numbers)  # Copy of the iterator
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result


# Now the function works correctly on a generator's return value.


it = read_visits(path)
percentages = normalize_copy(it)
print(percentages)
# [11.538461538461538, 26.923076923076923, 61.53846153846154]


# The problem with this approach is the copy of the input iterator's contents
# could be large. Copying the iterator could cause your program to run out of
# memory and crash. One way around this is to accept a function that returns
# a new iterator each time it's called.


def normalize_func(get_iter):
    total = sum(get_iter())  # New iterator
    result = []
    for value in get_iter():  # New iterator
        percent = 100 * value / total
        result.append(percent)
    return result


# To use normalize_func, you can pass in a lambda expression that calls the
# generator and produces a new iterator each time.


percentages = normalize_func(lambda: read_visits(path))
# https://www.quora.com/What-is-lambda-function-in-Python-and-why-do-we-need-it
# https://www.zhihu.com/question/20125256
print(percentages)
# [11.538461538461538, 26.923076923076923, 61.53846153846154]


# Though it works, having to pass a lambda function like this is clumsy. The
# better way to achieve the same result is to provide a new container class
# that implements the iterator protocol.

# The iterator protocol is how Python for loops and related expressions
# traverse the contents of a container type. When Python sees a statement like
# for x in foo will actually call iter(foo). The iter built-in function call
# the foo.__iter__ special method in turn. The __iter__ method mush return
# an iterator object (which itself implements the __next__ special method).
# Then the for loop repeatedly calls the next built-in function on the
# iterator object until it's exhausted (and raise a StopIteration exception).

# It sounds complicated, but practically speaking you can achieve all of this
# behavior for your classes by implementing the __iter__ method as a
# generator. Here, I define an iterable container class that reads the files
# containing tourism data:


class ReadVisits(object):
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)


# This new container type works correctly when passed to the original function
# without any modifications.


visits = ReadVisits(path)
percentages = normalize(visits)
print(percentages)
# [11.538461538461538, 26.923076923076923, 61.53846153846154]


# This works because the sum method in normalize will call
# ReadVisits.__iter__ to allocate a new iterator object. The for loop to
# normalize the numbers will also call __iter__ to a second iterator object.
# Each of those iterators will be advanced and exhausted independently,
# ensuring that each unique iteration sees all of the input data values. The
# only downside of this approach is that it reads the input data multiple
# times.

# Now that you know how containers like ReadVisits work, you can write your
# functions to ensure that parameters aren't just iterator. The protocol
# states that when an iterator is passed to the iter built-in function, iter
# will return the iterator itself. In contrast, when a container type is
# passed to iter, a new iterator object will be returned each time. Thus,
# you can test an input value for this behavior and raise a TypeError to
# reject iterators.


def normalize_defensive(numbers):
    if iter(numbers) is iter(numbers):  # An iterator -- bad!
        raise TypeError('Must supply a container')
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result


# This is ideal if you don't want to copy the full input iterator like
# normalize_copy above, but you also need to iterate over the input data
# multiple times. This function works as expected for list and ReadVisits
# inputs because they are containers. It will work for any type of container
# that follows the iterator protocol.


visits = [15, 35, 80]
print('[] Defensive:')
print(normalize_defensive(visits))
# [] Defensive:
# [11.538461538461538, 26.923076923076923, 61.53846153846154]
visits = ReadVisits(path)
print('Path Denfensive:')
print(normalize_defensive(visits))
# Path Denfensive:
# [11.538461538461538, 26.923076923076923, 61.53846153846154]


# The function will raise an exception if the input is iterable but not a
# container.


it = iter(visits)
print('normalize:')
print(normalize(it))
# normalize:
# []
print('normalize_copy:')
print(normalize_copy(it))
# normalize_copy:
# []
print('normalize_func:')
# print(normalize_func(it))
# TypeError: 'generator' object is not callable
print('normalize_defensive:')
# print(normalize_defensive(it))
# TypeError: Must supply a container


# Things to remember

# 1. Beware of functions that iterate over input arguments multiple times. If
#     these arguments are iterators, you may see strange behavior and missing
#     values.
# 2. Python's iterator protocol defines how containers and iterators interact
#     with the iter and next built-in functions, for loops, and related
#     expression.
# 3. You can easily define your own iterable container type by implementing
#     the __iter__ method as a generator.
# 4. You can detect that a value is an iterator (instead of a container) if
#     calling iter on it twice produces the same result, which can then be
#     progressed with the next built-in function.
