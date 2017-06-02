# Item 43: Consider contextlib and with statements for reusable try/finally
# behavior
from threading import Lock
import logging
from contextlib import contextmanager


# The with statement in Python is used to indicate when code is running in a
# special context. For example, mutual exclusion locks (see Item 38: "Use lock
# to prevent data races in threads") can be used in with statements to
# indicate that the indented code only runs while the lock is held.

lock = Lock()
with lock:
    print('Lock is held')

# The example above is equivalent to this try/finally construction because the
# Lock class properly enables the with statement.

lock.acquire()
try:
    print('Lock is held')
finally:
    lock.release()

# The with statement version of this is better because it eliminates the need
# to write the repetitive code of the try/finally construction. It's easy to
# make your objects and functions capable of use in with statements by using
# the contextlib built-in module. This module contains the contextmanager
# decorator, which lets a simple function be used in with statements. This is
# much easier than defining a new class with the special methods __enter__ and
# __exit__ (the standard way).

# For example, say you want a region of your code to have more debug logging
# sometimes. Here, I define a function that does logging at two severity
# levels:


def my_function():
    logging.debug('Some debug data')
    logging.error('Error log here')
    logging.debug('More debug data')

# The default log level for my program is WARNING, so only the error message
# will print to screen when I run the function.

# my_function()
# ERROR:root:Error log here

# I can elevate the log level of this function temporarily by defining a
# context manager. This helper function boosts the logging severity level
# before running the code in the with block and reduces the logging severity
# level afterward.


@contextmanager
def debug_logging(level):
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield
    finally:
        logger.setLevel(old_level)


# The yield expression is the point at which the with block's contents will
# execute. Any exceptions that happen in the with block will be re-raised by
# the yield expression for you to catch in the helper function (see Item 40:
# "Consider coroutines to run many functions concurrently" for an explanation
# of how that works).

# Now, I can call the sam logging function again, but in the debug_logging
# context. This time, all of the debug messages are printed to the screen
# during the with block. The same function running outside the with block
# won't print debug messages.

with debug_logging(logging.DEBUG):
    print('Inside:')
    my_function()
print('After:')
my_function()
# Inside:
# DEBUG:root:More debug data
# After:
# ERROR:root:Error log here


# Using with Targets

# The context manager passed to a with statement may also return an object.
# This object is assigned to a local variable in the as part of the compound
# statement. This gives the code running in the with block the ability to
# directly interact with its context.

# For example, say you want to write a file and ensure that it's always closed
# correctly. You can do this by passing open to the with statement. open
# returns a file handle for the as target of with and will close the handle
# when the with block exits.

with open('/tmp/my_output.txt', 'w') as handle:
    handle.write('This is some data!')


# This approach is preferable to manually opening and closing the file handle
# every time. It gives you confidence that the file is eventually closed when
# execution leaves the with statement. It also encourages you to reduce the
# amount of code that executes while the file handle is open, which is good
# practice in general.

# To enable your own functions to supply values for as targets, all you need
# to is yield a value from your context manager. For example, here I define
# a context manager to fetch a Logger instance, set its level, and then yield
# it for the as target.


@contextmanager
def log_level(level, name):
    logger = logging.getLogger(name)
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield logger
    finally:
        logger.setLevel(old_level)


# Calling logging methods like debug on the as target will produce output
# because the logging severity level is set how enough in the with block.
# Using the logging module directly won't print anything because the default
# logging severity level for the default program logger is WARNING.


with log_level(logging.DEBUG, 'my_log') as logger:
    logger.debug('This is my message!')
    logging.debug('This will not print')


# After the with statement exits, calling debug logging methods on the Logger
# named 'my-log' will not print anything because the default logging severity
# level has been restored. Error log messages will always print.

logger = logging.getLogger('my_log')
logger.debug('Debug will not print')
logger.error('Error will print')
# DEBUG:my_log:This is my message!
# ERROR:my_log:Error will print


# Things to remember

# 1. The with statement allows you to reuse logic from try/finally blocks and
#    reduce visual noise.
# 2. The contextlib built-in module provides a contextmanager decorator that
#    makes it easy to use your own functions in with statements.
# 3. The value yielded by context managers is supplied to the as part of the
#    with statement. It's useful for letting your code directly access the
#    cause of the special context.
