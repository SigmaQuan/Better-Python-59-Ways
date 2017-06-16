# Item 55: Use repr strings for debugging output


# When debugging a Python program, the print function (or output via the
# logging built-in module) will get you surprisingly far. Python internals are
# often easy to access via plain attributes (see Item 27: "Prefer public
# attributes over private ones"). All you need to do is print how the state of
# your program changes while it runs and see where it goes wrong.

# The print function outputs a human-readable string version of whatever you
# supply it. For example, printing a basic string will print the contents of
# the string without the surrounding quote characters.

# The problem is that the human-readable string for a value doesn't make it
# clear what the actual type of the value is. For example, notice how in the
# default output of print you can't distinguish between the types of the
# number 5 and the string '5'.

print(5)
print('5')
# 5
# 5

# If you're debugging a program with print, these type differences matter.
# What you almost always want while debugging is to see the repr version of an
# object. The repr built-in function returns the printable representation of
# an object, which should be its most clearly understandable string
# representation. For built-in types, the string returned by repr is a valid
# Python expression.

a = '\x07'
print(repr(a))
# '\x07'

# Passing the value from repr to the eval built-in function should result in
# the same Python object you started with (of course, in practice, you should
# only use eval with extreme caution).

b = eval(repr(a))
assert a == b

# When you're debugging with print, you should repr the value before printing
# to ensure that any difference in types is clear.

print(repr(5))
print(repr('5'))
# 5
# '5'

# For dynamic Python objects, the default human-readable string value is the
# same as the repr value. This means that passing a dynamic object to print
# will do the right thing, and you don't need to explicitly call repr on it.
# Unfortunately, the default value of repr for object instances isn't
# especially helpful. For example, here I define a simple class and then print
# its value:


class OpaqueClass(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


obj = OpaqueClass(1, 2)
print(obj)
print(repr(obj))
# <__main__.OpaqueClass object at 0x7f454b200828>
# <__main__.OpaqueClass object at 0x7f454b200828>

# This output can't be passed to the eval function, and it says nothing about
# the instance fields of the object.

# There are two solutions to this problem. If you have control of the class,
# you can define your own __repr__ special method that returns a string
# containing the Python expression that recreates the object. Here, I define
# that function for the class above:


class BetterClass(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'BetterClass(%d, %d)' % (self.x, self.y)


# Now, the repr value is much more useful.

obj = BetterClass(1, 2)
print(obj)
print(repr(obj))
# BetterClass(1, 2)
# BetterClass(1, 2)

# When you don't have control over the class definition, you can reach into
# the object's instance dictionary, which is stored in the __dict__
# attribute. Here, I print out the contents of an OpaqueClass instance:

obj = OpaqueClass(4, 5)
print(obj.__dict__)
# {'y': 5, 'x': 4}


# Things to remember

# 1. Calling print on built-in Python types will produce the human-readable
#    string version of a value, which hides type information.
# 2. Calling repr on built-in Python types will produce the printable string
#    version of a value. These repr strings could be passed to the eval
#    built-in function to get back the original value.
# 3. %s in format strings will produce human-readable strings like str.%r will
#    produce printable strings like repr.
# 4. You can define the __repr__ method to customize the printable
#    representation of a class and provide more detailed debugging
#    information.
# 5. You can reach into any object's __dict__ attribute to view its internals.
