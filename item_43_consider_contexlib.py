# Item 43: Consider contextlib and with statements for reusable try/finally
# behavior
from threading import Lock
import logging



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

my_function()
# ERROR:root:Error log here

# I can elevate the log level of this function temporarily by defining a
# context manager. This helper function boosts the logging severity level
# before running the code in the with block and reduces the logging severity
# level afterward.

# After the with statement exits, calling debug logging methods on the Logger
# named 'my-log' will not print anything because the default logging severity
# level has been restored. Error log messages will always print.

logger = logging.getLogger('my_log')
logger.debug('Debug will not print')
logger.error('Error will print')
#


# Things to remember

# 1. The with statement allows you to reuse logic from try/finally blocks and
#    reduce visual noise.
# 2. The contextlib built-in module provides a contextmanager decorator that
#    makes it easy to use your own functions in with statements.
# 3. The value yielded by context managers is supplied to the as part of the
#    with statement. It's useful for letting your code directly access the
#    cause of the special context.
