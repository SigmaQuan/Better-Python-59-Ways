# Item 21: Enforce clarity with key-word only arguments


# Passing arguments by keyword is a powerful feature of Python functions (see
# Item 19: "Provide optimal behavior with keyword arguments"). The flexibility
# of keyword arguments enables you to write code that will be clear for your
# use cases.

# For example, say you want to divide one number by another but be very
# careful about special cases. Sometimes you want to ignore ZeroDivisionError
# exceptions and return infinity instead. Other times, you want to ignore
# OverflowError exceptions and return Zero instead.


def safe_division(number, divisor, ignore_overflow, ignore_zero_division):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise


# Using this function is straightforward. This call will ignore the float
# overflow from division and will return zero.


result = safe_division(1, 100**500, True, False)
print(result)
# 0.0


# This call will ignore the error from dividing by zero and will return
# infinity.


result = safe_division(1, 0, False, True)
print(result)
# inf


# The problem is that it's easy to confuse the position of the two Boolean
# arguments that control the exception-ignoring behavior. This can easily
# cause bugs that are hard to track down. One way to improve the readability
# of this code is to use keyword arguments. By default, the function can be
# overly cautions and can always re-raise exceptions.


def safe_division_b(number, divisor,
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise


# Then callers can use keyword arguments to specify which of the ignore flags
# they want to flip for specific operations, overriding the default behavior.


print(safe_division_b(1, 10**500, ignore_overflow=True))
print(safe_division_b(1, 0, ignore_zero_division=True))
# 0.0
# inf


# The problem is, since these keyword arguments are optional behavior, there's
# nothing forcing callers of your functions to use keyword arguments for
# clarity. Even with the new definition of safe_division_b, you can will still
# call it the old way with positional arguments.


print(safe_division_b(1, 10**500, True, False))
# 0.0


# With complex functions like this, it's better to require that callers are
# clear about their intentions. In Python 3, you can demand clarity by
# defining your functions with keyword-only arguments. These arguments can
# only be supplied by keyword, never by position.

# Here, I redefine the safe_division function to accept keyword-only
# arguments. The * symbol in the argument list indicates the end of positional
# arguments and the beginning of the keyword-only arguments.


def safe_division_c(number, divisor, *,
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise


# Now, calling the function with positional arguments for the keyword argument
# won't work.


# result = safe_division_c(1, 10**500, True, False)
# line 123, in <module>
#     result = safe_division_c(1, 10**500, True, False)
# TypeError: safe_division_c() takes 2 positional arguments but 4 were given


# Keyword arguments and their default values work as expected.


result = safe_division_c(1, 0, ignore_zero_division=True)  # OK
print(result)
# inf

try:
    result = safe_division_c(1, 0)
    print(result)
except ZeroDivisionError:
    print("Exception ZeroDivisionError")
    pass  # Expected
# Exception ZeroDivisionError


# Keyword-only arguments in Python 2

# Unfortunately, Python 2 doesn't have explicit syntax for specifying
# keyword-only arguments like Python 3. But you can achieve the same behavior
# of raising TypeErrors for invalid function calls by using the ** operator in
# in argument list. The ** operator is similar to the * operator (see Item 18:
# "Reduce visual noise with variable positional arguments"), except that
# instead of accepting a variable number of positional arguments, it accepts
# any number of keyword arguments, even when they're not defined.


# Python 2
def print_args(*args, **kwargs):
    print('Positional:', args)
    print('Keyword:   ', kwargs)

print_args(1, 2, foo='bar', stuff='meep')
# ('Positional:', (1, 2))
# ('Keyword:   ', {'foo': 'bar', 'stuff': 'meep'})


# To make safe_division take keyword-only arguments in Python 2, you have the
# function accept **kwargs. Then you pop keyword arguments that you expect out
# of the kwargs dictionary, using the pop method's second argument to specify
# the default value when the key is messing. Finally, you makere sure there are
# no more keyword arguments left in kwargs to prevent callers from supplying
# arguments that are invalid.


# Python 2
def safe_division_d(number, divisor, **kwargs):
    ignore_overflow = kwargs.pop('ignore_overflow', False)
    ignore_zero_div = kwargs.pop('ignore_zero_division', False)
    if kwargs:
        raise TypeError('Unexpected **kwargs: %r' % kwargs)

    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_div:
            return float('inf')
        else:
            raise


# Now you can call the function with or without keyword arguments.


print(safe_division_d(1, 10.0))
print(safe_division_d(1, 0, ignore_zero_division=True))
print(safe_division_d(1, 10**500, ignore_overflow=True))
# 0.1
# inf
# 0.0


# Trying to pass keyword-only arguments by position won't work, just like in Python 3.


# safe_division_d(1, 0, False, True)
# line 209, in <module>
#     safe_division_d(1, 0, False, True)
# TypeError: safe_division_d() takes 2 positional arguments but 4 were given


# Trying to pass unexpected keyword arguments also won't work.


safe_division_d(0, 0, unexpected=True)
# line 179, in safe_division_d
#     raise TypeError('Unexpected **kwargs: %r' % kwargs)
# TypeError: Unexpected **kwargs: {'unexpected': True}


# Things to remember

# 1. Keyword arguments make the intention of a function call more clear.
# 2. Use keyword-only arguments to force callers to supply keyword arguments
#    for potentially confusing functions, especially those that accept
#    multiple Boolean flags.
# 3. Python 3 supports explicit syntax for keyword-only arguments in
#    functions.
# 4. Python 2 can emulate keyword-only arguments for functions by using
#    **kwargs and manually raising TypeError exceptions.
