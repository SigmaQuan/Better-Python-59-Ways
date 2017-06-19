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
     values.
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


## Chapter 3: Classes and Inheritance


### [Item 22: Prefer helper classes over bookkeeping with dictionaries and tuples](item_22_prefer_helper_classes.py)
- 1. Avoid making dictionaries with values that are other dictionaries or
    long tuples.
- 2. Use namedtuple for lightweight, immutable data containers before you need
    the flexibility of a full class.
- 3. Move your bookkeeping code to use multiple helper classes when your
    internal state dictionaries get complicated.


### [Item 23: Accept functions for simple interfaces instead of classes](item_23_accepts_functions_4_interfaces.py)
- 1. Instead of defining and instantiating classes, functions are often all
    you need for simple interfaces between components in Python.
- 2. References to functions and methods in Python are first class, meaning
    they can be used in expressions like any other type.
- 3. The __call__ special method enables instances of a class to be called
    like plain Python functions.
- 4. When you need a function to maintain state, consider defining a class
    that provides the __call__ method instead of defining a stateful closure
    (see Item 15: "Know how closures interact with variable scope").


### [Item 24: Use @classmethod polymorphism to construct objects generically](item_24_use_classmethod.py)
- 1. Python only supports a single constructor per class, the __init__ method.
- 2. Use @classmethod to define alternative constructors for your classes.
- 3. Use class method polymorphism to provide generic ways to build and
     connect concrete subclasses.


### [Item 25: Initialize parent classes with super](item_25_init_parent_classes_with_super.py)
- 1. Python's standard method resolution order (MRO) solves the problems to
    superclass initialization order and diamond inheritance.
- 2. Always use the super built-in function to initialize parent classes.


### [Item 26: Use multiple inheritance only for mix-in utility classes](item_26_when_use_multiple_inheritance.py)
- 1. Avoid using multiple inheritance if mix-in classes can achieve the same
    outcome.
- 2. Use pluggable behaviors at the instance level to provide per-class 
    customization when mix-in classes may require it.
- 3. Compose mix-ins to create complex functionality from simple behaviors.


### [Item 27: Prefer public attributes over private ones](item_27_prefer_public_attributes.py)
- 1. Private attributes aren't rigorously enforced by the Python compiler.
- 2. Plan from the beginning to allow subclass to do more with your internal
    APIs and attributes instead of locking them out by default.
- 3. Use documentation of protected fields to guide subclass instead of trying
    to force access control with private attributes.
- 4. Only consider using private attributes to avoid naming conflicts with
    subclasses that are out of your control.


### [Item 28: Inherit from collections.abc for custom container types](item_28_inherit_from_collections_abc.py)
- 1. Inherit directly from Python's container types (like list or dict) for
    simple use cases.
- 2. Beware of the large number of methods required to implement custom
    container types correctly.
- 3. Have your custom container types inherit from the interface defined in
    collections.abc to ensure that your classes match required interfaces
    and behaviors.


## Chapter 4: Metaclasses and Attributes


### [Item 29: Use plain attributes instead of get and set methods](item_29_use_plain_attributes.py)
- 1. Define new class interfaces using simple public attributes, and avoid set
     and get methods.
- 2. Use @property to define special behavior when attributes are accessed on
     your objects, if necessary.
- 3. Follow the rule of least surprise and void weird side effects in your
    @property methods.
- 4. Ensure that @property methods are fast; do slow or complex work using
    normal methods.


### [Item 30: Consider @property instead of refactoring attributes](item_30_consider_property.py)
- 1. Use @property to give existing instance attributes new functionality.
- 2. Make incremental progress toward better data models by using @property.
- 3. Consider refactoring a class and all call sites when you find yourself
     using @property too heavily.


### [Item 31: Use descriptors for reusable @property methods](item_31_use_descriptors.py)
- 1. Reuse the behavior and validation of @property methods by defining your
     own descriptor classes.
- 2. Use WeakKeyDictionary to ensure that your descriptor classes don't cause
     memory leaks.
- 3. Don't get bogged down trying to understand exactly how __getattribute__
     uses the descriptor protocol for getting and setting attributes.


