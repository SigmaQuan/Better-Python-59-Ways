# Item 28: Inherit from collections.abc for custom container types
# ToDo: need to debug.


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


class BinaryNode(object):
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


class IndexableNode(BinaryNode):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def _search(self, count, index):
        found = False
        return (found, count)
        # ...
        # returns (found, count)

    def __getitem__(self, index):
        found, _ = self._search(0, index)
        if not found:
            raise IndexError("Index out of range")
        return found.value


# You can construct your binary tree as usual.


tree = IndexableNode(
    10,
    left=IndexableNode(
        5,
        left=IndexableNode(2),
        right=IndexableNode(
            6,
            right=IndexableNode(7)
        )
    ),
    right=IndexableNode(
        15, left=IndexableNode(11)
    )
)


# But you can also access it like a list in addition to tree traversal.


print('LRR', tree.left.right.right.value)
# print('Index 0 = ', tree[0])
# print('Index 1 = ', tree[1])
# print('11 in the tree?', 11 in tree)
# print('17 in the tree?', 17 in tree)
# print('Tree is ', list(tree))


# The problem is that implementing __getitem__ isn't enough to provide all of
# the sequence semantics you'd expect.


# len(tree)
# TypeError: object of type 'IndexableNode' has no len()


# The len built-in function requires another special method named __len__ that
# must have an implementation for your custom sequence type.


class SequenceNode(IndexableNode):
    def __len__(self):
        _, count = self._search(0, None)
        return count

tree = IndexableNode(
    10,
    left=IndexableNode(
        5,
        left=IndexableNode(2),
        right=IndexableNode(
            6,
            right=IndexableNode(7)
        )
    ),
    right=IndexableNode(
        15, left=IndexableNode(11)
    )
)

print('Tree has %d nodes' % len(tree))


# Unfortunately, this still isn't enought. Also missing are the count and
# index methods that a Python programmer would expect to see on a sequence
# like list or tuple. Defining your own container types is much harder than
# it looks.

# To avoid this difficulty throughout the Python universe, the built-in
# collections.abc mudule defines a set of abstract base classes that provide
# all of the typical methods for each container type. When you subclass from
# these abstract base classes and forget to implement required methods, the
# module will tell you something is wrong.


# from collections.abc import Sequence
from collections import Sequence


class BadType(Sequence):
    pass

foo = BadType()
# TypeError: Can't instantiate abstract class BadType with abstract methods __getitem__, __len__


# When you do implement all of the methods required by an abstract base class,
# as I did above with SequenceNode, it will provide all of the additional
# methods like index and count for free.


class BetterNode(SequenceNode, Sequence):
    pass

tree = IndexableNode(
    10,
    left=IndexableNode(
        5,
        left=IndexableNode(2),
        right=IndexableNode(
            6,
            right=IndexableNode(7)
        )
    ),
    right=IndexableNode(
        15, left=IndexableNode(11)
    )
)

print('Index of 7 is', tree.index(7))
print('Count of 10 is', tree.count(10))


# The benefit of using these abstract base class is even greater for more
# complex types like Set and MutableMapping, which have a large number of
# special methods that need to be implemented to match Python conventions.


# Things to remember

# 1. Inherit directly from Python's container types (like list or dict) for
#    simple use cases.
# 2. Beware of the large number of methods required to implement custom
#    container types correctly.
# 3. Have your custom container types inherit from the interface defined in
#    collections.abc to ensure that your classes match required interfaces
#    and behaviors.
