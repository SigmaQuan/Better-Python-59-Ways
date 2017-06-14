# Item 52: Know how to break circular dependencies


# Inevitably, while you're collaborating with others, you'll find a mutual
# interdependency between modules. It can even happen while you work by
# yourself on the various parts of a single program.

# There are three other ways to break circular dependencies.

# Reordering Imports
# The first approach is to change the order of imports.

# Import, Configure, Run
# A second solution to the circular imports problem is to have your modules
# minimize side effects at import time.

# Dynamic Import
# The third--and often simplest--solution to the circular imports problem is
# to use an import statement within a function or method. This is called a
# dynamic import because the module import happens while the program is
# running, not while the program is first starting up and initializing its
# modules.


# Things to remember

# 1. Circular dependencies happen when two modules must call into each other
#    at import time. They can cause your program to crash at startup.
# 2. The best way to break a circular dependency is refactoring mutual
#    dependencies into a separate module at the bottom of the dependency tree.
# 3. Dynamic imports are the simplest solution for breaking a circular
#    dependency between modules while minimizing refactoring and complexity.