### [Item_32_Use __getattr__, __getattribute__, and __setattr__ for lazy attributes](item_32_use_getattr.py)
- 1. Use __getattr__ and __setattr__ to lazily load and save attributes for an
     object.
- 2. Understand that __getattr__ only gets called once when accessing a
     missing attribute, whereas __getattribute__ gets called every time an
     attribute is accessed.
- 3. Avoid infinite recursion in __getattribute__ and __setattr__ by using
     methods from super() (i.e., the object class) to access instance
     attributes directly.


### [Item 33: Validate subclass with metaclass](item_33_validate_subclass.py)
- 1. Use metaclasses to ensure that subclass are well formed at the time they 
     are defined, before objects of their type are constructed.
- 2. Metaclass have slightly different syntax in Python 2 vs. Python 3.
- 3. The __new__ method of metaclasses is run after the class statement's
     entire body has been processed.


### [Item 34: Register class existence with metaclass](item_34_register_class_existence.py)
- 1. Class registration is a helpful pattern for building modular Python
     programs.
- 2. Metaclass let you run registration code automatically each time your
     base class is subclassed in a program.
- 3. Using metaclass for class registration avoids errors by ensuring that
     you never miss a registration call.


### [Item 35: Annotate class attributes with metaclass](item_35_annotate_class_attributes.py)
- 1. Metaclass enable you to modify a class's attributes before the class is
     fully defined.
- 2. Descriptors and metaclasses make a powerful combination for declarative
     behavior and runtime introspection.
- 3. You can avoid both memory leaks and the weakref module by using
     metaclasses along with descriptors.


## Chapter 5: Concurrency and parallelism


### [Item 36: use subprocess to manage child processes](item_36_use_subprocess.py)
- 1. Use the subprocess to run child processes and manage their input and
    output streams.
- 2. Child processes run in parallel with the Python interpreter, enabling you
    to maximize your CPU usage.
- 3. Use the timeout parameter with communicate to avoid deadlocks and hanging
    child processes.


### [Item 37: Use threads for blocking I/O, avoid for parallelism](item_37_use_threads.py)
- 1. Python threads can't bytecode in parallel on multiple CPU cores because
     of the global interpreter lock (GIL).
- 2. Python threads are still useful despite the GIL because they provide an
     easy way to do multiple things at seemingly the same time.
- 3. Use Python threads to make multiple system calls in parallel. This allows
     you to do blocking I/O at the same time as computation.


### [Item 38: Use lock to prevent data races in threads](item_38_use_lock.py)
- 1. Even though Python has a global interpreter lock, you're still
     responsible for protecting against objects without locks.
- 2. Your programs will corrupt their data structures if you allow multiple
     threads to modify the same objects without locks.
- 3. The lock class in the threading built-in module is Python's standard
     mutual exclusion lock implementation.


### [Item 39: Use queue to coordinate work between threads](item_39_use_queue.py)
- 1. Pipelines are a great way to organize sequences of work that run
     concurrently using multiple Python threads.
- 2. Be aware of the many problems in building concurrent pipelines: busy
     waiting, stopping workers, and memory explosion.
- 3. The Queue class has all of the facilities you need to build robust
     pipelines: blocking operations, buffer sizes, and joining.


### [Item 40: Consider coroutines to run many functions concurrently](item_40_consider_coroutines.py)
- 1. Coroutines provide an efficient way to run tens of thousands of functions
    seemingly at the same time.
- 2. Within a generator, the value of the yield expression will be whatever
    value was passed to the generator's send method from the exterior code.
- 3. Coroutines give you a powerful tool for separating the core logic of your
    program from its interaction with the surrounding environment.
- 4. Python 2 doesn't support yield from or returning values from generators.


### [Item 41: Consider concurrent.futures for true parallelism](item_41_consider+concurrent_futures.py)
- 1. Moving CPU bottlenecks to C-extension modules can be an effective way to
    improve performance while maximizing your investment in Python code.
    However, the cost of doing so is high and may introduce bugs.
- 2. The multiprocessing module provides powerful tools that can parallelize
    certain types of Python computation with minimal effort.
