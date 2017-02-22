# Item 19: Provide optimal behavior with keyword arguments


# Like most other programming languages, calling a function in Python allows
# for passing arguments by position.


def remainder(number, divisor):
    return number % divisor


assert remainder(20, 7) == 6


# All positional arguments to Python functions can also be passed by keyword,
# where the name of the argument is used in an assignment within the
# parentheses of a function call. The keyword arguments can be passed in any
# order as long as all of the required positional arguments are specified.
# You can mix and match keyword and positional arguments. There calls are
# equivalent.


print(remainder(20, 7))
print(remainder(20, divisor=7))
print(remainder(number=20, divisor=7))
print(remainder(divisor=7, number=20))
# 6
# 6
# 6
# 6


# Positional arguments must be specified before keyword arguments.


# remainder(number=20, 7)
# line 36
#     remainder(number=20, 7)
# SyntaxError: non-keyword arg after keyword arg


# Each argument can only be specified noce.


# remainder(20, number=7)
# line 45, in <module>
#     remainder(20, number=7)
# TypeError: remainder() got multiple values for keyword argument 'number'


# The flexibility of keyword arguments provides three significant benefits.

# The first advantage is that keyword arguments make the function call clearer
# to new reader of the code. With the call remainder(20, 7), it's not evident
# looking at the implementation of the remainder method. In the call with
# keyword arguments, number=20 and divisor=7 make it immediately obvious which
# parameter is being used for each purpose.

# The second impact of arguments is that they can have default values
# specified in the function definition. This allows a function to provide
# additional capabilities when you need them but lets you accept the default
# behavior most of the time. This can eliminate repetitive code and reduce
# noise.

# For example, say you want to compute the rate of fluid flowing into a vat.
# If the vat is also on a scale, then you could use the difference between two
# weight measurements at two different times to determine the flow rate.


def flow_rate(weight_diff, time_diff):
    return weight_diff / time_diff

weight_diff = 0.5
time_diff = 3
flow = flow_rate(weight_diff, time_diff)
print('%.3f kg per second' % flow)
# 0.167 kg per second


# In the typical case, it's useful to know the flow rate in kilograms per
# second. Other times, it'd be helpful to use the last sensor measurements
# to larger time scales, like hours or days. You can provide this behavior
# in the same function by adding an argument for the time period scaling
# factor.


def flow_rate(weight_diff, time_diff, period):
    return (weight_diff / time_diff) * period


# The problem is that now you need to specify the period argument every time
# you call the function, even in the common case of flow rate per second (
# where the period is 1).


flow_per_second = flow_rate(weight_diff, time_diff, 1)


# To make this less noisy, I can give the period arguments a default value.


def flow_rate(weight_diff, time_diff, period=1):
    return (weight_diff / time_diff) * period


# The period argument is now optional.


flow_per_second = flow_rate(weight_diff, time_diff)
flow_per_hour = flow_rate(weight_diff, time_diff, period=3600)
print(flow_per_second)
print(flow_per_hour)
# 0.166666666667
# 600.0


# This works well for simple default values (it gets tricky for complex
# default values--see Item 20: "Use None and Docstrings to specify dynamic
# default arguments").

# The third reason to use keyword arguments is that they provide a powerful
# way to extend a function's parameters while remaining backwards compatible
# with existing callers. This lets you provide additional functionality
# without having to migrate a lot of code, reducing the chance of introducing
# bugs.


def flow_rate(weight_diff, time_diff, period=1, units_per_kg=1):
    return ((weight_diff / units_per_kg) / time_diff) * period


# The default argument value for units_per_kg is 1, which makes the return
# weight units remain as kilograms. This means that all existing callers will
# see no change in behavior. New callers to flow_rate can specify the new
# keyword argument to see the new behavior.


pounds_per_hour = flow_rate(
    weight_diff, time_diff, period=3600, units_per_kg=2.2)
print(pounds_per_hour)
# 272.727272727


# The only problem with this approach is that optional keyword arguments like
# period and units_per_kg may still be specified as positional arguments.


pounds_per_hour = flow_rate(weight_diff, time_diff, 3600, 2.2)
print(pounds_per_hour)
# 272.727272727


# Supplying optional arguments positionally can be confusing because it isn't
# clear that the values 3600 and 2.2 correspond to. The best practice is to
# always specify optional arguments using the keyword names and never pass
# them as positional arguments.

# Note:
# Backwards compatibility using optional keyword arguments like this is
# crucial for functions that accept *args (see Item 18: "Reduce visual noise
# with variable positional arguments"). But a even better practice is to use
# keyword-only arguments (see Item 21: "Enforce clarity with keyword-only
# arguments").


# Things to remember

# 1. Function arguments can be specified by position or by keyword.
# 2. Keywords make it clear what the purpose of each arguments is when it
#    would be confusing with only positional arguments.
# 3. Keywords arguments with default values make it easy to add new behaviors
#    to a function, especially when the function has existing callers.
# 4. Optional keyword arguments should always be passed by keyword instead of
#    by position.
