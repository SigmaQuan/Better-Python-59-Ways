# Item 28: Inherit from collections.abc for custom container types


# Much of programming in Python is defining classes that contain data and
# describing how such objects relate to each other. Every Python class is a
# container of some kind, encapsulating attributes and functionality together.
# Python also provides built-in container types for managing data: lists,
# tuples, sets, and dictionaries.

# When you'r designing classes for simple use cases like sequence, it's
# natural that you'd want to subclass Python built-in list type directly.
# For example, say you want to create your own custom list type that has
# additional methods for counting the frequency of its members.


class FrequencyList(list):
    def __init__(self, members):
        super().__init__(members)

    def frequency(self):
        counts = {}
        for item in self:
            counts.setdefault(item, 0)
            counts[item] += 1
        return counts


# By subclassing list, you get all of list's standard functionality and
# preserve the semantics familiar to all Python programmers. Your additional
# methods can add any custom behaviors you need.


foo = FrequencyList(['a', 'b', 'a', 'c', 'b', 'a', 'd'])
print('Length is', len(foo))
foo.pop()
print('After pop:', repr(foo))
print('Frequency:', foo.frequency())
# Length is 7
# After pop: ['a', 'b', 'a', 'c', 'b', 'a']
# Frequency: {'a': 3, 'b': 2, 'c': 1}


# Now imagine you want to provide an object that feels like a list, allowing
# indexing, but isn't a list subclass. For example, say you want to provide
# sequence semantic (like list or tuple) for a binary tree class.


class BianryNode(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


# How do you make this act like a sequence type? Python implements its
# container behaviors with instance methods that have special names. When you
# access a sequence item by index.

bar = [1, 2, 3]
print(bar[0])
# 1


# it will be interpreted as:


print(bar.__getitem__(0))
# 1


# To make the BinaryNode class act like a sequence, you can provide a custom
# implementation of __getitem__ that traverses the object tree depth first.



# Things to remember

# 1. Inherit directly from Python's container types (like list or dict) for
#    simple use cases.
# 2. Beware of the large number of methods required to implement custom
#    container types correctly.
# 3. Have your custom container types inherit from the interface defined in
#    collections.abc to ensure that your classes match required interfaces
#    and behaviors.
