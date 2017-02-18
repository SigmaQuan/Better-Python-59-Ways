# Item 18: Reduce visual noise with variable positional arguments


# Accepting optional positional arguments (often called star args in reference
# to the conventional name for the parameter, *args) can make a function call
# more clear and remove visual noise.

# For example, say you want to log some debug information. With a fixed
# number of arguments, you would need a function that takes a message and a
# list of values.


def log(message, values):
    if not values:
        print(message)
    else:
        valuse_str = ', '.join(str(x) for x in values)
        print('%s: %s' % (message, valuse_str))

log("My numbers are", [1, 2])
log("Hi there", [])
# My numbers are: 1, 2
# Hi there

# Having to pass an empty list when you have no values to log is cumbersome
# and noise. It'd be better to leave out the second argument entirely. You can
# do this in Python by prefixing the last positional parameter with *. The
# first parameter for the log message is required, whereas any number of
# subsequent positional arguments are optional. The function body doesn't
# need to change, only the callers do.


def log(message, *values):  # The only difference
    if not values:
        print(message)
    else:
        valuse_str = ', '.join(str(x) for x in values)
        print('%s: %s' % (message, valuse_str))

log("My numbers are", 1, 2)
log("Hi there")  # Much better
# My numbers are: 1, 2
# Hi there


# If you already have a list and want to call a variable argument function
# like log, you can do this by using the * operator. This instructs Python to
# pass items from the sequence as positional arguments.


favorites = [7, 33, 99]
log('Favorite colors', *favorites)
# Favorite colors: 7, 33, 99


# There are two problems wit accepting a variable number of positional
# arguments.


# 1. The first issue is that the variable arguments are always turned into
# a tuple before they are passed to your function. This means that if the
# caller of your function uses the * operator on a generator, it will be
# iterated until it's exhausted. The resulting tuple will include every value
# from the generator, which could consume a lot of memory and cause your
# program to crash.


def my_generator():
    for i in range(10):
        yield i


def my_func(*args):
    print(args)


it = my_generator()
my_func(*it)
# (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)


# Function that accept *args are best for situations where you know the number
# of inputs in the argument list will be reasonably small. It's ideal for
# function calls that pass many literals or variable names together. It's
# primarily for the convenience of the programmer and the readability of the
# code.

# 2. The second issue with *args is that you can't add new positional
# arguments to your function in the future without migrating every caller. If
# you try to add a positional argument in the front of the argument list,
# existing callers will subtly break if they aren't updated.


def log(sequence, message, *values):
    if not values:
        print('%s: %s' % (sequence, message))
    else:
        values_str = ', '.join(str(x) for x in values)
        print('%s: %s: %s' % (sequence, message, values_str))

log(1, 'Favorites', 7, 33)      # New usage is OK
log('Favorite numbers', 7, 33)  # Old usage breaks
# 1: Favorites: 7, 33
# Favorite numbers: 7: 33


# The problem here is that the second call to log used 7 as the message
# parameter because a sequence argument wasn't given. Bugs like this are
# hard to track down because the code still runs without raising any
# exceptions. To avoid this possibility entirely, you should use
# key-word-only arguments when you want to extend functions that accept *args
# (see Item 21: "Enforce clarity with keyword-only arguments").


# Things to remember

# 1. Functions can accept a variable number of positional arguments by using
#    *args in the def statement.
# 2. You can use the items from a sequence as the positional arguments for a
#    function with the * operator.
# 3. Using the * operator with a generator may cause your program to run out
#    of memory and crash.
# 4. Adding new positional parameters to functions that accept *args can
#    introduce hard-to-find bugs.
