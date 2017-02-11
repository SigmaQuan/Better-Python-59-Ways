# Item 8: Avoid more than two expressions in list comprehensions


# Beyond basic usage (see Item 7: Use list comprehensions instead of map and
# filter), list comprehensions also support multiple levels of looping. For
# example, say you want to simplify a matrix (a list containing other lists)
# into one flat list of all cells. Here, I do this with a list comprehension
# by including two for expressions. These expressions run in the order
# provided from left to right.


matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [x for row in matrix for x in row]
print(flat)
# [1, 2, 3, 4, 5, 6, 7, 8, 9]


# The example above is simple, readable, and a reasonable usage of multiple
# loops. Another reasonable usage of multiple loops is replicating the
# two-level deep layout of the input list. For example, say you want to square
# the value in each cell of a two-dimensional matrix. This expression is
# noisier because of the extra [] characters, but it's still easy to read.


squared = [[x**2 for x in row] for row in matrix]
print(squared)
# [[1, 4, 9], [16, 25, 36], [49, 64, 81]]


# If this expression included another loop, the list comprehension would get
# so long that you'd have to split it over multiple lines.

my_lists = [
    [[1, 2, 3], [4, 5, 6]],
    # ...
    [[11, 22, 33], [44, 55, 66]]
]
flat = [x for sublist1 in my_lists
        for sublist2 in sublist1
        for x in sublist2]
print(flat)
# [1, 2, 3, 4, 5, 6, 11, 22, 33, 44, 55, 66]


# At this point, the multiline comprehension isn't much shorter thant the
# alternative. Here, I produce the same using normal loop statements. The
# indentation of this version makes the looping clearer than the list
# comprehension.


flat = []
for sublist1 in my_lists:
    for sublist2 in sublist1:
        flat.extend(sublist2)
print(flat)
# [1, 2, 3, 4, 5, 6, 11, 22, 33, 44, 55, 66]


# List comprehensions also support multiple if conditions. Multiple
# conditions at the same loop level are an implicit and expression. For
# example, say you want to filter a list of numbers to only even values
# greater than four. These only list comprehensions are equivalent.


a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
b = [x for x in a if x > 4 if x % 2 == 0]
c = [x for x in a if x > 4 and x % 2 == 0]
print(b)
print(c)
# [6, 8, 10]
# [6, 8, 10]


# Conditions can be specified at each level of looping after the for
# expression. For example, say you want to filter a matrix so the only cells
# remaining are those divisible by 3 in rows that sum to 10 or higher.
# Expressing this with list comprehensions is short, but extremely difficult
# to read.


matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
filtered = [[x for x in row if x % 3 == 0]
            for row in matrix if sum(row) >= 10]
print(filtered)
# [[6], [9]]


# Though this example is a bit convoluted, in practice you'll see situations
# arise where such expressions seem like a good fit. I strongly encourage you
# to avoid using list comprehensions that look like this. The resulting code
# is very difficult for others to comprehend. What you save in the number of
# lines doesn't outweigh the difficulties it could cause later.

# The rule of thumb is to avoid using more than two expressions in a list
# comprehension. This could be two conditions, two loops, or one condition
# and one loop. As soon as it gets more complicated than that, you should
# use normal if and for statements and write a helper function (see Item 16:
# Consider generators instead of returning lists).


# Things to remember

# 1. List comprehensions support multiple levels of loops and multiple
#     conditions per loop level.
# 2. List comprehensions with more than two expressions are very difficult to
#     read and should be avoided.
