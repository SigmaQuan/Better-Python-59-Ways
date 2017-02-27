# Effective Python: 59 Specific Ways to Write Better Python
Code Sample of Book "Effective Python: 59 Specific Ways to Write Better Python" by Brett Slatkin.

## Chapter 1: Pythonic thinking


### [Item 1: Know which version of python you're using](item_01_version_of_python.py)
- 1. There are two major version of Python still in active use: Python 2 and
Python 3.
- 2. There are multiple popular runtimes for Python: CPython, Jython,
     IronPython, PyPy, etc.
- 3. Be sure that the command-line for running Python on your system is the
     version you expect it to be.
- 4. Prefer Python 3 for your next project because that is the primary focus
     of the Python community.
    
     
### [Item 2: Follow the PEP 8 style guide](item_02_PEP8Style.py)
- 1. Always follow the PEP 8 style guide when writing Python code.
- 2. Sharing a common style with the larger Python community facilitates
     collaboration with others.
- 3. Using a consistent style makes it easier to modify your own code later.


### [Item 3: Know the difference between bytes, str, and unicode](item_03_Difference_bytes_str_unicode.py)
- 1. In Python 3, bytes contains sequences of 8-bit values, str contains
     sequences of Unicode characters. bytes and str instances can't be
     used together with operators (like > or +).
- 2. In Python 2, str contains sequences of 8-bit values, unicode contains
     sequences of Unicode characters. str and unicode can be used together
     with operators if the str only contains 7-bit ASCII characters.
- 3. Use helper functions to ensure that the inputs you operate on are the
     type of character sequence you expect (8-bit values, UTF-8 encoded
     characters, Unicode characters, etc.)
- 4. If you want to read or write binary data to/from a file, always open the
     file using a binary mode (like 'rb' or 'wb').


### [Item 4: Write helper functions instead of complex expressions](item_04_helper_function.py)
- 1. Python's syntax makes it all too easy to write single-line expressions
     that are overly complicated and difficult to read.
- 2. Move complex expressions into helper functions, especially if you need to
     use the same logic repeatedly.
- 3. The if/else expression provides a more readable alternative to using
     Boolean operators like or and adn in expressions.


### [Item 5: Know hot to slice sequences](item_05_slice_sequence.py)
- 1. Avoid being verbose: Don't supply 0 for the start index or the length of
     the sequence for the end index.
- 2. Slicing is forgiving of start or end indexes that are out of bounds,
     making it easy to express slices on the front or back boundaries of a
     sequence (like a[:20] or a[-20:]).
- 3. Assigning to a list slice will replace that range in the original
     sequence with what's referenced even if their lengths are different.


### [Item 6: Avoid using start, end and stride in a single slice](item_06_avoid_using.py)
- 1. Specifying start, end, and stride in a slice can be extremely confusing.
- 2. Prefer using positive stride values in slices without start or end
     indexes. Avoid negative stride values if possible.
- 3. Avoid using start, end and stride together in a single slice. If you need
     all three parameters, consider doing two assignments (one to slice,
     another to stride) or using islice form itertools built-in module.


### [Item 7: Use list comprehensions instead of map and filter](item_07_list_not_map_filter.py) 
- 1. List comprehensions are clearer than the map and filter built-in
     functions because they don't require extra lambda expressions.
- 2. List comprehensions allow you easily skip items from the input list, a
     behavior map doesn't support without help from filter.
- 3. Dictionaries and sets also support comprehension expressions.


### [Item 8: Avoid more than two expressions in list comprehensions](item_08_no_more_than_2_expressions.py)
- 1. List comprehensions support multiple levels of loops and multiple
     conditions per loop level.
- 2. List comprehensions with more than two expressions are very difficult to
     read and should be avoided.


### [Item 9: Consider generator expressions for large comprehensions](item_09_generator_expressions.py)
- 1. List comprehensions can cause problems for large inputs by using too much
     memory.
- 2. Generator expressions avoid memory issues by producing outputs one at a
     time as an iterator.
- 3. Generator expressions can be composed by passing the iterator from one
     generator expression into the for subexpression of another.
- 4. Generator expressions execute very quickly when chained together.


### [Item 10: Prefer enumerate over range](item_10_prefer_enumerate.py)
- 1. enumerate provides concise syntax for looping over an iterator and
     getting the index of each item from the iterator as you go.
- 2. Prefer enumerate instead of looping over a range and indexing into a
     sequence.
- 3. You can supply a second parameter to enumerate to specify the number from
     which to begin counting (zero is default).


### [Item 11: Use zip to process iterators in parallel](item_11_use_zip.py)
- 1. The zip built-in function can be used to iterate over multiple iterators
     in parallel.
- 2. In Python 3, zip is a lazy generator that produces tuples. In Python 2,
     zip returns the full result as a list of tuples.
- 3. zip truncates its outputs silently if you supply it with iterators of
     different lengths.
