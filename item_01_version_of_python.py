# Chapter 1: Pythonic thinking


# Item 1: Know which version of python you're using


# $ python --version
# Python 2.7.12
#
# $ python3 --version
# Python 3.5.2


import sys
print(sys.version_info)
# sys.version_info(major=2, minor=7, micro=12, releaselevel='final', serial=0)

print(sys.version)
# 2.7.12 (default, Nov 19 2016, 06:48:10)
# [GCC 5.4.0 20160609]


# Things to Remember

# 1. There are two major version of Python still in active use: Python 2 and
#     Python 3.
# 2. There are multiple popular runtimes for Python: CPython, Jython,
#     IronPython, PyPy, etc.
# 3. Be sure that the command-line for running Python on your system is the
#     version you expect it to be.
# 4. Prefer Python 3 for your next project because that is the primary focus
#     of the Python community.
