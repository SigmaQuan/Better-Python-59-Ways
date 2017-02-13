# Item 13: Take advantage of each block in try/except/else/finally
import json


# There are four distinct times that you may want to take action during
# exception handling in Python. These are captured in the functionality of
# try, except, else, and finally blocks. Each block serves a unique purpose in
# the compound statement, and their various combinations are useful (see Item
# 51).


# Finally Blocks

# Use try/finally when you want exceptions to propagate up, but you also want
# to run cleanup code when exceptions occur. One common usage to try/finally
# is reliably closing file handles (see Item 43: "Consider contextlib and with
# statements for reusable try/finally behavior" for another approach).


handle = open('item_13_try_except_else_finally.py')  # May raise IOError
# handle = open('item_13_try_except_else_finally_.py')  # May raise IOError
# FileNotFoundError: [Errno 2] No such file or directory:
#     'item_13_try_except_else_finally_.py'
try:
    data = handle.read()   # May raise UnicodeDecodeError
finally:
    handle.close()  # Always runs after try:


# Any exception raised by the read method will always propagate up to the
# calling code, yet the close method of handle is also guaranteed to run in
# the finally block.


# Else Blocks

# Use try/except/else to make it clear with exceptions will be handled try
# your code and which exceptions will propagate up. When the try block doesn't
# raise an exception, the else block will run. The else block helps you
# minimize the amount of code in the try block and improves readability. For
# example, say you want to load JSON dictionary data from a string and return
# the value of a key it contains.


def load_json_key(data, key):
    try:
        result_dict = json.loads(data)  # May raise ValueError
    except ValueError as e:
        raise KeyError from e
    else:
        return result_dict[key]   # May raise KeyError


# If the data isn't valid JSON, then decoding with json.load will raise a
# ValueError. The exception is caught by the except block and handled. If
# decoding is successful, then the key lookup will occur in the else block. if
# the key lookup raises any exceptions, they will propagate up to the caller
# because they are outside the try block. The else clause ensures that what
# follows the try/except is visually distinguished from the except block. This
# makes the exception propagation behavior clear.


# Everything together

# Use try/except/else/finally when you want to do it all in one compound
# statement. For example, say you want to read a description of work to do
# from a file, process it, and then update the file in place. Here, the try
# block is used to read the file and process it. The except block is used to
# handle exceptions from the try block that are expected. The else block is
# used to update the file in place and to allow realted exceptions to
# propagated up. The finally block cleans up the file handle.


UNDEFINED = object()


def divide_json(path):
    handle = open(path, 'r+')  # May raise IOError
    try:
        data = handle.read()   # May raise UnicodeDecodeError
        op = json.loads(data)  # May raise ValueError
        value = (              # May raise ZeroDivisionError
            op['numerator']/op['denominator'])
    except ZeroDivisionError as e:
        return UNDEFINED
    else:
        op['result'] = value
        result = json.dumps(op)
        handle.seek(0)
        handle.write(result)   # May raise IOError
        return value
    finally:
        handle.close()         # Always runs


# This layout is especially useful because all of the blocks work together in
# intuitive ways. For example, if an exception gets raised in the else block
# while rewriting the result data, the finally block will still run and close
# the file handle.


# Things to remember

# 1. The try/finally compound statement lets you run cleanup code regardless
#     of whether exceptions were raised in the try block.
# 2. The else block helps you minimize the amount of code in try blocks and
#     visually distinguish the success case from the try/except blocks.
# 3. An else block can be used to perform additional actions after a
#     successful try block but before common cleanup in a finally block.
