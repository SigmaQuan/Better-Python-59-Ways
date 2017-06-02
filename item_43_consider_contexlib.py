# Item 43: Consider contextlib and with statements for reusable try/finally
# behavior
from threading import Lock


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
# to

# Things to remember

# 1.
# 2.
# 3.
