# Item 35: Annotate class attributes with metaclass


# One more useful feature enable by metaclasses is the ability to modify or
# annotate properties after a class is defined but before the class is
# actually used. This approach is commonly used with descriptors (see Item 31:
# "Use descriptors for reuseable @property methods") to give them more
# introspection into how they're being used within their containing class.

# For example, say you want to define a new class that represents a row in
# your customer database. You'd like a corresponding property on the class
# for each column in the database table. To do this, here I define a
# descriptor class to connect attributes to column names.


class Field(object):
    def __init__(self, name):
        self.name = name
        self.internal_name = '_' + self.name

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name)

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


# With the column name stored in the Field descriptor, I can save all of the
# per-instance state directly in the instance dictionary as protected fields
# using the setattr and getattr built-in functions. At first, this seems to be
# much more convenient than building descriptors with weakref to avoid memory
# leaks.

# Defining the class representing a row requires supplying the column name for
# each class attribute.


class Customer(object):
    first_name = Field('first_name')
    last_name = Field('last_name')
    prefix = Field('prefix')
    suffix = Field('suffix')


# Using the class is simple. Here, you can see how the Field descriptors
# modify the instance dictionary __dict__ as expected:


foo = Customer()
# print('Before: ', repr(foo.first_name), foo.__dict__)
print('Before: ', foo.__dict__)
foo.first_name = 'Euclid'
print('After:  ', repr(foo.first_name), foo.__dict__)
# Before:  {}
# After:   'Euclid' {'_first_name': 'Euclid'}


# But it seems redundant. I already declared the name of the field when I
# assigned the constructed Field object to Customer.first_name in the class
# statement body. Why do I also have to pass the field name ('first_name' in
# this case) to the Field constructor?

# The problem is that the order of operations in the Customer class definition
# is the opposite of how it reads from left to right. First, the Field
# constructor is called as Field('first_name'). Then, the return value of that
# is assigned to Customer.field_name. There's no way for the Field to know
# upfront which class attribute it will be assigned to.

# To eliminate the redundancy, I can use a metaclass. Metaclasses let you hook
# the class statement directly and take action as soon as a class body is
# finished. In this case, I can use the metalcass to assign Field.name and
# Field.internal_name on the descriptor automatically instead of manually
# specifying the field name multiple times.


class Meta(type):
    def __new__(meta, name, bases, class_dict):
        for key, value in class_dict.items():
            if isinstance(value, Field):
                value.name = key
                value.internal_name = '_' + key
        cls = type.__new__(meta, name, bases, class_dict)
        return cls


# Here, I define a base class that uses the metaclass. All classes
# representing database rows should inherit from this class to ensure that
# they use the metaclass:


class DatabaseRow(object, metaclass=Meta):
    pass


# To work with the metaclass, the field descriptor is largely unchanged. The
# only difference is that it no longer requires any arguments to be passed to
# its constructor. Instead, its attributes are set by the Meta.__new__ method
# above.
#
class Field(object):
    def __init__(self):
        self.name = None
        self.internal_name = None

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name)

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


# By using the metaclass, the new DatabaseRow base class, and the new Field
# descriptor, the class definition for a database row no longer has the
# redundancy from before.


class BetterCustomer(DatabaseRow):
    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()


# The behavior of the new class is identical to the old one.


foo = BetterCustomer()
# print('Before: ', repr(foo.first_name), foo.__dict__)
print('Before: ', foo.__dict__)
foo.first_name = 'Euler'
print('After:  ', repr(foo.first_name), foo.__dict__)
# Before:  {}
# After:   'Euler' {'_first_name': 'Euler'}


# Things to remember

# 1. Metaclass enable you to modify a class's attributes before the class is
#     fully defined.
# 2. Descriptors and metaclasses make a powerful combination for declarative
#     behavior and runtime introspection.
# 3. You can avoid both memory leaks and the weakref module by using
#     metaclasses along with descriptors.