- 3. The power of multiprocessing is best accessed through the
    concurrent.futures built-in module and its simple ProcessPoolExecutor
    class.
- 4. The advanced parts of the multiprocessing module should be avoided
    because they are so complex.


## Chapter 6: Built-in Modules


### [Item 42: Define function decorators with functools.wraps](item_42_define_function_decorators.py)
- 1. Decorators are Python syntax for allowing one function to modify another
    function at runtime.
- 2. Using decorators can cause strange behaviors in tools that do
    introspection, such as debuggers.
- 3. Use the wraps decorator from the functools built-in module when you
    define your own decorators to avoid any issues.


### [Item 43: Consider contextlib and with statements for reusable try/finally behavior](item_43_consier_contextlib.py)
- 1. The with statement allows you to reuse logic from try/finally blocks and
    reduce visual noise.
- 2. The contextlib built-in module provides a contextmanager decorator that
    makes it easy to use your own functions in with statements.
- 3. The value yielded by context managers is supplied to the as part of the
    with statement. It's useful for letting your code directly access the
    cause of the special context.


### [Item 44: Make pickle reliable with copyreg](item_44_make_pickle_reliable.py)
- 1. The pickle built-in module is only useful for serializing and
    de-serializing objects between trusted programs.
- 2. The pickle module may break down when used for more than trivial use
    cases.
- 3. Use the copyreg built-in module with pickle to add missing attributes
    values, allow versioning of classes, and provide stable import paths.


### [Item 45: Use datetime instead of time for local clocks](item_45_use_date_time.py)
- 1. Avoid using the time module for translating between different time zones.
- 2. Use the datetime built-in module along with the pytz module to reliably
    convert between times in different time zones.
- 3. Always represent time in UTC and do conversations to local time as the
    final step before presentation.


### [Item 46: Use built-in algorithms and data structures](item_46_use_built_in_algorithm.py)
- 1. Use Python's built-in modules for algorithms and data structures.
- 2. Don't re-implement this functionality yourself. It's hard to get right.


### [Item 47: Use decimal when precision ia paramount](item_47_use_decimal.py)
- 1. Python has built-in types and classes in modules that can represent
    practically every type of numerical value.
- 2. The Decimal class is ideal for situations that require high precision and
    exact rounding behavior, such as computations of monetary values.


### [Item 48: Know where to find community built modules](item_48_communit_built_modules.py)
- 1. The Python Package Index (PyPI) contains a wealth of common packages
    that are built and maintained by the Python community.
- 2. pip is the command-line to use for installing packages from PyPI.
- 3. pip is installed by default in Python 3.4 and above; you must install it
    yourself for older versions.
- 4. The majority of PyPI modules are free and open source software.


## Chapter 7: Collaboration


### [Item 49: Write docstrings for every function, class and module](item_49_write_docstrings_4_everything.py)
- 1. Write documentation for every module, class and function using
    docstrings. Keep them up to date as your code changes.
- 2. For modules: introduce the contents of the module and any important
    classes or functions all users should know about.
- 3. For classes: document behavior, important attributes, and subclass
    behavior in the docstring following the class statement.
- 4. For functions and methods: document every argument, returned value,
    raised exception, and other behaviors in the docstring following the
    def statement.


### [Item 50: Use packages to organize modules and provide stable APIs](item_50_use_packages.py)
- 1. Packages in Python are modules that contain other modules. Packages allow
    you to organize your code into separate, non-conflicting namespaces with
    unique absolute module names.
- 2. Simple package are defined by adding an __init__.py file to a directory
    that contains other source files. These files become that child modules
    of the directory's package. Package directories may also contain other
    packages.
- 3. You can provide an explict API for a module by listing its publicly
    visible name in its __all__ special attribute.
- 4. You can hide a package's internal implementation by only importing public
    names in the package's __init__.py file or by naming internal-only
    members with a leading underscore.
- 5. When collaborating within a single team or on a single codebase, using
    __all__ for explicit APIs is probably unnecessary.


### [Item 51: Define a root exception to insulate callers from APIs](item_51_define_a_root_exception.py)
- 1. Defining root exceptions for your modules allows API consumers to
    insulate themselves from your API.
