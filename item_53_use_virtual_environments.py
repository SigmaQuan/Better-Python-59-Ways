# Item 53: Use virtual environments for isolated and reproducible dependencies


# Building larger and more complex programs often leads you rely on various
# packages from the Python community (see Item 48: "Know where to find
# community-built modules"). You'll find yourself running pip to install pytz,
# numpy, and many others.

# The problem is that, by default, pip installs new packages in a global
# location. That cause all Python programs on your system to be affected by
# these install modules. In theory, this shouldn't be an issue. If you install
# a package and never import it, how could it affect your programs?

# The trouble comes from transitive dependencies: the packages that the
# packages you install depend on. For example, you can see what the Sphinx
# package depends on after installing it by asking pip.

# pip3 show Sphinx

# If you install another package like flask, you can see that it, too, depends
# on the Jinja2 package.

# pip show flask

# The conflict arises as Sphinx and flask diverge over time. Perhaps right now
# they both the both require the same version of Jinja2 and everything is
# fine. But six months or a year from now, Jinja2 may release a new version
# that makes breaking changes to users of the library. If you update your
# global version of Jinja2 with pip install --upgrade, you may find that
# Sphinx breaks while flask keep working.

# The cause of this breakage is that Python can only have a single global
# version of a module installed at a time. If one of your installed packages
# must use the new version and another package must use the old version, your
# system isn't going to work properly.

# Such package can even happen when package maintainers try their best to
# preserve API compatibility between release (see Item 50: "Use packages to
# organize modules and provide stable APIs"). New versions of a library can
# subtly change behaviors that API-consuming code relies on. Users on a
# system may upgrade one package to a new version but not others, which could
# dependencies. There's a constant risk of the ground moving beneath your
# feet.

# These difficulties are magnified when you collaborate with other developers
# who do their work on separate computers. It's reasonable to assume that the
# versions of Python and global packages they have installed on their machines
# will be slightly different than your own. This can cause frustrating
# situations where a codebase works perfectly on one programmer's machine and
# is completely broken on another's.

# The solution to all of these problems is a tool called pyvenv, which
# provides virtual environments. Since Python 3.4, the pyvenv command-line
# tool is available by default along with the Python installation (it's also
# accessible with python -m venv). Prior versions of Python require installing
# a separate package (with pip install virtualenv) and using a command-line
# tool called virtualenv.

# pyvenv allows you to create isolated versions of the Python environment.
# Using pyvenv, you can have many different versions of the same package
# installed on the same system at the same time without conflicts. This lets
# you work on many different projects and use many different tools on the same
# computer.

# pyvenv does this by installing explicit versions of packages and their
# dependencies into completely separate directory structures. This makes it
# possible to reproduce a Python environment that you know will work with your
# code. It's reliable way to avoid surprising breakages.

# The pyvenv Command

# Here's a quick tutorial on how to use pyvenv effectively. Before using the
# tool, it's important to note the meaning of the python3 command-line on your
# system. On my computer, python3 is located in the /usr/local/bin directory
# and evaluates to version 3.4.2 (see Item 01: "Know which version of Python
# you're using?").

# $ which python3
# /usr/bin/python3
# $ python3 --version
# Python 3.5.2

# To demonstrate the setup of my environment, I can test that running a
# command to import the pytz module doesn't cause an error. This works
# because I already have the pytz installed as a global module.

# $ python3 -c 'import pytz'

# Now, I use pyvenv to create a new virtual environment called myproject.
# Each virtual environment must live in its own unique directory. The result
# of the command is a tree of directories and files.

# $ pyvenv /tmp/myproject
# $ cd /tmp/myproject/
# /tmp/myproject$ ls
# bin  include  lib  lib64  pyvenv.cfg  share

# To start using the virtual environment, I use the source command from my
# shell on the  bin/activate script. It also updates my command-line prompt to
# include the virtual environment name ('myproject) to make it extremely clear
# what I'm working on.

# /tmp/myproject$ source bin/activate
# (myproject) robot@robot-gpu:/tmp/myproject$ which python3

# After activation, you can see that the path to the python3 command-line tool
# has moved to within the virtual environment directory.

# (myproject) robot@robot-gpu:/tmp/myproject$ which python3
# /tmp/myproject/bin/python3
# (myproject) robot@robot-gpu:/tmp/myproject$ ls -l /tmp/myproject/bin/python3
# lrwxrwxrwx 1 robot robot 9 Jun 15 13:46 /tmp/myproject/bin/python3 -> python3.5
# (myproject) robot@robot-gpu:/tmp/myproject$ ls -l /tmp/myproject/bin/python3.5
# lrwxrwxrwx 1 robot robot 18 Jun 15 13:46 /tmp/myproject/bin/python3.5 -> /usr/bin/python3.5

