# Item 3: Know the difference between bytes, str, and unicode
import os

# In Python 3, there are two types that represent sequences of characters:
# bytes and str. Instances of bytes contain raw 8-bit values. Instances of
# str contain Unicode characters.

# In Python 2, there two types that represent sequences of characters: str and
# unicode. In contrast to Python 3, instances of str contain raw 8-bit values.
# Instances of unicode contain Unicode characters.

# There are many ways to represent Unicode characters as binary data (raw
# 8-bits values). The most common encoding in UTF-8. Importantly, str
# instances in Python 3 and unicode instances in Python 2 do not have an
# associated binary encoding. To convert Unicode characters to binary data,
# you must use the encode method. To convert binary data to Unicode
# characters, you must use the decode method.

# When you're writing Python programs, it's important to do encoding and
# decoding of Unicode at the furthest boundary of your interfaces. The core of
# your program should use Unicode character types (str in Python 3, unicode in
# Python 2) and should not assume any thing about character encodings. This
# approach allows you to be very accepting of alternative text encodings
# (such as Latin-1, Shift  JIS, and Big5) while being strict about your output
# text encoding (idealy, UTF-8).

# The split between character types leads to two common situations in Python
# code:
# 1. You want to operate on raw 8-bit values that are UTF-8-encoded characters
#     (or some other encoding).
# 2. You want to operate on Unicode characters that have no specific encoding.

# You'll often need two helper functions to convert between these two cases
# and and to ensure that the type of input values matches your code's
# expectations.

# In Python 3, you'll need one method that takes a str or bytes and always
# returns a str.


def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value  # Instance of str


# You'll need another method that takes a str and bytes and always returns a
# bytes.


def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value  # Instance of str


# In Python 2, you'll need one method that takes a str or unicode and always
# returns a unicode.


def to_unicode(unicode_or_str):
    if isinstance(unicode_or_str, str):
        value = unicode_or_str.decode('utf-8')
    else:
        value = unicode_or_str
    return value  # Instance of unicode


# You'll need another method that takes str or unicode and always returns a str.


def to_str(unicode_or_str):
    if isinstance(unicode_or_str):
        value = unicode_or_str.encode('utf-8')
    else:
        value = unicode_or_str
    return value  # Instance of str


# There are two big gotchas when dealing with raw 8-bit values and Unicode
# characters in Python.

# The first issue is that in Python 2, unicode and str instances seem to be
# the same type when a str only contains 7-bit ASCII characters.
# 1. You can combine such a str and unicode together using the + operator.
# 2. You can compare such str and unicode instances using equality and
#     inequality operators.

# All of this behavior means that you can often pass a str or unicode instance
# to a function expecting one or the other and things will just work (as long
# as you're only dealing with 7-bit ASCII). In Python 3, bytes and str
# instances are never equivalent-not even the empty string-so you must be more
# deliberate about the types of character sequences that you're passing around.

# The second issue is that in Python 3, operations involving file handles
# (returned by the open built-in function) default to UTF-8 encoding. In
# Python 2, file operations default to binary encoding. This causes surprising
# failures, especially for programmers accustomed to Python 2.

# For example, say you want to write some random binary data to a file. In
# Python 2, this works. In Python 3, this breaks.


with open('random.bin', 'w') as f:
    f.write("random")
    # f.write(os.urandom(10))

# TypeError: write() argument must be str, not bytes


# The cause of this exception is the new encoding argument for open that was
# added in Python 3. This parameter defaults to 'utf-8'. That makes read and
# write operations on file handles expect str instances containing Unicode
# characters instead of bytes instances containing binary data.

# To make this work properly, you must indicate that the data is being
# opened in write binary mode ('wb') instead of write character mode ('w').
# Here, I use open in a way that works correctly in Python 2 and Python 3:


with open('random.bin', 'wb') as f:
    f.write(os.urandom(10))


# This problem also exists for reading data from files. The solution is the
# same: Indicate binary mode by using 'rb' instead of 'r' when opening a file.


# Things to Remember

# 1. In Python 3, bytes contains sequences of 8-bit values, str contains
#     sequences of Unicode characters. bytes and str instances can't be
#     used together with operators (like > or +).
# 2. In Python 2, str contains sequences of 8-bit values, unicode contains
#     sequences of Unicode characters. str and unicode can be used together
#     with operators if the str only contains 7-bit ASCII characters.
# 3. Use helper functions to ensure that the inputs you operate on are the
#     type of character sequence you expect (8-bit values, UTF-8 encoded
#     characters, Unicode characters, etc.)
# 4. If you want to read or write binary data to/from a file, always open the
#     file using a binary mode (like 'rb' or 'wb').
