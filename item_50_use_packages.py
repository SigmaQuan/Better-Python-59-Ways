# Item 50: Use packages to organize modules and provide stable APIs


# As the size of a program's codebase grows, it's natural for you to
# reorganize its structure. You split larger functions into smaller functions.
# You refactor data structures into helper classes (see Item 22: "Prefer
# helper class over bookkeeping with dictionaries and tuples"). You separate
# functionality into various modules that depend on each other.

# At some point, you'll find yourself with so many modules that you need
# another layer in your program to make it understandable. For this purpose,
# Python provides packages. Packages are modules that contain other modules.

# In most cases, packages are defined by putting an empty file named
# __init__.py into a directory. Once __init__.py is present, any other Python
# in that directory will be available for import using a path relative to the
# directory. For example, imagine that you have the following directory
# structure in your program.

# main.py
# mapackage/__init__.py
# mapackage/models.py
# mapackage/utils.py

# To import the utils module, you use the absolute module name that includes
# the package directory's name.

# main.py
# from mypackage import utils

# This pattern continue when you have package directories present within other
# packages (like mypackage.foo.bar)

# Note
# Python 3.4 introduces namespace packages, a more flexible way to define
# packages. Namespace packages can be composed of modules from completely
# separate directories, zip archives, or even remote systems. For details on
# how to use the advanced features of namespace packages, see PEP 420
# (http://www.python.org/dev/peps/pep-0420/).

# The functionality provided by packages has two primary purposes in Python
# programs.


# Namespaces

# The first use of packages is to help divide your modules with the same
# filename but different absolute paths that are unique. For example, here's a
# program that imports attributes from two modules with the same name,
# utils.py. This works because the modules can be addressed by their absolute
# paths.

# main.py
# from analysis.utils import log_base2_bucket
# from frontend.utils import stringify

# bucket = stringify(log_base2_bucket)

# This approach breaks down when the functions, classes, or submodules defined
# in packages have the same names. For example, say you want to use the
# inspect function from both the analysis.utils and frontend.utils modules.
# Importing the attributes directly won't work because the second import
# statement will overwrite the value of inspect in the current scope.

# main2.py
# from analysis.utils import inspect
# from frontend.utils import inspect  # Overwrites!

# The solution is to use the as clause of the import statement to rename
# whatever you've imported for the current scope.

# main3.py
# from analysis.utils import inspect as analysis_inspect
# from frontend.utils import inspect as frontend_inspect

# value = 33
# if analysis_inspect(value) == frontend_inspect(value):
#     print('Inspection equal!')

# The as clause can be use to rename anything you retrieve with the import
# statement, including entire modules. This makes it easy to access
# namespaced code and make its identity clear when you use it.

# Note
# Another approach for avoiding imported name conflicts is to always access
# names by their highest unique module name.

# For the example above, you'd first import analysis.utils and import
# frontend.utils. Then, you'd access the inspect functions with the full
# paths of analysis.utils.inspect and frontend.utils.inspect.

# This approach allows you to avoid the as clause altogether. It also makes it
# abundantly clear to new readers of the code where each function is defined.


# Stable APIs

# The second use of packages in Python is to provide strict, stable APIs for
# external consumers.

# When you're writing an API for wider consumption, like an open source
# package (see Item 48: "Know where to find community-built modules"), you'll
# want to provide stable functionality that doesn't change between release. To
# ensure that happens, it's important to hide your internal code organization
# from external users. This enables you to refactor and improve your package's
# internal modules without breaking existing users.

# Python can limit the surface area exposed to API consumers by using the
# __all__ special attribute of a module or package. The value of  __all__ is a
# list of every name to export from the module as part of its public API. When
# consuming code does from foo import *, only the attributes in foo.__all__
# will be imported from foo. If __all__ isn't  present in foo, then only
# public attributes, those without a leading underscore, are imported (see
# Item 27: "Prefer public attributes over private ones").

# For example, say you want to provide a package for calculating collisions
# between moving projectiles. Here, I define the models module of mypackage to
# contain the representation of projectiles:

# models.py
__all__ = ['Projectile']


class Projectile(object):
    def __init__(self, mass, velocity):
        self.mass = mass
        self.velocity = velocity


# I also define a utils module in mypackage to perform operations on the
# Projectile instances, such as simulating collisions between them.

# utils.py
from . models import Projectile

__all__ = ['simulate_collision']


def _dot_product(a, b):
    # ...
    pass


def simulate_collision(a, b):
    # ...
    pass

# Now, I'd like to provide all of the public parts of this API as a set of
# attributes that are available on the mypackage module. This will allow
# downstream consumers to always import directly from mypackage instead of
# importing from my package.models or mypackage.utils. This ensures that API
# consumer's code continue to work even if the internal organization of
# mypackage changes (e.g., models.py is deleted).

# To do this with Python packages, you need to modify the __init__.py file in
# the mypackage directory. This file actually becomes the contents of the
# mypackage directory. Thus, you can specify an explicit API for mypackage by
# limiting what you import into __init__.py. Since all of my internal modules
# already specify __all__, I can expose the public interface of mypackage by
# simply importing everything from the internal modules and updating __all__
# accordingly.

# __init__.py
__all__ = []
from . models import *
__all__ += models.__all__
from . utils import *
__all__ += utils.__all__

# Here's a consumer of the API that directly imports from mypackage instead of
# accessing the inner modules:

# api_consumer.py
from mypackage import *

a = Projectile(1.5, 3)
b = Projectile(4, 1.7)
after_a, after_b = simulate_collision(a, b)


# Notably, internal-only functions like mypackage.utils._dot_product will not
# be available to the API consumer on mypackage because they weren't present
# in __all__. Being omitted from __all__ means they weren't imported by the
# from mypackage import * statement. The internal-only names are effectively
# hidden.

# This whole approach works great when it's important to provide an explicit,
# stable API. However, if you're building an API for use between your own
# modules, the functionality of __all__ is probably unnecessary and should be
# avoided. The namespacing provided by packages is usually enough for a team
# of programmers to collaborate on large amounts of code they control while
# maintaining reasonable interface boundaries.


# Beware of import *
# Import statements like from x import y are clear because the source of y is
# explicitly the x package or module. Wildcard imports like from foo import *
# can also be useful, especially in interactive Python sessions. However,
# wildcards make code more difficult to understand.
# 1. from foo import * hides the source of names from new readers of the code.
#    If a module has multiple import * statements, you'll need to check all
#    of the referenced modules to figure out where a name was defined.
# 2. Names from import * statements will overwrite any conflicting names
#    within the containing module. This can lead to strange bugs caused by
#    accidental interactions between your code and overlapping names from
#    multiple import * statements.
# The safest approach is to avoid import * in your code and explicitly import
# names with the from x import y style.


# Things to remember

# 1. Packages in Python are modules that contain other modules. Packages allow
#    you to organize your code into separate, non-conflicting namespaces with
#    unique absolute module names.
# 2. Simple package are defined by adding an __init__.py file to a directory
#    that contains other source files. These files become that child modules
#    of the directory's package. Package directories may also contain other
#    packages.
# 3. You can provide an explict API for a module by listing its publicly
#    visible name in its __all__ special attribute.
# 4. You can hide a package's internal implementation by only importing public
#    names in the package's __init__.py file or by naming internal-only
#    members with a leading underscore.
# 5. When collaborating within a single team or on a single codebase, using
#    __all__ for explicit APIs is probably unnecessary.
