# Item 6: Avoid using start, end and stride in a single slice


# In addition to basic slicing (see Item 5: Knowing how to slice sequences),
# Python has special syntax for the stride of a slice in the form
# somelist[start:end:stride]. This lets you take every n-th item when slicing
# a sequence. For example, the stride makes it easy to group by even and odd
# indexes in a list.


a = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
odds = a[::2]
evens = a[1::2]
print(odds)
print(evens)
# ['red', 'yellow', 'blue']
# ['orange', 'green', 'purple']


# The problem is that the stride syntax ofter cause unexpected behavior that
# can introduce bugs. For example, a common Python trick for reversing a byte
# string is to slice the string with a stride of -1.


x = b'mongoose'
y = x[::-1]
print(y)
# b'esoognom'


# That works well for byte strings and ASCII characters, but it will break for
# Unicode characters encoded as UTF-8 byte strings.


w = '谢谢谢谢'
# x = w.enocde('utf-8')
# y = x[::-1]
# z = y.decode('utf-8')
# print(y)
# print(z)
# AttributeError: 'str' object has no attribute 'enocde'


# Are negative strides besides -1 useful? Consider the following examples.


a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
print(a[::2])
print(a[::-2])
# ['a', 'c', 'e', 'g']
# ['h', 'f', 'd', 'b']


# Here, ::2 means select every second item starting at the beginning.
# Trickier, ::-2 means select every second item starting at the end and moving
# backwards.


# What do you think 2::2 means? What about -2::-2 vs. -2:2:-2 vs. 2:2:-2?
print(a[2::2])
print(a[-2::-2])
print(a[-2:2:-2])
print(a[2:2:-2])
# ['c', 'e', 'g']
# ['g', 'e', 'c', 'a']
# ['g', 'e']
# []


# The point is that the stride part of the slicing syntax can be extremely
# confusing. Having three numbers within the brackets is hard enough to read
# because of its density. Then it's not obvious when the start and end indexes
# come into effect relative to the stride value, especially when stride is
# negative.


# To prevent problems, avoid using stride along with start and end indexes. If
# you must use a stride, prefer making it a positive value and omit start and
# end indexes. If you must use stride with start and end indexes, consider
# using one assignment to stride and another to slice.


b = a[::2]
c = b[1:-1]
print(b)
print(c)
# ['a', 'c', 'e', 'g']
# ['c', 'e']


# Slicing and then striding will create an extra shallow copy of the data.
# The first operation should try to reduce the size of the resulting slice by
# as much as possible. If your program can't afford the time or memory
# required for two steps, consider using the itertools built-in module's
# islice method (see Item 46: Use built-in algorithms and data structures),
# which doesn't permit negative values for start, end or stride.


# Things to remember

# 1. Specifying start, end, and stride in a slice can be extremely confusing.
# 2. Prefer using positive stride values in slices without start or end
#     indexes. Avoid negative stride values if possible.
# 3. Avoid using start, end and stride together in a single slice. If you need
#     all three parameters, consider doing two assignments (one to slice,
#     another to stride) or using islice form itertools built-in module.
