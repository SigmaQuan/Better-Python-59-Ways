# Item 48: Know where to find community built modules


# Python has a central repository of modules (https://pypi.python.org) for you
# to install and use in your programs. These modules are built and maintained
# by people like you: the Python community. When you find yourself facing an
# unfamiliar challenge, the Python Package Index (PyPI) is a great place to
# look for code that will get you closer to your goal.

# To use the Package Index, you'll need to use a command-line tool named pip.
# pip is installed by default in Python 3.4 and above (it's also accessible
# with python -m pip). For earlier versions, you can find instructions for
# pip on the Python Packaging website (https:packaging.python.org).

# Once installed, using pip to install a new module is simple. For example,
# here I install the pytz module that I used in another item in this chapter
# (see Item 45: Use datatime instead of time for local clocks).

# $ pip3 install pytz

# In the example above, I used the pip3 command-line to install the Python 3
# version of the package. The pip command-line (without the 3) is also
# available for installing packages for Python 2. The majority of popular
# packages are now available for either version of Python (see Item 1: "Know
# which version of Python you're using"). pip can also be used with pyvenv to
# track sets of packages to install for your projects (see Item 53: "Use
# virtual environments for isolated and reproducible dependencies").

# Each module in the PyPI has its own software license. Most of the packages,
# especially the popular ones, have free or open source licenses (see
# http://opensource.org for details). In most cases, these licenses how you to
# include a copy of the module with your program (when in doubt, talk to a
# lawyer).


# Things to remember

# 1. The Python Package Index (PyPI) contains a wealth of common packages
#    that are built and maintained by the Python community.
# 2. pip is the command-line to use for installing packages from PyPI.
# 3. pip is installed by default in Python 3.4 and above; you must install it
#    yourself for older versions.
# 4. The majority of PyPI modules are free and open source software.
