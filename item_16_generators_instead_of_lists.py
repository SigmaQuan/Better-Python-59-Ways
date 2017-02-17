# Item 16: Consider generators instead of returning lists
import itertools


# The simple choice for functions that produce a sequence of results is to
# return a list of items For example, say you want to find the index of every
# word in string. Here, I accumulate results in a list using the append method
# and return it at the end of the function:


def index_words(text):
    result = []
    if next:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == ' ':
            result.append(index + 1)
    return result


# This words as expected for some sample input.


address = 'Four score and seven years ago...'
result = index_words(address)
print(result[:3])
# [0, 5, 11]


# There are two problems with index_words function.

# The first problem is that the code is a bit dense and noisy. Each time a
# new result is found, I call the append method. The method call's bulk (
# result.append) deemphasizes the value being added to the list (index + 1).
# There is one line for creating the result list and another for returning it.
# While the function body contains ~130 characters (without whitespace), only
# ~75 characters are important.

# A better way to write this function is using a generator. Generators are
# functions that use yield expressions. When called, generator functions do
# not actually run but instead immediately return an iterator. With each call
# to the next built-in function, the iterator will advance the generator to
# its next yield expression. Each value passed to yield by the generator will
# be returned by the iterator to the caller.

# Here, I define a generator function that produces the same results as
# before:


def index_words_iter(text):
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1


# It's significantly easier to read because all interactions with the result
# list have been eliminated. Results are passed to yield expressions instead.
# The iterator returned by the generator call can easily be converted to a
# list by passing it to the list built-in function (see Item 9: "Consider
# generator expressions for large comprehensions" for how this works).


result = list(index_words(address))
print(result)
# [0, 5, 11, 15, 21, 27]


# The second problem with index_words is that it requires all results to be
# stored in the list before being returned. For huge inputs, this can cause
# your program to return out of memory and crash. In contrast, a generator
# version of this function can easily be adapted to take inputs of arbitrary
# length.

# Here, I define a generator that streams input from a file one line at a time
# and yields outputs one word at a time. The working memory for this function
# is bounded to the maximum length of one line of input.


def index_file(handle):
    offset = 0
    for line in handle:
        if line:
            yield offset
        for letter in line:
            offset += 1
            if letter == ' ':
                yield offset


# Running the generator produces the same results.


with open('item_16_address.txt', 'r') as f:
    it = index_file(f)
    results = itertools.islice(it, 0, 3)
    print(list(results))
# [0, 5, 11]


# The only gotcha of defining generators like this is that the callers must be
# aware that the iterators returned are stateful and can't be reused (see
# Item 17: "Be defensive when iterating over arguments").


# Things to remember

# 1. Using generators can be clearer than the alternative of returning lists
#    of accumulated results.
# 2. The iterator returned by a generator produces the set of values passed to
#    yield expressions within the generator function's body.
# 3. Generators can produce a sequence of outputs for arbitrarily large inputs
#    because their working memory doesn't include all inputs and outputs.
