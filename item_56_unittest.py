# Item 56: Test everything with unittest
from unittest import TestCase, main
from item_56_utils import to_str


# Python doesn't have static type checking. There's nothing int eh compiler
# that ensure your program will work when you run it. With Python you don't
# know whether the functions your program calls will be defined at runtime,
# even when their existence is evident in the source code. This dynamic
# behavior is a blessing and a curse.

# The large numbers of Python programmers out there say it's worth it because
# of the productivity gained from the resulting brevity and simplicity. But
# most people have heard at least one horror story about Python in which a
# program encountered a boneheaded error at run time.

# One of the worst examples I've heard is when a SyntaxError was raised in
# production as a side effect of a dynamic import (see Item 52: "Know how to
# break circular dependencies"). The programmer I know who was hit by this
# surprising occurrence has since ruled out using Python ever again.

# But I have to wonder, why wasn't the code tested before the program was
# deployed to production? Type safety isn't everything. You should always test
# your code, regardless of what language it's written in. However, I'll admit
# that the big difference between Python and many other languages is that the
# only way to have any confidence in a Python program is by writing tests.
# There is no veil of static type checking to make you feel safe.

# Luckily, the same dynamic features that prevent static type checking in
# Python also make it extremely easy to write test for your code. You can use
# Python's dynamic nature and easily overridable behaviors to implement tests
# and ensure that your programs work as expected.

# You should think of tests as an insurance policy on your code. Good tests
# give you confidence that your code is correct. If you refactor or expand
# your code, tests make it easy to identify how behaviors have changed. It
# sounds counter-intuitive, but having good tests actually makes it easier to
# modify Python code, not harder.

# The simplest way to write tests is to use the unittest built-in module. For
# example, say you have the following utility function defined in utils.py


def to_str(data):
    if isinstance(data, str):
        return data
    elif isinstance(data, bytes):
        return data.decode('utf-8')
    else:
        raise TypeError('Must supply str or bytes, '
                        'found: %r' % data)


# To define tests, I create a second file named test_utils.py or utils_test.py


class UtilsTestCase(TestCase):
    def test_to_str_bytes(self):
        self.assertEqual('hello', to_str(b'hello'))

    def test_to_str_str(self):
        self.assertEqual('hello', to_str('hello'))

    def test_to_str_bad(self):
        self.assertRaises(TypeError, to_str, object())


if __name__ == '__main__':
    main()


# Tests are organized into TestCase classes. Each test is a method beginning
# with the word test. If a test method runs without raising any kind of
# Exception (including AssertionError from assert statements), then the test
# is considered to have passed successfully.

# The TestCase class provides helper methods for making assertions in your
# tests, such as assertEqual for verifying equality, assertTrue for verifying
# that exceptions are raised when appropriate (see help (TestCase) for more).
# You can define your own helper methods in TestCase subclasses to make your
# tests more readable; just ensure that your method names don't begin with
# the word test.

# Note
# Another common practice when writing test is to use mock functions and
# classes to stub out certain behaviors. For this purpose, Python 3 provides
# the unittest.mock built-in module, which is available for Python 2 as an
# open source package.

# Sometimes, your TestCase classes need to set up the test environment before
# running test methods. To do this, you can override the setUp and tearDown
# methods. These methods are called before and after each test method,
# respectively, and they let you ensure that each test runs in isolation (an
# important best practice of proper testing). For example, here I define a
# TestCase that creates a temporary directory before each test and deletes its
# contents after each test finishes:


class MyTest(TestCase):
    def setUp(self):
        self.test_dir = TemporaryDirectory()

    def tearDown(self):
        self.test_dir.cleanup()
    #
    # def test_to_str_bytes(self):
    #     self.assertEqual('hello', to_str(b'hello'))
    #
    # def test_to_str_str(self):
    #     self.assertEqual('hello', to_str('hello'))
    #
    # def test_to_str_bad(self):
    #     self.assertRaises(TypeError, to_str, object())

# I usually define one TestCase for each set of related tests. Sometimes I
# have one TestCase for each function that has many edge cases. Other times,
# a TestCase spans all functions in a single module. I'll also create one
# TestCase for testing a single class and all of its methods.

# When programs get complicated, you'll want additional test for verifying
# the interactions between your modules, instead of only testing code in
# isolation. This is the difference between unit tests and integration tests.
# In Python, it's important to write both types of test for exactly the same
# reason: You have no guarantee that your modules will actually work together
# unless you prove it.

# Note
# Depending on your project, it can also be useful to define data-driven tests
# or organize test into different suites of related functionality. For these
# purpose, code coverage reports, and other advanced use cases, the nose
# (http://nose.readthedocs.org/) and pytest (http://pytest.org/) open source
# packages can be especially helpful.


# Things to remember

# 1. The only way to have confidence in a Python program is to write tests.
# 2. The unittest built-in module provides most of the facilities you'll need
#    to write good tests.
# 3. You can define tests by subclassing TestCase and defining one method per
#    behavior you'd like to test. Test methods on TestCase classes must start
#    with the word test.
# 4. It's important to write both unit tests (for isolated functionality) and
#    integration tests (for modules that interact).
