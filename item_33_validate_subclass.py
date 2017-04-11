# Item 33: Validate subclass with metaclass


# One of simplest applications of metaclass is verifying that a class was
# defined correctly. When you're building a complex class hierarchy, you may
# want to enforce style, require overriding methods, or have strict
# relationships between class attributes. Metaclass enable these use cases by
# providing a reliable way to run your validation code each time a new
# subclass is defined.

# Often a class's validation code runs in the __init__ method, when an object
# of the class's type is constructed (see Item 28: "inherit from
# collections.abc for custom container types" for an example). Using metaclass
# for validation can raise errors much earlier.

# Before I get into how to define a metaclass for validating subclasses, it's
# important to understand the metaclass action for standard objects. A
# metaclass is defined by inheriting from type. In the default case, a
# metaclass receives the contents of associated class statements in its
# __new__ method. Here, you can modify the class information before the type
# is actually constructed:


class Meta(type):
    def __new__(meta, name, bases, class_dict):
        print((meta, name, bases, class_dict))
        return type.__new__(meta, name, bases, class_dict)


class MyClass(object, metaclass=Meta):
    stuff = 123

    def foo(self):
        pass


# (<class '__main__.Meta'>,
# 'MyClass',
# (<class 'object'>,),
# {'stuff': 123,
# 'foo': <function MyClass.foo at 0x7fe21e0b5d08>,
# '__qualname__': 'MyClass',
# '__module__': '__main__'})


# The metaclass has access to the name of the class, the parent classes it
# inherits from, and all of the class attributes that were defined in the
# class's body.


# Python 2 has slightly different syntax and specifies a metaclass using the
# __metaclass__ class attribute. The Meta.__new__ interface is the same.


# Python 2
# class Meta(type):
#     def __new__(meta, name, bases, class_dict):
#         print((meta, name, bases, class_dict))
#         return type.__new__(meta, name, bases, class_dict)
#
#
# class MyClassInPython2(object):
#     __metaclass__ = Meta
#     stuff = 123
#
#     def foo(self):
#         pass


# (<class '__main__.Meta'>,
# 'MyClassInPython2',
# (<type 'object'>,),
# {'__module__': '__main__',
#  'stuff': 123,
#  '__metaclass__': <class '__main__.Meta'>,
# 'foo': <function foo at 0x7fab81b7cde8>})


# You can add functionality to the Meta.__new__ method in order to validate
# all the parameters of a class before it's defined. For example, say you want
# to represent any type of multi-sided polygon. You can do this by defining a
# special validating metaclass and using it in the base class of your polygon
# class hierarchy. Note that it's important not to apply the same validation
# to the base class.


class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        '''Don't validate the abstract Polygon class'''
        if bases != (object,):
            if class_dict['sides'] < 3:
                raise ValueError('Polygons need 3+ sides')
        return type.__new__(meta, name, bases, class_dict)


class Polygon(object, metaclass=ValidatePolygon):
    sides = None  # Specified by subclass

    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180


class Triangle(Polygon):
    sides = 3


# If you try to define a polygon with fewer that three sides, the validation
# will cause the class statement to fail immediately after the class statement
# body. This means your program will not even be able to start running when
# you define such a class.


print('Before class')


class Line(Polygon):
    print('Before side')
    sides = 1
    print('After side')
print('After class')
# Before class
# Before side
# ValueError: Polygons need 3+ sides


# Things to remember

# 1. Use metaclasses to ensure that subclass are well formed at the time they
#     are defined, before objects of their type are constructed.
# 2. Metaclass have slightly different syntax in Python 2 vs. Python 3.
# 3. The __new__ method of metaclasses is run after the class statement's
#     entire body has been processed.