- 2. Catching root exceptions can help you find bugs in code that consumes an
    API.
- 3. Catching the Python Exception base class can help you find bugs in API
    implementations.
- 4. Intermediate root exceptions let you add more specific types of
    exceptions in the future without breaking your API consumers.


### [Item 52: Know how to break circular dependencies](item_52_break_circular_dependencies.py)
- 1. Circular dependencies happen when two modules must call into each other
    at import time. They can cause your program to crash at startup.
- 2. The best way to break a circular dependency is refactoring mutual
    dependencies into a separate module at the bottom of the dependency tree.
- 3. Dynamic imports are the simplest solution for breaking a circular
    dependency between modules while minimizing refactoring and complexity.


### [Item 53: Use virtual environments for isolated and reproducible dependencies](item_53_use_virtual_environments.py)
- 1. Virtual environment allow you to use pip to install many different
    versions of the same package on the same machine without conflicts.
- 2. Virtual environments are created with pyvenv, enabled with source
    bin/activate, and disabled with deactivate.
- 3. You can dump all of the requirements of an environment with pip freeze.
    You can reproduce the environment by supplying the requirements.txt file
    to pip install -r.
- 4. In versions of Python before 3.4, the pyvenv tool must be downloaded and
    installed separately. The command-line tool is called virtualenv instead
    of pyvenv.


## Chapter 8: Production


### [Item 54: Consider module-scoped code to configure deployment environments](item_54_consier_module_scoped_code.py)
- 1. Programs often need to run in multiple deployment environments that each
    have unique assumptions and configurations.
- 2. You can tailor a module's contents to different deployment environments
    by using normal Python statements in module scope.
- 3. Module contents can be the product of any external condition, including
    host introspection through the sys and os modules.


### [Item 55: Use repr strings for debugging output](item_55_use_repr_strings.py)
- 1. Calling print on built-in Python types will produce the human-readable
    string version of a value, which hides type information.
- 2. Calling repr on built-in Python types will produce the printable string
    version of a value. These repr strings could be passed to the eval
    built-in function to get back the original value.
- 3. %s in format strings will produce human-readable strings like str.%r will
    produce printable strings like repr.
- 4. You can define the __repr__ method to customize the printable
    representation of a class and provide more detailed debugging
    information.
- 5. You can reach into any object's __dict__ attribute to view its internals.


### [Item 56: Test everything with unittest](item_56_unittest.py)
- 1. The only way to have confidence in a Python program is to write tests.
- 2. The unittest built-in module provides most of the facilities you'll need
    to write good tests.
- 3. You can define tests by subclassing TestCase and defining one method per
    behavior you'd like to test. Test methods on TestCase classes must start
    with the word test.
- 4. It's important to write both unit tests (for isolated functionality) and
    integration tests (for modules that interact).


### [Item 57： Consider interactive debugging with pdb](item_57_pdb.py)
 1. You can initiate the Python interactive debugger at a point of interest
    directly in your program with the import pdb; pdb.set_trace() statements.
 2. The Python debugger prompt is a full Python shell that lets you inspect
    and modify the state of a running program.
 3. pdb shell commands let you precisely control program execution, allowing
    you to alternate between inspecting program state and progressing program
    execution.


### [item 58: Profile before optimizing](item_58_profile_before_optimizing.py)
- 1. It's import to profile Python programs before optimizing because the
    source of slowdowns is often obscure.
- 2. Use the cProfile module instead of the profile module because it provides
    more accurate profiling information.
- 3. The Profile object's runcall method provides everything you need to
    profile a tree of function calls in isolation.
- 4. The Stats object lets you select and print the subset of profiling
    information you need to see to understand your program's performance.

### [Item 59: Use tracemalloc to understand memory usage and leaks](item_59_use_tracemalloc.py)
- 1. It can be difficult to understand how Python programs use and leak
    memory.
- 2. The gc module can help you understand which objects exist, but it has no
    information about how they were allocated.
- 3. The tracemalloc built-in module provides powerful tools for understanding
    the source of memory usage.
- 4. tracemalloc is only available in Python 3.4 and above.
