# Chapter 7: Collaboration


# There are language features in Python to help you construct well-defined
# APIs with clear interface boundaries. The Python community has established
# best practices that maximize the maintainability of code over time. There
# are also standard tools that ship with Python that enable large teams to
# work together across disparate environment.

# Collaborating with others on Python programs requires being deliberate about
# how you write your code. Even if you're working on your own, chances are you
# will be using code written by someone else via the standard library or open
# source packages. It's important to understand the mechanisms that make it
# easy to collaborate with other Python programmers.


# Item 49: Write docstrings for every function, class and module


# Documentation in Python is extremely important because of the dynamic nature
# of the language. Python provides built-in support for attaching
# documentation to blocks of code. Unlike many other languages, the
# documentation from a program's source code is directly accessible as the
# program runs.

# For example, you can add documentation by providing a docstring immediately
# after the def statement of a function.


def palindrome(word):
    """Return True if the given word is a palindrome."""
    return word == word[::-1]


# You ran retrieve the docstring form within the Python program itself by
# accessing the function's __doc__ special attribute.

print(repr(palindrome.__doc__))
# 'Return True if the given word is a palindrome.'

# Docstring can be attached to functions, classes, and modules. This
# connection is part of the process of compiling and running a Python program.
# Support for docstrings and the __doc__ attribute has three consequences:
# 1. The accessibility of documentation makes interactive development easier.
#    You can inspect functions, classes, and modules to see their
#    documentation by using the help built-in function. This makes the Python
#    interactive interpreter (the Python "shell") and tools like IPython Note
#    (http://ipython.org) a joy to use while you're developing algorithms,
#    testing APIs, and writing code snippets.
# 2. A standard way of defining documentation makes it easy to build tools
#    that convert the text into more appealing formats (like HTML). This has
#    led to excellent documentation-generation tools for the Python community,
#    such as Sphinx (http://sphinx-doc.org). It's also enabled
#    community-founded sites like Read the Docs (https://readthedocs.org) that
#    provide free hosting of beautiful-looking documentation for open source
#    Python projects.
# 3. Python's first-class, accessible, and good-looking documentation
#    encourage people to write more documentation. The members of the Python
#    community have a strong belief in the importance of documentation. There
#    is an assumption that "good code" also means well-documented code. This
#    means that you can expect most open source Python libraries to have
#    decent documentation.

# To participate in this excellent culture of documentation, you need to
# follow a few guidelines when you write docstrings. The full details are
# discussed online in PEP 257 (http://www.python.org/dev/peps/pep-0257).
# There are a few best-practices you should be sure to follow.


# Documenting Modules

# Each module should have a top-level docstring. This is string literal that
# is the first statement in a source file. It should use three double quotes
# (""").  The goal of this docstring is to introduce the module and its
# contents.

# The first line of the docstring should be a single sentence describing the
# module's purpose. The paragraphs that follow should contain the details that
# all users of the module should know about its operation. The module
# docstring is also a jumping-off point where you can high-light important
# classes and functions found in the module.

# Here's an example of a modules docstring:

# words.py
# !/usr/bin/env python3
"""Library for test words for various linguistic patterns.

Testing how words relate to each other can be tricky sometimes! This module
provides easy ways to determine when words you've found have special
properties.

Available functions:
- palindrome: Determine if a word is a palindrome.
- check_anagram: Determine if two words are anagrams.
...
"""
# ...

# If the module is a command-line utility, the module docstring is also a
# great place to put usage information for running the tool from the
# command-line.


# Documenting Classes

# Each class should have a class-level docstring. This largely follows the
# same pattern as the module-level docstring. The first line is the
# single-sentences purpose of the class. Paragraphs that follow discuss
# important details of the class's operation.

# Important public attributes and methods of the class should be highlighted
# in the class-level docstring. It should also provide guidance to subclasses
# on how to properly interact with protected attributes (see Item 27: "Prefer
# public attributes over private ones") and the super class's methods.

# Here's an example of a class docstring:

class Player(object):
    """Represents a player of the game.

    Subclasses may override the 'tick' method to provide custom animations for
    the player's movement depending on their power level. etc.

    Public attributes:
    - power: Unused power-ups (float between 0 and 1).
    - coins: Coins found during the level (integer).
    """
    # ...
    pass


# Documenting Functions


# Each public function and method should have a docstring. This follows the
# same pattern as modules and classes. The first line is the single-sentence
# description of what the function does. The paragraphs that follow should
# describe any specific behaviors and the arguments for the function. Any
# return values should be mentioned. Any exceptions that callers must handle
# as part of the function's interface should be explained.

# Here's an example of a function docstring:


def find_anagrms(word, dictionary):
    """Find all anagrams for a word.

    This function only runs as fast as the test for membership in the
    'dictionary' container. It will be slow if the dictionary is a list and
    fast if it's a set.

    Args:
        word: String of the target word.
        dictionary: Container with all strings that are known to be actual
        words.
    Returns:
        List of anagrams that were found. Empty if none were found.
    """
    # ...
    pass

# There are also some special cases in writing docstrings for functions that
# are important to know.
# 1. If your function has no arguments and a single return value, a single
#    sentence description is probably good enough.
# 2. If your function doesn't return anything, it's better to leave out any
#    mention of the return value instead of saying "returns None".
# 3. If you don't expect your function to raise an exception during normal
#    operation, don't mention that fact.
# 4. If your function accepts a variable number of arguments (see Item 18:
#    "Reduce visual noise with variable positional arguments") or
#    keyword-arguments (see Item 19: "Provide optional behavior with keyword
#    arguments"), use *args and **kwargs in the documented list of arguments
#    to describe their purpose.
# 5. If your function has arguments with default values, those defaults should
#    be mentioned (see Item 20: "Use None and docstring to specify dynamic
#    default arguments").
# 6. If your function is a generator (see Item 16: "Consider generators
#    instead of returning lists"), then your docstring should describe what
#    the generator yields when it's iterated.
# 7. If your function is a coroutine (see Item 40: "Consider coroutines to run
#    many functions concurrently"), then your docstring should contain what
#    the coroutine yields, what it excepts to receive from yield expressions,
#    and when it will stop iteration.

# Note

# Once you've written docstrings for your modules, it's important to keep the
# documentation up to date. The doctest built-in module makes it easy to
# exercise usage embedded in docsrings to ensure that your source code and its
# documentation don't diverge over time.


# Things to remember

# 1. Write documentation for every module, class and function using
#    docstrings. Keep them up to date as your code changes.
# 2. For modules: introduce the contents of the module and any important
#    classes or functions all users should know about.
# 3. For classes: document behavior, important attributes, and subclass
#    behavior in the docstring following the class statement.
# 4. For functions and methods: document every argument, returned value,
#    raised exception, and other behaviors in the docstring following the
#    def statement.
