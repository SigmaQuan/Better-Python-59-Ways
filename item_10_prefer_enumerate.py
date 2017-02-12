# Item 10: Prefer enumerate over range
import random


# The range built-in function is useful for loops that iterate over a set of
# integers.

random_bits = 0
for i in range(64):
    if random.randint(0, 1):
        random_bits |= 1 << i


# When you have a data structure to iterate over, like a list of strings, you
# can loop directly over the sequence.


flavor_list = ['vanilla', 'chocolate', 'pecan', 'strawberry']
for flavor in flavor_list:
    print('%s is delicious' % flavor)
# vanilla is delicious
# chocolate is delicious
# pecan is delicious
# strawberry is delicious


# Often, you'll want to iterate over a list and also know the index of the
# current item in the list. For example, say you want to print the ranking of
# your favorite ice cream flavors. One way to do it is using range.


for i in range(len(flavor_list)):
    flavor = flavor_list[i]
    print('%d: %s' % (i+1, flavor))
# 1: vanilla
# 2: chocolate
# 3: pecan
# 4: strawberry


# This looks clumsy compared with the other examples of iterating over
# flavor_list or range. You have to get the length of the list. You have to
# index into the array. It's harder to read.

# Python provides the enumerate built-in function for addressing this
# situation. enumerate wraps any iterator with a lazy generator. This
# generator yields pairs of the loop index and the next value from the
# iterator. The resulting code is much clearer.


for i, flavor in enumerate(flavor_list):
    print('%d: %s' % (i + 1, flavor))
# 1: vanilla
# 2: chocolate
# 3: pecan
# 4: strawberry


# You can make this even shorter by specifying the number from which enumerate
# should begin counting (1 in this case).


for i, flavor in enumerate(flavor_list, 1):
    print('%d: %s' % (i, flavor))
# 1: vanilla
# 2: chocolate
# 3: pecan
# 4: strawberry


# Things to remember

# 1. enumerate provides concise syntax for looping over an iterator and
#     getting the index of each item from the iterator as you go.
# 2. Prefer enumerate instead of looping over a range and indexing into a
#     sequence.
# 3. You can supply a second parameter to enumerate to specify the number from
#     which to begin counting (zero is default).
