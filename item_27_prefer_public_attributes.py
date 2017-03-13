# Item 27: Prefer public attributes over private ones


# In Python, there are only two types of attribute visibility for a class's
# attributes: public and private.


class MyObject(object):
    def __init__(self):
        self.public_field = 5
        self.__private_field = 10

    def get_private_field(self):
        return self.__private_field


# Public attributes can be accessed by anyone using the dot operator on the
# object.


foo = MyObject()
assert foo.public_field == 5


# Private field are specified by prefixing an attribute's name with a double
# underscore. They can be assessed directly by methods of the containing
# class.


assert foo.get_private_field() == 10


# Directly accessing private fields from outside the class raises an exception.


# foo.__private_field
# line 36, in <module>
#     foo.__private_field
# AttributeError: 'MyObject' object has no attribute '__private_field'


# Class methods also have access to private attributes because they are
# declared within the surrounding class block.


class MyOtherObject(object):
    def __init__(self):
        self.__private_field = 71

    @classmethod
    def get_private_field_of_instance(cls, instance):
        return instance.__private_field


bar = MyOtherObject()
assert MyOtherObject.get_private_field_of_instance(bar) == 71


# As you'd expect with private fields, a subclass can't access its parent
# class's private fields.


class MyParentObject(object):
    def __init__(self):
        self.__private_field = 71


class MyChildObject(MyParentObject):
    def get_private_field(self):
        return self.__private_field


baz = MyChildObject()
# baz.get_private_field()
# line 74, in <module>
#     baz.get_private_field()
# line 70, in get_private_field
#     return self.__private_field
# AttributeError: 'MyChildObject' object has no attribute '_MyChildObject__private_field'


# The private attribute behavior is implemented with a simple transformation
# of the attribute name. When the Python compiler sees private attribute
# access in methods like MyChildObject.get_private_field, it translate
# __private_field to access _MyChildObject__private_field instead. In this
# example, __private_field was only defined in MyParentObject.__init__,
# meaning the private attribute's real name is _MyParentObject__private_field.
# Accessing the parent's private attribute from the child class fails simply
# because teh transformed attribute name doesn't match.

# Knowing this scheme, you can easily access the private attributes of any
# class, from a subclass or externally, without asking for permission.


assert baz._MyParentObject__private_field == 71
# print(baz._MyParentObject__private_field)


# If you look in the object's attribute dictionary, you'll see that private
# attributes are actually stored with the names as they appear after the
# transformation.


print(baz.__dict__)
# {'_MyParentObject__private_field': 71}


# Why doesn't the syntax for private attributes actually enforce strict
# visibility? The simplest answer is one often-quoted motto of Python:
# "We are all consenting adults here." Python programmers believe that the
# benefits of being open outweigh the downsides of being closed.
"""
Nothing is really private in python. No class or class instance can keep you
away from all what's inside (this makes introspection possible and powerful).
Python trusts you. It says "hey, if you want to go poking around in dark
places, I'm gonna trust that you've got a good reason and you're not making
trouble." After all, we're all consenting adults here.
"""

# Beyond that, having the ability to hook language features like attribute
# access (see Item 32: "Use __getattr__, __getattribute__, and __setattr__ for
# lazy attributes") enables you to mess around with the internals of objects
# whenever you wish. If you can do that, what is the value of Python trying to
# prevent private attribute access otherwise?

# To minimize the damage of accessing internals unknowingly, Python
# programmers follow a naming convention defined in the style guide (see
# Item 2: "Follow the PEP 8 style guide"). Fields prefixed by a single
# underscore (like _protected_field) are protected, meaning external users of
# the class should proceed with caution.

# However, many programmers who are new to Python use private fields to
# indicate an internal API that shouldn't be accessed by subclasses or
# externally.


class MyClass(object):
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return str(self.__value)


foo = MyClass(5)
assert foo.get_value() == '5'
print(foo.get_value())


# But if the class hierarchy changes beneath you, these classes will break
# because the private references are no longer valid. Here, the
# MyIntegerSubclass class's immediate parent, MyClass, has had another parent
# class added called MyBaseClass:


class MyBaseClass(object):
    def __init__(self, value):
        self.__value = value


class MyClass(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)


class MyIntegerSubclass(MyClass):
    def get_value(self):
        return int(self._MyClass__value)


# The __value attribute is now assigned in the MyBaseClass parent class, not
# the MyClass parent. That causes the private variable reference
# self._MyClass__value to break in MyIntegerSubclass.


foo = MyIntegerSubclass(5)
# foo.get_value()
# line 170, in <module>
#     foo.get_value()
#  line 162, in get_value
#     return int(self._MyClass__value)
# AttributeError: 'MyIntegerSubclass' object has no attribute '_MyClass__value'


# In general, it's better to err on the side of allowing subclasses to do
# more by using protected attributes. Document each protected field and
# explain which are internal APIs available to subclasses and which should be
# left alone entirely. This is as much advice to other programmers as it is
# guidance for your future self on how to extend your own code safely.


class MyClass(object):
    def __init__(self, value):
        """
        This stores the user-supplied value for the object.
        It should be coercible to a string. Once assigned for
        the object it should be treated as immutable.
        :param value:
        """
        self._value = value


# You only time to seriously consider using private attributes is when your're
# worried about naming conflicts with subclasses. This problem occurs when a
# child class unwittingly defines an attribute that was already defined by its
# parent class.


class ApiClass(object):
    def __init__(self):
        self._value = 5

    def get(self):
        return self._value


class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello'  # Conflicts

a = Child()
print(a.get(), 'and', a._value, 'should be different')
# hello and hello should be different


# This is primarily a concern with classes that are part of a public API; the
# subclasses are out of your control, so you can't refactor to fix the
# problem. Such a conflict is especially possible with attribute names that
# are very common (like value). To reduce the risk of this happening, you can
# use a private attribute in the parent class to ensure that there are no
# attribute names that overlap with child classes.


class ApiClass(object):
    def __init__(self):
        self.__value = 5

    def get(self):
        return self.__value


class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello'  # Ok

a = Child()
print(a.get(), 'and', a._value, 'should be different')
# 5 and hello should be different


# Things to remember

# 1. Private attributes aren't rigorously enforced by the Python compiler.
# 2. Plan from the beginning to allow subclass to do more with your internal
#    APIs and attributes instead of locking them out by default.
# 3. Use documentation of protected fields to guide subclass instead of trying
#    to force access control with private attributes.
# 4. Only consider using private attributes to avoid naming conflicts with
#    subclasses that are out of your control.
