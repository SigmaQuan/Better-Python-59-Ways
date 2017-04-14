# Item 34: Register class existence with metaclass
import json


# Another common use of metaclass is to automatically register types in your
# program. Registration is useful for doing reverse lookups, where you need to
# map a simple identifier back to a corresponding class.

# For example, say you want to implement your own serialized representation of
# a Python object using JSON. You need a way to take an object and turn it
# into a JSON string. Here, I do this generically by defining a base class
# that records the constructor parameters and turns them into a JSON
# dictionary.


class Serializable(object):
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({'args': self.args})


# This class makes it easy to serialize simple, immutable data structures like
# Point2D to a string.


class Point2D(Serializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point2D(%d, %d)' % (self.x, self.y)


point = Point2D(5, 3)
print('Object:    ', point)
print('Serialized:', point.serialize())
# Object:     Point2D(5, 3)
# Serialized: {"args": [5, 3]}


# Now, I need to deserialized this JSON string and construct the Point2D
# object it represents. Here, I define another class that can deserialize
# the data from its Serializable parent class:


class Deserializable(Serializable):
    @classmethod
    def deserialize(cls, json_data):
        params = json.loads(json_data)
        return cls(*params['args'])


# Using Deserizlizable makes it easy to serialize and deserialize simple,
# immutable objects in a generic way.


class BetterPoint2D(Deserializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point2D(%d, %d)' % (self.x, self.y)


point = BetterPoint2D(5, 3)
print('Before:     ', point)
data = point.serialize()
print('Serialized: ', data)
after = BetterPoint2D.deserialize(data)
print('After:      ', after)
# Before:      Point2D(5, 3)
# Serialized:  {"args": [5, 3]}
# After:       Point2D(5, 3)


# The problem with this approach is that it only works if you know the
# intended type of the serialized data ahead of time (e.g., Point2D,
# BetterPoint2D). Ideally, you'd have a large number classes serializing to
# JSON and one common function that could deserialize any of them back to a
# corresponding Python object.

# To do this, I include the serialized object's class name in the JSON data.


class BetterSerializable(object):
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args': self.args
        })

    def __repr__(self):
        return 'Point2D(%d, %d)' % (self.x, self.y)


# Then, I can maintain a mapping of class names back to constructors for those
# objects. The general deserialize function will work for any class passed to
# register_class.


registry = {}


def register_class(target_class):
    registry[target_class.__name__] = target_class


def deserialize(data):
    params = json.loads(data)
    name = params['class']
    target_class = registry[name]
    return target_class(*params['args'])


# To ensure that deserialize always works properly, I must call register_class
# for every class I want to deserialize in the future.


class EvenBetterPoint2D(BetterSerializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return 'EvenBetterPoint2D(%d, %d)' % (self.x, self.y)


register_class(EvenBetterPoint2D)


# Now, I can deserialize an arbitrary JSON string without having to know which
# class it contains.


point = EvenBetterPoint2D(5, 3)
print('Before:     ', point)
data = point.serialize()
print('Serialized: ', data)
after = deserialize(data)
print('After:      ', after)
# Before:      EvenBetterPoint2D(5, 3)
# Serialized:  {"class": "EvenBetterPoint2D", "args": [5, 3]}
# After:       EvenBetterPoint2D(5, 3)


# The problem with this approach is that you can forget to call
# register_class.


class Point3D(BetterSerializable):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return 'Point3D(%d, %d, %d)' % (self.x, self.y, self.z)

# Forgot to call register_class! Whoops!


# This will cause your code to break at runtime, when you finally try to
# deserialize an object of a class you forgot to register.


point = Point3D(5, 9, -4)
data = point.serialize()
# deserialize(data)
# KeyError: 'Point3D'


# Even though you chose to subclass BetterSerializable, you won't actually get
# all of its features if you forget to call register_class after your class
# statement body. This approach is error prone and especially challenging for
# beginners. The same omission can happen with class decorators in Python 3.

# What if you could somehow act on the programmer's intent to use
# BetterSerialized and ensure that register_class is called in all cases?
# Metaclasses enable this by intercepting the class statement when subclasses
# are defined (see Item 33: "Validate subclasses with Metaclass"). This lets
# you register the new type immediately after the class's body.


class Meta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        register_class(cls)
        return cls


class RegisteredSerializable(BetterSerializable, metaclass=Meta):
    pass


# When I define a subclass of RegisteredSerializable, I can be confident that
# the call to register_class happened and deserialize will always work as
# expected.


class Vector3D(RegisteredSerializable):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x, self.y, self.z = x, y, z

    def __repr__(self):
        return 'Vector3D(%d, %d, %d)' % (self.x, self.y, self.z)


v3 = Vector3D(10, -7, 3)
print('Before:     ', v3)
data = v3.serialize()
print('Serialized: ', data)
after = deserialize(data)
print('After:      ', after)
# Before:      Vector3D(10, -7, 3)
# Serialized:  {"class": "Vector3D", "args": [10, -7, 3]}
# After:       Vector3D(10, -7, 3)

# Using metaclass for class registration ensures that you'll never miss a
# class as long as the inheritance tree is right. This works well for
# serialization, as I've shown, and also applies to database
# object-relationship mappings (ORMs), plug-in systems, and system hooks.


# Things to remember

# 1. Class registration is a helpful pattern for building modular Python
#     programs.
# 2. Metaclass let you run registration code automatically each time your
#     base class is subclassed in a program.
# 3. Using metaclass for class registration avoids errors by ensuring that
#     you never miss a registration call.
