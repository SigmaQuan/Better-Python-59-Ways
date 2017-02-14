# Chapter 2: Functions


# The first organizational tool programmers use in Python is the function. As
# in other programming language, functions enable you to break large programs
# into smaller pieces. They improve read-ability and make code more
# approachable. They allow for reuse and refactoring.

# Functions in Python have a variety of extra features that make the
# programmer's life easier. Some are similar to capabilities in other
# programming languages, but many are unique to Python. These extras can
# eliminate noise and clarify the intention of callers. They can significantly
# reduce subtle bugs that are difficult to find.


# Item 14: Prefer exceptions to returning None


# When writing utility functions, there's a draw for Python programmers to
# give special meaning to the return value of None. It seems to makes sense
# in some cases. For example, say you want a helper function that divides one
# number by another. In the case of dividing by zero, returning None seems
# natural because the results is undefined.


def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


# Code using this function can interpret the return value accordingly.


x, y = 1, 2
# Result is not None
# x, y = 1, 0
# Invalid inputs
result = divide(x, y)
if result is None:
    print('Invalid inputs')
else:
    print('Result is not None')


# What happens when the numerator is zero? That will cause the return value
# to be zero (if the denominator is non-zero). This can cause problems when
# you evaluate the result in a condition like an if statement. You may
# accidentally look for any False equivalent value to indicate errors instead
# of only looking for None (see Item 4: "What helper functions instead of
# complex expressions" for a similar situation).


x, y = 0, 5
result = divide(x, y)
if not result:
    print('Invalid inputs')  # This is wrong!
# Invalid inputs


# This is a common mistake in Python code when None has special meaning. This
# is why returning None from a function is error prone. There are two ways to
# reduce the chance of such error.

# The first way is to split the return value into a two-tuple. The first part
# of the tuple indicates that the operation was a success or failure. The
# second part is the actual result that was computed.


def divide(a, b):
    try:
        return True, a / b
    except ZeroDivisionError:
        return False, None


# Caller of this function have to unpack the tuple. That forces them to
# consider the status part of the tuple instead of just looking at the
# result of division.


success, result = divide(x, y)
if not success:
    print('Invalid inputs')
else:
    print('Success')
# Success


# The problem is that callers can easily ignore the first part of the tuple
# (using the underscore variable name, a Python convention for unused
# variables). The resulting code doesn't look wrong at first glance. This
# is as bad as just returning None.


_, result = divide(x, y)
if not result:
    print('Invalid inputs')
else:
    print('Get result')
# Invalid inputs


# The second better way to reduce these errors is to never return None at all.
# Instead, raise an exception up to the caller and make them deal with it.
# Here, I turn a ZeroDivisionError into a ValueError to indicate to the caller
# the input values are bad:


def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs') from e


# Now the caller should handle the exception for the invalid input case (this
# behavior should be documented; see Item 49: "Write docstrings for every
# function, class and module"). The caller no longer requires a condition on
# the return value of the function. If the function didn't raise an exception,
# then the return value must be good. The outcome of exception handing is
# clear.


x, y = 5, 2
try:
    result = divide(x, y)
except ValueError:
    print('Invalid inputs')
else:
    print('Result is %.2f' % result)
# Result is 2.50


# Things to remember

# 1. Functions that return None to indicate special meaning are error prone
#     because None and other values (e.g., zero, the empty string) all
#     evaluate to False in conditional expressions.
# 2. Raise exceptions to indicate special situations instead of returning
#     None. Expect the calling code to handle exceptions properly when they
#     are documented.
