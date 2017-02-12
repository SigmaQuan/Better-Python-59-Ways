# Item 11: Use zip to process iterators in parallel


# Often in Python you find yourself with many lists of related objects. List
# comprehensions make it easy to take a source list and get a derived list by
# applying an expression (see Item 7: Use list comprehensions instead of map
# and filter).


names = ['Cecilia', 'Lise', 'Marie']
letters = [len(n) for n in names]


# The items in the derived list are related to the items in the source list by
# their indexes. To iterate over both lists in parallel, you can iterate over
# the length of the names source list.


longest_name = None
max_letters = 0

for i in range(len(names)):
    count = letters[i]
    if count > max_letters:
        longest_name = names[i]
        max_letters = count

print(longest_name)
# Cecilia


# The problem is that this whole loop statement is visually noisy. The indexes
# into names and letters make the code hard to read. Indexing into the arrays
# by the loop index i happens twice. Using enumerate (see Item 10: Prefer
# enumerate over range) improves this slightly, but it's still not ideal.


for i, name in enumerate(names):
    count = letters[i]
    if count > max_letters:
        longest_name = name
        max_letters = count


# To make this code clearer, Python provides the zip built-in function. In
# Python 3, zip wraps two or more iterators with a lazy generator. The zip
# generator yields tuples containing the next value from each iterator. The
# resulting code is much cleaner that indexing into multiple lists.


for name, count in zip(names, letters):
    if count > max_letters:
        longest_name = name
        max_letters = count


# There are two problems with the zip built-in.

# The first issue is that in Python 2 zip is not a generator; it will fully
# exhaust the supplied iterators and return a list of all the tuples it
# creates. This could potentially use a lot of memory and cause your program
# to crash. If you want to zip very large iterators in Python 2, you should
# use izip from the itertools built-in module (see Item 46: Use built-in
# algorithms and data structures).

# The second issue is that zip behaves strangely if the input iterators are of
# different lengths. For example, say you add other name to the list above but
# forget to update the letter counts. Running zip on the two input lists will
# have an unexpected result.


names.append('Rosalind')
for name, count in zip(names, letters):
    print(name)
# Cecilia
# Lise
# Marie


# The new item for 'Rosalind' isn't there. This is just now zip works. It
# keeps yielding tuples until a wrapped iterator is exhausted. This approach
# works fine when you know that the iterators are of the same length, which is
# often the case for derived lists created by list comprehensions. In many
# other cases, the truncating behavior of zip is surprising and bad. If you
# aren't confident that the lengths of the list you want to zip are equal,
# consider using the zip_longest function from itertools built-in module
# instead (also called izip_longest in Python 2).


# Things to remember

# 1. The zip built-in function can be used to iterate over multiple iterators
#     in parallel.
# 2. In Python 3, zip is a lazy generator that produces tuples. In Python 2,
#     zip returns the full result as a list of tuples.
# 3. zip truncates its outputs silently if you supply it with iterators of
#     different lengths.
# 4. The zip_longest function from the itertools built-in module lets you
#     iterate over multiple iterators in parallel regardless of their
#     lengths (see Item 46: Use built-in algorithms and data structures).
