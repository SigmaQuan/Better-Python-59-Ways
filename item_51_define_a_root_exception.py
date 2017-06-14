# Item 51: Define a root exception to insulate callers from APIs


# When you're defining a module's API, the exceptions you throw are just as
# much a part of your interface as the functions and classes you define (see
# Item 14: "Prefer exceptions to returning None").

# Python has a built-in hierarchy of exceptions for the language and standard
# library. There's a draw to using the built-in exception types for reporting
# errors instead of defining your own new types. For example, you could raise
# a ValueError exception whenever an invalid parameter is passed to your
# function.


def determine_weight(volume, density):
    if density < 0:
        raise ValueError('Density must be positive')
    # ...


# In some cases, using ValueError makes sense, but for APIs it's much more
# powerful to define your own hierarchy of exceptions. You can do this by
# providing a root Exception in your module. Then, have all other exceptions
# raised by that module inherit from the root exception.from

# my_module.py
class Error(Exception):
    """Base-class for all exceptions raised by this module."""
    pass


class InvalidDensityError(Error):
    """There was a problem with a provided density value."""
    pass

# Having a root exception in a module makes it easy for consumers of your API
# to catch all of the exceptions that you raise on purpose. For example, here
# a consumer of your API makes a function all with a try/except statement that
# catches your root exception:

# try:
#     weight = my_module.determine_weight(1, -1)
# except my_module.Error as e:
#     logging.error('Unexpected error: %s', e)

# The try/except prevents your API's exceptions from progagating too far
# upward and breaking the calling program. It insulates the calling code from
# your API. This insulation has three helpful effects.

# First, root exceptions let callers understand when there's a problem with
# their usage of your API. If callers are using your API properly, they should
# catch the various exceptions that you deliberately raise. If they don't
# handle such an exception, it will propagate all the way up to the insulating
# except block that catches your module's root exception. That block can bring
# the exception to the attention of the API consumer, giving them a chance to
# add proper handling of the exception type.

# try:
#     weight = my_module.determine_weight(1, -1)
# except my_module.InvalidDensityError:
#     weight = 0
# except my_module.Error as e:
#     logging.error('Bug in the calling code: %s', e)

# The second advantage of using root exceptions is that they can help find
# bugs in your API module's code. If your code only deliberately raises
# exceptions that you define within your module's hierarchy, then all other
# types of exceptions raised by your module must be the ones that you didn't
# intend to raise. These are bugs in your API's code.

# Using the try/except statement above will not insulate API consumers from
# bugs in your API module's code. To do that, the caller need to add another
# except block that catches Python's base Exception class. This allows the
# API consumer to detect when there's a bug in the API module's implementation
# that needs to be fixed.

# try:
#     weight = my_module.determine_weight(1, -1)
# except my_module.InvalidDensityError:
#     weight = 0
# except my_module.Error as e:
#     logging.error('Bug in the calling code: %s', e)
# except Exception as e:
#     logging.error('Bug in the API code: %s', e)

# The third impact of using root exceptions is future-proofing your API. Over
# time, you may want to expand your API to provide more specific exceptions in
# certain situation. For example, you could add an Exception subclass that
# indicates the error condition of supplying negative densities.


# my_module.py
class NegativeDensityError(InvalidDensityError):
    """A provided density value was negative."""
    pass


def determine_weight(volume, density):
    if density < 0:
        raise NegativeDensityError


# The calling code will continue to work exactly as before because it already
# catches InvalidDensityError exceptions (the parent class of
# NegativeDensityError). In the future, the caller could decide to
# special-case the new type of exception and change its behavior accordingly.

# try:
#     weight = my_module.determine_weight(1, -1)
# except my_module.NegativeDensityError as e:
#     raise ValueError('Must supply non-negative density') from e
# except my_module.InvalidDensityError:
#     weight = 0
# except my_module.Error as e:
#     logging.error('Bug in the calling code: %s', e)
# except Exception as e:
#     logging.error('Bug in the API code: %s', e)

# You can take API future-proofing further by providing a broader set of
# exceptions directly below the root exception. For example, imagine you had
# one set of errors related to calculating weights, another related to
# calculating volume, and a third related to calculating density.


# my_module.py
class WeightError(Error):
    """Base-class for weight calculation errors."""


class VolumeError(Error):
    """Base-class for volume calculation errors."""


class DensityError(Error):
    """Base-class for density calculation errors."""


# Specific exceptions would inherit from these general exceptions. Each
# intermediate exception acts as its own kind of root exception. This makes
# it easier to insulate layers of calling code from API code based on broad
# functionality. This is much better than having all callers catch a long
# list of very specific Exception subclasses.


# Things to remember

# 1. Defining root exceptions for your modules allows API consumers to
#    insulate themselves from your API.
# 2. Catching root exceptions can help you find bugs in code that consumes an
#    API.
# 3. Catching the Python Exception base class can help you find bugs in API
#    implementations.
# 4. Intermediate root exceptions let you add more specific types of
#    exceptions in the future without breaking your API consumers.