- 4. The zip_longest function from the itertools built-in module lets you
     iterate over multiple iterators in parallel regardless of their
     lengths (see Item 46: Use built-in algorithms and data structures).


### [Item 12: Avoid else blocks after for and while loops](item_12_avoid_else.py)
- 1. Python has special syntax that allows else blocks to immediately follow
     for and while loop interior blocks.
- 2. The else block after a loop only runs if the loop body did not encounter
     a break statement.
- 3. Avoid using else blocks after loops because their behavior isn't
     intuitive and can be confusing.


### [Item 13: Take advantage of each block in try/except/else/finally](item_13_try_except_else_finally.py)
- 1. The try/finally compound statement lets you run cleanup code regardless
     of whether exceptions were raised in the try block.
- 2. The else block helps you minimize the amount of code in try blocks and
     visually distinguish the success case from the try/except blocks.
- 3. An else block can be used to perform additional actions after a
     successful try block but before common cleanup in a finally block.


## Chapter 2: Functions


### [Item 14: Prefer exceptions to returning None](item_14_prefer_exceptions.py)
- 1. Functions that return None to indicate special meaning are error prone
     because None and other values (e.g., zero, the empty string) all
     evaluate to False in conditional expressions.
- 2. Raise exceptions to indicate special situations instead of returning
     None. Expect the calling code to handle exceptions properly when they
     are documented.


### [item 15: Know how closures interact with variable scope](item_15_closure_variable_scope.py)
- 1. Closure functions can refer to variables from any of the scopes in which 
     they were defined.
- 2. By default, closure can't affect enclosing scopes by assigning variables.
- 3. In Python 3, use the nonlocal statement to indicate when a closure can 
     modify a variable in its enclosing scopes.
- 4. In Python 2, use a mutable value (like a single-item list) to work around
     the lack of the nonlocal statement.
- 5. Avoid using nonlocal statements for anything beyond simple functions.


### [Item 16: Consider generators instead of returning lists](item_16_generators_instead_of_lists.py)
- 1. Using generators can be clearer than the alternative of returning lists
    of accumulated results.
- 2. The iterator returned by a generator produces the set of values passed to
    yield expressions within the generator function's body.
- 3. Generators can produce a sequence of outputs for arbitrarily large inputs
    because their working memory doesn't include all inputs and outputs.


### [Item 17: Be defensive when iterating over arguments](item_17_be_defensive.py)
- 1. Beware of functions that iterate over input arguments multiple times. If
     these arguments are iterators, you may see strange behavior and missing 
-     values.
- 2. Python's iterator protocol defines how containers and iterators interact
     with the iter and next built-in functions, for loops, and related 
     expression.
- 3. You can easily define your own iterable container type by implementing 
     the __iter__ method as a generator.
- 4. You can detect that a value is an iterator (instead of a container) if
     calling iter on it twice produces the same result, which can then be 
     progressed with the next built-in function.


### [Item 18: Reduce visual noise with variable positional arguments](item_18_reduce_visual_noise.py)
- 1. Functions can accept a variable number of positional arguments by using
    *args in the def statement.
- 2. You can use the items from a sequence as the positional arguments for a
    function with the * operator.
- 3. Using the * operator with a generator may cause your program to run out
    of memory and crash.
- 4. Adding new positional parameters to functions that accept *args can
    introduce hard-to-find bugs.

### [Item 19: Provide optimal behavior with keyword arguments](item_19_provide_optimal_behavior.py)
- 1. Function arguments can be specified by position or by keyword.
- 2. Keywords make it clear what the purpose of each arguments is when it
    would be confusing with only positional arguments.
- 3. Keywords arguments with default values make it easy to add new behaviors
    to a function, especially when the function has existing callers.
- 4. Optional keyword arguments should always be passed by keyword instead of
    by position.


### [Item 20: Use None and Docstrings to specify dynamic default arguments](item_20_use_none_and_docstrings.py)
- 1. Closure functions can refer to variables from any of the scopes in which
     they were defined.
- 2. By default, closure can't affect enclosing scopes by assigning variables.
- 3. In Python 3, use the nonlocal statement to indicate when a closure can
     modify a variable in its enclosing scopes.
- 4. In Python 2, use a mutable value (like a single-item list) to work around
     the lack of the nonlocal statement.
- 5. Avoid using nonlocal statements for anything beyond simple functions.


### [Item 21: Enforce clarity with key-word only arguments](item_21_enforce_clarity.py)
- 1. Keyword arguments make the intention of a function call more clear.
- 2. Use keyword-only arguments to force callers to supply keyword arguments
    for potentially confusing functions, especially those that accept
    multiple Boolean flags.
- 3. Python 3 supports explicit syntax for keyword-only arguments in
    functions.
- 4. Python 2 can emulate keyword-only arguments for functions by using
    **kwargs and manually raising TypeError exceptions.
