# Item 31: Use descriptors for reusable @property methods
import weakref


# The big problem with the @property built-in (see Item 29: Use plain
# attributes instead of get and set methods and Item 30: consider @property
# instead of refactoring attributes) is reuse. The methods it decorates can't
# be reused for multiple attributes of the same class. The also can't be
# reused by unrelated classes.

# For example, say you want a class to validate that the grade received by a
# student on a homework assignment is a percentage.


class Homework(object):
    def __init__(self):
        self._grade = 0

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._grade = value


# Using an @property makes this class easy to use.


galileo = Homework()
# galileo.grade = 101
# ValueError: Grade must be between 0 and 100
galileo.grade = 95
# print(galileo.grade)
# 95


# Say you also want to give the student a grade for an example, where the
# exam has multiple subjects, each with a separate grade.


class Exam(object):
    def __init__(self):
        self._writing_grade = 0
        self._math_grade = 0

    @staticmethod
    def _check_grade(value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
# This quickly gets tedious. Each section of the exam requires adding a new
# @property and related validation.from.

    @property
    def writing_grade(self):
        return self._writing_grade

    @writing_grade.setter
    def writing_grade(self, value):
        self._check_grade(value)
        self._writing_grade = value

    @property
    def math_grade(self):
        return self._math_grade

    @math_grade.setter
    def math_grade(self, value):
        self._check_grade(value)
        self._math_grade = value


# Also, this approach is not general. If you want to reuse this percentage
# validation beyond homework and exams, You'd need to write the @property
# boilerplate and _check_grade repeatedly.

# The better way to do this in Python is to use a descriptor. The descriptor
# protocol defines how attribute access is interpreted by the language. A
# descriptor class can provide __get__ and __set__ methods that let you reuse
# the grade validation behavior without any boilerplate. For this purpose,
# descriptor are also better than mix-ins (see Item 26: Use multiple
# inheritance only for mix-in utility classes) because they let you reuse the
# same logic for many different attributes in a single class.


# Here, I define a new class called Exam with class attributes that are Grade
# instances. The Grade class implements the descriptor protocol. Before I
# explain how the Grade class works, it's important to understand what Python
# will do when your code accesses such descriptor attributes on an Exam
# instance.

#
# class Grade(object):
#     def __get__(*args, **kwargs):
#         # super().__getattribute__(*args, **kwargs)
#
#     def __set__(*args, **kwargs):
#         # super().__setattr__(args, kwargs)
#
#
# class Exam(object):
#     math_grade = Grade()
#     writing_grade = Grade()
#     science_grade = Grade()
#
#
# # When you assign a property:
# exam = Exam()
# exam.writing_grade = 40
#
# # it will be interpreted as:
# Exam.__dict__['writing_grade'].__set__(exam, 4)
#
# # When you retrieve a property:
# print(exam.writing_grade)
#
# # it will be interpreted as:
# print(Exam.__dict__['writing_grade'].__get__(exam, Exam))


# What drives this behavior is the __getattribute__ method of object (see Item
# 32: "Use __getattr__, __getattribute__, and __setattr__ for lazy
# attributes"). In short, when an Exam instance doesn't have an attribute
# named writing_grade, Python will fall back to the Exam class's attribute
# instead. If this class attribute is an object that has __get__ and __set__
# methods, Python will assume you want to follow the descriptor protocol.

# Knowing this behavior and how I used @property for grade validation in the
# Homework class, here's reasonable first attempt at implementing the Grade
# descriptor.

#
# class Grade(object):
#     def __init__(self):
#         self._value = 0
#
#     def __get__(self, instance, owner):
#         return self._value
#
#     def __set__(self, instance, value):
#         if not (0 <= value <= 100):
#             raise ValueError('Grade must be between 0 and 100')
#         self._value = value
#
#
# class Exam(object):
#     math_grade = Grade()
#     writing_grade = Grade()
#     science_grade = Grade()
#
#
# # Unfortunately, this is wrong and will result in broken behavior. Accessing
# # multiple attributes on a single Exam instance works as expected.
# first_exam = Exam()
# first_exam.writing_grade = 82
# first_exam.science_grade = 99
# print('Writing', first_exam.writing_grade)
# print('Science', first_exam.science_grade)
# # Writing 82
# # Science 99
#
#
# # But accessing these attributes on multiple Exam instances will have
# # unexpected behavior.
# second_exam = Exam()
# second_exam.writing_grade = 75
# print('Second', second_exam.writing_grade, 'is right')
# print('First', first_exam.writing_grade, 'is wrong')
# # Second 75 is right
# # First 75 is wrong


# The problem is that a single Grade instance is shared across all Exam
# instances for the class attribute writing_grade. The Grade instance for
# this attribute is constructed once in the program lifetime when the Exam
# class is first defined, not each time an Exam instance is created.

# To solve this, I need the Grade class to keep track of its value for each
# unique Exam instance. I can do this by saving the per-instance state in a
# dictionary.

class Grade(object):
    def __int__(self):
        self._values = {}
        # self._values = weakref.WeakKeyDictionary()

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        # if not (0 <= value <= 100):
        #     raise ValueError('Grade must be between 0 and 100')
        # self._values.set(instance, value)  # [instance] = value
        # self._values[instance] = value
        self._values[instance] = value


# This implementation is simple and works well, but there's still one gotcha:
# It leaks memory. The _values dictionary will hold a reference to every
# instance of Exam ever passed to __set__ over the lifetime of the program.
# This causes instances to never have their reference count go to zero,
# preventing cleanup by the garbage collector.

# To fix this, I can use Python's weakref built-in module. This module
# provides a special class called WeakKeyDictionary that can take the place
# of WeakKeyDictionary is that it will remove Exam instance from its set of
# keys when the runtime knows it's holding the instance's last remaining
# reference in the program. Python will do the bookkeeping for you and ensure
# that the _values dictionary will be empty when all Exam instances are no
# longer in use.

# class Grade(object):
#     def __int__(self):
#         self._values = weakref.WeakKeyDictionary()

# Using this implementation of the Grade descriptor, everything works as
# expected.


class Exam(object):
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()


first_exam = Exam()
first_exam.writing_grade = 82
second_exam = Exam()
second_exam.writing_grade = 75
print('First ', first_exam.writing_grade, 'is right')
print('Second', second_exam.writing_grade, 'is right')
# TODO: there is a bug:
# AttributeError: 'Grade' object has no attribute '_values'


# Things to remember

# 1. Reuse the behavior and validation of @property methods by defining your
#     own descriptor classes.
# 2. Use WeakKeyDictionary to ensure that your descriptor classes don't cause
#     memory leaks.
# 3. Don't get bogged down trying to understand exactly how __getattribute__
#     uses the descriptor protocol for getting and setting attributes.
