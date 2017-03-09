# Item 25: Initialize parent classes with super
from pprint import pprint


# The old way to initialize a parent class from a child class is to directly
# call the parent class's __init__ method with the child instance.


class MyBaseClass(object):
    def __init__(self, value):
        self.value = value


class MyChildClass(MyBaseClass):
    def __init__(self):
        MyBaseClass.__init__(self, 5)


# This approach works fine for simple hierarchies but breaks down in many
# cases.

# If your class is affected by multiple inheritance (something to avoid in
# general; see Item 26: "Use multiple inheritance only for mix-in utility
# classes"), calling the superclass' __init__ methods directly can lead to
# unpredictable behavior. One problem is that the __init__ call order isn't
# specified across all subclass. For example, here I define two parent classes
# that operate on the instance's value field:


class TimesTwo(object):
    def __init__(self):
        self.value *= 2


class PlusFive(object):
    def __init__(self):
        self.value += 5


# This class defines its parent classes in one ordering.


class OneWay(MyBaseClass, TimesTwo, PlusFive):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)


# And constructing it produces a result that matches the parent class ordering.


foo = OneWay(5)
print("First ordering is (5*2)+5=", foo.value)
# First ordering is (5*2)+5= 15


# Here's another class that defines the same parent classes but in a different
# ordering:


class AnotherWay(MyBaseClass, PlusFive, TimesTwo):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)


# However, I left the calls to the parent class constructors PlusFive.__init__
# and TimesTwo.__init__ in the same order as before, causing this class's
# behavior not to match the order of the parent classes in its definition.


bar = AnotherWay(5)
print("Second ordering still is ", bar.value)
# Second ordering still is  15


# Another problem occurs with diamond inheritance. Diamond inheritance happens
# when a subclass inherits from two separate classes that have the same
# superclass superclass somewhere in the hierarchy. Diamond inheritance causes
# the common superclass's __init__ method to run multiple times, causing
# unexpected behavior. For example, here I define two child classes that
# inherit from MyBaseClass.


class TimesFive(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value *= 5


class PlusTwo(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value += 2


# Then, I define a child class that inherit from both of these classes, making
# MyBaseClass the top of the diamond.


class ThisWay(TimesFive, PlusTwo):
    def __init__(self, value):
        TimesFive.__init__(self, value)
        PlusTwo.__init__(self, value)


foo = ThisWay(5)
print("Should be (5*5)+2 = 27 but is ", foo.value)
# Should be (5*5)+2 = 27 but is  7


# The output should be 27 because (5*5)+2 = 27. But the call to the second
# parent class's constructor, PlusTwo.__init__, causes self.value to be reset
# back to 5 when MyBaseClass.__init__ gets a second time.

# To solve these problems, Python 2.2 added the super built-in function and
# defined the method resolution order (MRO). The MRO standardizes which
# superclasses are initialized before others (e.g. depth-first,
# left-to-right). It also ensures that common superclass in diamond
# hierarchies are only run once.

# Here, I create a diamond-shaped class hierarchy again, but this time I use
# super (in Python 2 style) to initialize the parent class:


# Python 2
class TimesFiveCorrect(MyBaseClass):
    def __init__(self, value):
        super(TimesFiveCorrect, self).__init__(value)
        self.value *= 5


class PlusTwoCorrect(MyBaseClass):
    def __init__(self, value):
        super(PlusTwoCorrect, self).__init__(value)
        self.value += 2


# Now the top part of the diamond, MyBaseClas.__init__, is only run a single
# time. The other parent classes are run in the order specified in the class
# statement.


# Python 2
class GoodWay(TimesFiveCorrect, PlusTwoCorrect):
    def __init__(self, value):
        super(GoodWay, self).__init__(value)


foo = GoodWay(5)
print("Should be 5*(5+2) = 35 and is ", foo.value)
# Should be 5*(5+2) = 35 and is  35


# This order may seem backwards at first. Shouldn't TimesFiveCorrect.__init__
# have run first? Shouldn't the result be (5*5)+2 = 27? The answer is no.
# This ordering matches what the MRO defines for this class. The MRO ordering
# available on a class method called mro.


pprint(GoodWay.mro())
# [<class '__main__.GoodWay'>,
#  <class '__main__.TimesFiveCorrect'>,
#  <class '__main__.PlusTwoCorrect'>,
#  <class '__main__.MyBaseClass'>,
#  <class 'object'>]


# When I call Goodway(5), it in turn calls TimesFiveCorrect.__init__, which
# calls PlusTwoCorrect.__init__, which calls MyBaseClass.__init__. Once this
# reaches the top of the diamond, then all of the initialization method
# actually do their work in the opposite order from how their __init__
# functions were called. MyBaseClass.__init__ assigns the value to 5.
# PlusTwoCorrect.__init__ adds 2 to make value equal 7.
# TimesFiveCorrect.__init__ multiple it by 5 to make value equal 35.

# The super built-in function works well, but it still has two noticeable
# problems in Python 2:

# - Its syntax is a bit verbose. You have to specify the class you're in,
#   the self object, the method name (usually __init__), and all the
#   arguments. This construction can be confusing to new Python programmers.

# - You have to specify the current class by name in the call to super. If you
#   ever change the class's name--a very common activity when improving a
#   class hierarchy--you also need to update every call to super.

# Thankfully, Python 3 fixes these issues by making calls to super with no
# arguments equivalent to calling super with __class__ and self specified. In
# Python 3, you should always use super because it's clear, concise, and
# always does the right things.


class Explicit(MyBaseClass):
    def __init__(self, value):
        super(__class__, self).__init__(value * 2)


class Implicit(MyBaseClass):
    def __init__(self, value):
        super().__init__(value * 2)


assert Explicit(10).value == Implicit(10).value


# This works because Python 3 lets you reliably reference the current class
# in methods using the __class__ variable. This doesn't work in Python 2
# because __class__ isn't defined. You may guess that you could use
# self.__class__ as an argument to super, but this breaks because of the way
# super is implemented in Python 2.


# Things to remember

# 1. Python's standard method resolution order (MRO) solves the problems to
#    superclass initialization order and diamond inheritance.
# 2. Always use the super built-in function to initialize parent classes.
