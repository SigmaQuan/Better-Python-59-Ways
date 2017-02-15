# Item 15: Know how closures interact with variable scope


# Say you want to sort a list of numbers but prioritize one group of numbers
# to come first. This pattern is useful when you're rendering a user interface
# and want important messages or exceptional events to be displayed before
# everything else.

# A common way to do this is to pass a helper function as the key argument to
# a list's sort method. The helper's return value will be used as the value
# for sorting each item in the list. The helper can check whether the given
# item is in the important group and can vary the sort key accordingly.


def sort_priority(values, group):
    def helper(x):
        if x in group:
            return (0, x)
        return (1, x)
    values.sort(key=helper)


# This function works for simple inputs.


numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = {2, 3, 5, 7}
sort_priority(numbers, group)
print(numbers)
# [2, 3, 5, 7, 1, 4, 6, 8]


# There are three reasons why this function operates as expected:
# 1. Python supports closures: functions that refer to variables from the
#     scope in which they were defined. This is why the helper function is
#     able to access the group argument to sort_priority.
# 2. Functions are first-class objects in Python, meaning you can refer to
#     them directly, assign them to variables, pass them as arguments to other
#     functions, compare them in expressions and if statements, etc. This is
#     how the sort method can accept a closure function as the key argument.
# 3. Python has specific rules for comparing tuples. It first compares items
#     in index zero, then index one, then index two, and so on. This is why
#     the return value from the helper closure causes the sort order to have
#     two distinct groups.

# It'd be nice if this function returned whether higher-priority items were
# seen at all so the user interface code can act accordingly. Adding such
# behavior seems straightforward. There's already a closure function for
# deciding which group each number is in. Why not also use the closure to
# flip a flag when high-priority items are seen? Then the function can return
# the flag value after it's been modified by the closure.

# Here, I try to do that in a seemingly obvious way:


def sort_priority2(numbers, group):
    found = False
    def helper(x):
        if x in group:
            found = True  # Seems simple
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found


# I can run the function on the same inputs as before.


found = sort_priority2(numbers, group)
print('Found:', found)
print(numbers)
# Found: False
# [2, 3, 5, 7, 1, 4, 6, 8]


# The sorted results are correct, but the found result is wrong. Items from
# group were definitely found in numbers, but the function returned False. How
# could this happen?

# When you reference a variable in an expression, the Python interpreter will
# traverse the scope to resolve the reference in this order:
# 1. The current function's scope
# 2. Any enclosing scopes (like other containing functions)
# 3. The scope of the module that contains the code (also called the global
#     scope)
# 4. The built-in scope (that contains functions like len and str)

# If none of these places have a defined variable with the referenced name,
# then a NameError exception is raised.

# Assigning a value to a variable works differently. If the variable is
# already defined in the current scope, then it will just take on the new
# value. If the variable doesn't exist in the current scope, the Python
# treats the assignment as a variable definition. The scope of the newly
# defined variable is the function that contains the assignment.

# This assignment behavior explains the wrong return value of the
# sort_priority2 function. The found variable is assigned to True in the
# helper closure. The closure's assignment is treated as a new variable
# definition within helper, not as an assignment within sort_priority2.


def sort_priority2(number, group):
    found = False  # Scope: 'sort_priority2
    def helper(x):
        if x in group:
            found = True  # Scope: 'helper'  -- Bad!
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found


# Encountering this problem is sometimes called the scoping bug because it
# can be so surprising to newbies. But this is the intended result. This
# behavior prevents local variables in a function from polluting the
# containing module. Otherwise, every assignment within a function would put
# garbage into the global module scope. Not only would that be noise, but the
# interplay of the resulting global variables could cause obscure bugs.


# Getting data out


# In Python 3, there is special syntax for getting data out of a closure. The
# nonlocal statement is used to indicate that scope traversal should happen
# upon assignment for a specific variable name. The only limit is that
# nonlocal won't traverse up to the module-level scope (to avoid polluting
# globals)

# Here, I define the same function again using nonlocal:


def sort_priority3(numbers, group):
    found = False
    def helper(x):
        nonlocal found
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found


# The nonlocal statement makes it clear when data is being assigned out of a
# closure into another scope. It's comlementary to the global statement, which
# indicates that a variable's assignment should go directly into the module
# scope.

# However, much like the anti-patten of global variables, I'd caution against
# using nonlocal for anything beyond simple functions. The side effect of
# nonlocal can be hard to follow. It's especially hard to understand in long
# functions where the nonlocal statements and assignments to associated
# variables are far apart.

# When your usage of nonlocal starts getting complicated, it's better to wrap
# your state in a helper class. Here, I define a class that achieves the same
# result as the nonlocal approach. It's a little longer, but is much easier to
# read (see Item 23: "Accept Functions for simple interfaces instead of
# classes" for detail on the __call__ special method).


class Sorter(object):
    def __init__(self, group):
        self.group = group
        self.found = False

    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return (1, x)


sorter = Sorter(group)
numbers.sort(key=sorter)
print(numbers)
assert sorter.found is True
# [2, 3, 5, 7, 1, 4, 6, 8]


# Scope in Python 2


# Unfortunately, Python 2 donesn't support that nonlocal keyword. In order to
# get similar behavior, you need to use a work-around that takes advantage of
# Python's scoping rules. This approach isn't pretty, but it's the common
# Python idiom.


# Python 2
def sort_priority(numbers, group):
    found = [False]
    def helper(x):
        if x in group:
            found[0] = True
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found[0]


# As, explained above, Python will traverse up the scope where the found
# variable is referenced to resolve its current value. The trick is that the
# value for found is a list, which is mutable. This means that once retrieved,
# the closure can modify the state of found to send data out of the inner
# scope (with found[0] = True).

# This approach also works when the variable used to traverse the scope is a
# dictionary, a set, or an instance of a class you've defined.


# Things to remember

# 1. Closure functions can refer to variables from any of the scopes in which
#     they were defined.
# 2. By default, closure can't affect enclosing scopes by assigning variables.
# 3. In Python 3, use the nonlocal statement to indicate when a closure can
#     modify a variable in its enclosing scopes.
# 4. In Python 2, use a mutable value (like a single-item list) to work around
#     the lack of the nonlocal statement.
# 5. Avoid using nonlocal statements for anything beyond simple functions.