# This ensures that changes to the outside system will not affect the virtual
# environment. Even if the outer system upgrades its default python3 to
# version 3.5, my virtual environment will still explicitly point to
# version 3.4.

# The virtual environment I created with pyvenv starts with no packages
# installed except for pip and setuptools. Trying to use the pytz package
# that was installed as a global module in the outsize system will fail
# because it's unknown to the virtual environment.

# (myproject) robot@robot-gpu:/tmp/myproject$ python3 -c 'import pytz'
# Traceback (most recent call last):
#   File "<string>", line 1, in <module>
# ImportError: No module named 'pytz'

# I can use pip to install the pytz module into my virtual environment.

# (myproject) robot@robot-gpu:/tmp/myproject$ pip3 install pytz

# Once it's installed, I can verify that it's working with the same test
# import command.

# (myproject) robot@robot-gpu:/tmp/myproject$ python3 -c 'import pytz'
# (myproject) robot@robot-gpu:/tmp/myproject$

# When you're done with a virtual environment and want to go back to your
# default system, you use the deactivate command. This restores your
# environment to the system defaults, including the location of the python3
# command-line tool.

# (myproject) robot@robot-gpu:/tmp/myproject$ deactivate
# robot@robot-gpu:/tmp/myproject$ which python3
# /usr/bin/python3


# Reproducing Dependencies

# Once you have a virtual environment, you can continue installing packages
# with pip as you need them. Eventually, you may want to copy your environment
# somewhere else. For example, say you want to reproduce your development
# environment on a production server. Or maybe you want to clone someone
# else's environment on your own machine so you can run their code.

# pyvenv makes these situations easy. You can use the pip freeze command to
# save all of your explicit package dependencies into a file. By convention,
# this file is named requirements.txt

# (myproject) robot@robot-gpu:/tmp/myproject$ pip3 freeze > requirements.txt
# (myproject) robot@robot-gpu:/tmp/myproject$ cat requirements.txt
# numpy==1.8.2
# pytz==2014.4
# requests==2.3.0

# Now, imagine that you'd like to have another virtual environment that
# matches the myproject environment. You can create a new directory like
# before using pyvenv and activate it.
# robot@robot-gpu:~$ pyvenv /tmp/otherproject
# robot@robot-gpu:~$ cd /tmp/otherproject/
# robot@robot-gpu:/tmp/otherproject$ source bin/activate
# (otherproject) robot@robot-gpu:/tmp/otherproject$

# The new environment will have no extra packages installed.

# (otherproject) robot@robot-gpu:/tmp/otherproject$ pip3 list
# pip (8.1.1)
# pkg-resources (0.0.0)
# setuptools (20.7.0)

# You can install all of the packages from the first environment by running
# pip install on the requirements.txt that you generated with the pip freeze
# command.

# (otherproject) robot@robot-gpu:/tmp/otherproject$ pip3 install -r /tmp/myproject/requirements.txt

# This command will crank along for a little while as it retrieves and
# installs all of the packages required to reproduce the first environment.
# Once it's done, listing the set of installed packages in the second virtual
# environment will produce the same list of dependencies found in the first
# virtual environment.

# (otherproject) robot@robot-gpu:/tmp/otherproject$ pip list
# pip (8.1.1)
# pkg-resources (0.0.0)
# setuptools (20.7.0)

# Using a requirement.txt file is ideal for collaborating with others through
# a revision control system. You can commit changes to your code at the same
# time you update your list of package dependencies, ensuring that they move
# in lockstep.

# The gotcha with virtual environments is that moving them breaks everything
# because all of the paths, like python3, are hard-coded to the environment's
# install directory. But that doesn't matter. The whole purpose of virtual
# environments is to make it easy to reproduce the same setup. Instead of
# moving a virtual environment directory, just freeze the old one, create a
# new one somewhere else, and reinstall everyting from the requirements.txt
# file.


# Things to remember

# 1. Virtual environment allow you to use pip to install many different
#    versions of the same package on the same machine without conflicts.
# 2. Virtual environments are created with pyvenv, enabled with source
#    bin/activate, and disabled with deactivate.
# 3. You can dump all of the requirements of an environment with pip freeze.
#    You can reproduce the environment by supplying the requirements.txt file
#    to pip install -r.
# 4. In versions of Python before 3.4, the pyvenv tool must be downloaded and
#    installed separately. The command-line tool is called virtualenv instead
#    of pyvenv.
