# Item 9: Consider generator expressions for large comprehensions


# The problem with list comprehensions (see Item 7: Use list comprehensions
# instead of map and filter) is that they may create a whole new list
# containing one item for each value in the input sequence. This is fine for
# small inputs, but for large inputs this could consume significant amounts of
# memory and cause your program to crash.

# For example, say you want to read a file and return the number of
# characters on each line. Doing this with a list comprehension would require
# holding the length of every line of the file in memory. If the file is
# absolutely enormous or perhaps a never-ending network socket, list
# comprehensions are problematic. Here, I use a list comprehension in a way
# that can only handle small input values.


value = [len(x) for x in open('item_09_generator_expressions.py')]
print(value)
# [66, 1, 1, 76, 70, 77, 79, 42, 1, 68, 78, 73, 69, 76, 43, 1, 1, 46, 12]
print("line: %d, max length: %d\n" % (len(value), max(value)))
# line: 39, max length: 79


# To solve this, Python provides generator expressions, a generalization of
# list comprehensions and generators. Generator expressions don't materialize
# the whole output sequence when they're run. Instead, generator expressions
# evaluate to an iterator that yields one item at a time form the expression.

# A generator expression is created by putting list-comprehension-like syntax
# between () characters. Here, I use a generator expression that is equivalent
# to the code above. However, the generator expression immediately evaluates
# to an iterator and doesn't make any forward progress.


it = (len(x) for x in open('item_09_generator_expressions.py'))
print(it)
# <generator object <genexpr> at 0x7f5f396eaa40>


# The returned iterator can be advanced one step at a time to produce the next
# output from the generator expression as needed (using the next built-in
# function). Your code can consume as much of the generator expression as you
# want without risking a blowup in memory usage.


print(next(it))
print(next(it))
# 66
# 1


# Another powerful outcome of generator expressions is that they can be
# composed together. Here, I take the iterator returned by the generator
# expression above and use it as the input for another generator expression.


roots = ((x, x**0.5) for x in it)
print(next(roots))
print(next(roots))
# (1, 1.0)
# (76, 8.717797887081348)


# Each time I advance this iterator, it will also advance the interior
# iterator, creating a domino effect of looping, evaluating
# conditional expressions, and passing around inputs and outputs.


print(next(roots))
# (70, 8.366600265340756)


# Chaining generators like this executes very quickly in Python. When you're
# looking for a way to compose functionality that's operating on a large
# stream of input, generator expressions are the best tool for the job.
# The only gotcha is that the iterators returned by generator expressions are
# stateful, so you must be careful not to use them more than once (see Item
# 17: Be defensive when iterating over arguments).


# Things to remember

# 1. List comprehensions can cause problems for large inputs by using too much
#     memory.
# 2. Generator expressions avoid memory issues by producing outputs one at a
#     time as an iterator.
# 3. Generator expressions can be composed by passing the iterator from one
#     generator expression into the for subexpression of another.
# 4. Generator expressions execute very quickly when chained together.
