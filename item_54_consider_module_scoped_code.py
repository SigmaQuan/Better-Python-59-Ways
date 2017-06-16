# Chapter 8: Production


# Putting a Python program to use requires moving it from a development
# environment to a production environment. Supporting disparate configurations
# like this can be a challenge. Making programs that are dependable in
# multiple situations is just as important as making programs with correct
# functionality.

# The goal is to productionize your Python programs and make them bulletproof
# while they're in use. Python has built-in modules that aid in hardening your
# programs. It provides facilities for debugging, optimizing, and testing to
# maximize the quality and performance of your programs at runtime.


# Item 54: Consider module-scoped code to configure deployment environments

# A deployment environment is a configuration in which your program runs.
# Every program has at least one deployment environment, the production
# environment. The goal of writing a program in the first place is to put it
# to work in the production environment and achieve some kind of outcome.

# Writing or modifying a program requires being able to run it on the computer
# you use for developing. The configuration of your development may be much
# different from your production environments have the same Python packages
# installed. The trouble is that production environment often require many
# external assumptions that are hard to reproduce in development environments.

# For example, say you want to run your program in a web server container and
# give it access to a database. This means that very time you want to modify
# your program's code, you need to run a server container, the database must
# be set up properly, and your program needs to password for access. That's a
# very high cost if all you're trying to do is verify that a one-line change
# to your program works correctly.

# The best way to work around these issues is to override parts of your
# program at startup time to provide different functionality depending on the
# deployment environment. For example, you could have two different __main__
# files, one for production and one for development.

# # dev_main.py
# TESTING = True
# import db_connection
# db = db_connection.Database()

# # prod_main.py
# TESTING = False
# import db_connection
# db = db_connection.Database()

# The only difference between the two files is the value of the TESTING
# constant. Other modules in your program can then import the __main__ module
# and use the value of TESTING to decide how they define their own attributes.

# # db_connection.py
# import __main__
#
#
# class TestingDatabase(object):
#     #...
#     pass
#
#
# class RealDatabase(object):
#     #...
#     pass
#
#
# if __main__.TESTING:
#     Database = TestingDatabase
# else:
#     Database = RealDatabase

# The key behavior to notice here is that code running in module scope--not
# inside any function or method--is just normal Python code. You can use an
# if statement at the module level to decide how the module will define names.
# This makes it easy to tailor modules to your various deployment
# environments. You avoid having to reproduce costly assumptions like
# database configurations when they aren't needed. You can inject fake or mock
# implementations that ease interactive development and testing (see Item 56:
# "Test everything with unittest")

# Note
# Once your deployment environments get complicated, you should consider moving
# them out of Python constants (like TESTING) and into dedicated configuration
# files. Tools like the configparser built-in module let you maintain
# production configurations separate from code, a distinction that's crucial for
# collaborating with an operations team.

# This approach can be used for more than working around external assumptions.
# For example, if you know that your program must work differently based on its
# host platform, you can inspect the sys module before defining top-level
# constructs in a module.

# db_connection.py
import sys


class Win32Database(object):
    #...
    pass


class PosixDatabase(object):
    #...
    pass


if sys.platform.startswith('win32'):
    Database = Win32Database
else:
    Database = PosixDatabase


# Similarly, you can use environment variable from os.environ to guide your
# module definitions.


# Things to remember

# 1. Programs often need to run in multiple deployment environments that each
#    have unique assumptions and configurations.
# 2. You can tailor a module's contents to different deployment environments
#    by using normal Python statements in module scope.
# 3. Module contents can be the product of any external condition, including
#    host introspection through the sys and os modules.
