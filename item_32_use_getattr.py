# Item_32_Use __getattr__, __getattribute__, and __setattr__ for lazy
# attributes

# Python's language hooks make it easy to write generic code for gluing
# systems together. For example, say you want to represent teh rows of your
# database as Python objects. Your database has its schema set. Your code
# that uses objects corresponding to those rows must also know what your
# database looks like. However, in Python, the code that connects your Python
# object to the database doesn't need to know the schema of your rows: it can
# be generic.

# How is that possible? Plain instance attributes, @property methods, and
# descriptors can't do this because they all need to be defined in advance.
# Python makes this dynamic behavior possible with the __getattr__ special
# method. If your class defines __getattr__, that method is called every time
# an attribute can't be found in an object's instance dictionary.


class LazyDB(object):
    def __init__(self):
        self.exists = 5

    def __getattr__(self, name):
        value = 'Value for %s' %  name
        setattr(self, name, value)
        return value


# Here, I access the missing property foo. This causes Python to call the
# __getattr__ method above, which mutates the instance dictionary __dict__.
data = LazyDB()
print('Before:', data.__dict__)
print('foo:   ', data.foo)
print('After: ', data.__dict__)
# Before: {'exists': 5}
# foo:    Value for foo
# After:  {'exists': 5, 'foo': 'Value for foo'}


# Here, I add logging to LazyDB to show when __getattr__ is actually called.
# Note that I use super().__getattr__() to get the real property value in
# order to avoid infinite recursion.


class LoggingLazyDB(LazyDB):
    # def __init__(self):
    #     super().__init__()

    def __getattr__(self, name):
        print('Called __getattr__(%s)' % name)
        return super().__getattr__(name)

data = LoggingLazyDB()
print('exists:', data.exists)
print('foo:   ', data.foo)
print('foo:   ', data.foo)
# exists: 5
# Called __getattr__(foo)
# foo:    Value for foo
# foo:    Value for foo


# The exists attribute is present in the instance dictionary, so __getattr__
# is never called for it. The foo attribute is not in the instance dictionary
# initially, so __getattr__ is called the first time. But the call to
# __getattr__ for foo also does a setattr, which populates foo in the instance
# dictionary. This is why the second time I access foo there isn't a call to
# __getattr__.

# This behavior is especially helpful for use cases like lazily accessing
# schemaless data. __getattr__ runs once to do the hard work of loading a
# property; all subsequent accesses retrieve the existing result.

# Say you also want transactions in this database system. The next time the
# user accesses a property, you want to know whether the corresponding row in
# the database is still valid and whether the transaction is still open. The
# __getattr__ hook won't let you do this reliably because it will use the
# object's instance dictionary as the fast path for existing attributes.

# To enable this use case, Python has another language hook call
# __getattribute__. This special method is called every time an attribute is
# accessed on an object, even in cases where it does exist in the attribute
# dictionary. This enables you to do things like check global transaction
# state on every property access. Here, I define ValidatingDB to log each time
# __getattribute__ is called:


class ValidatingDB(object):
    def __init__(self):
        self.exists = 5

    def __getattribute__(self, name):
        print('Called __getattribute__(%s)' % name)
        try:
            return super().__getattribute__(name)
        except AttributeError:
            value = 'Value for %s' % name
            setattr(self, name, value)
            return value

data = ValidatingDB()
print('exists:', data.exists)
print('foo:   ', data.foo)
print('foo:   ', data.foo)
# Called __getattribute__(exists)
# exists: 5
# Called __getattribute__(foo)
# foo:    Value for foo
# Called __getattribute__(foo)
# foo:    Value for foo


# In the event that a dynamically accessed property shouldn't exist, you can
# raise an AttributeError to cause Python's standard missing property behavior
# for both __getattr__ and __getattribute__.


class MissingPropertyDB(object):
    def __getattr__(self, name):
        if name == 'bad_name':
            raise AttributeError('%s is missing' % name)

data = MissingPropertyDB()
# data.bad_name
# AttributeError: bad_name is missing


# Python code implementing generic functionality often relies on the hasattr
# built-in function to determine when properties exist, and the getattr
# built-in function to retrieve property values. These functions also look in
# the instance dictionary for an attribute name before calling __getattr__.


data = LoggingLazyDB()
print('Before:     ', data.__dict__)
print('foo exists: ', hasattr(data, 'foo'))
print('After:      ', data.__dict__)
print('foo exists: ', hasattr(data, 'foo'))
# Before:      {'exists': 5}
# Called __getattr__(foo)
# foo exists:  True
# After:       {'foo': 'Value for foo', 'exists': 5}
# foo exists:  True


# In the example above, __getattr__ is only called once. In contrast, classes
# that implement __getattribute__ will have that method called each time
# hasattr or getattr is run on an object.
data = ValidatingDB()
print('foo exists: ', hasattr(data, 'foo'))
print('foo exists: ', hasattr(data, 'foo'))
# Called __getattribute__(foo)
# foo exists:  True
# Called __getattribute__(foo)
# foo exists:  True

# Now, say you want to lazily push data back to the database when values are
# assigned to your Python object. You can do this with __setattr__, a similar
# to language hook that lets you intercept arbitrary attribute assignments.
# Unlike retrieving an attribute with __getattr__ and __getattribute__,
# there's no need for two separate methods. The __setattr__ method is always
# called every time an attribute is assigned on an instance (either directly
# or through the setattr built-in function).


class SavingDB(object):
    def __setattr__(self, name, value):
        '''Save some data to the DB log'''
        super().__setattr__(name, value)


# Here, I define a logging subclass of SavingDB. Its __setattr__ method is
# always called on each attribute assignment:


class LoggingSavingDB(SavingDB):
    def __setattr__(self, name, value):
        print('Called __setattr__(%s, %r)' % (name, value))
        super().__setattr__(name, value)

data = LoggingSavingDB()
print('Before: ', data.__dict__)
data.foo = 5
print('After:  ', data.__dict__)
data.foo = 7
print('Finally:', data.__dict__)
# Before:  {}
# Called __setattr__(foo, 5)
# After:   {'foo': 5}
# Called __setattr__(foo, 7)
# Finally: {'foo': 7}


# The problem with __getattribute__ and __setattr__ is that they're called on
# every attribute access for an object, even when you many not want to happen.
# For example, say you want attribute accesses on your object to actually look
# up keys in an associated dictionary.


class BrokenDictionaryDB(object):
    def __init__(self, data):
        self._data = {}

    def __getattribute__(self, name):
        print('Called __getattribute__(%s)' % name)
        return self._data[name]


# This requires accessing self._data from the __getatribute__ method.
# However, if you actually try to do that, Python will recurse until it
# reaches its stack limit, and then it'll die.


data = BrokenDictionaryDB({'foo': 3})
# data.foo


# The problem is that __getattribute__ access self._data, which causes
# __getattribute__ to run again, which access self._data again, and so on.
# The solution is to use the super().__getattribute__ method on your instance
# to fetch values from the instance attribute dictionary. This avoids the
# recursion.


class DictionaryDB(object):
    def __init__(self, data):
        self._data = data

    def __getattribute__(self, name):
        data_dict = super().__getattribute__('_data')
        return data_dict[name]

data = DictionaryDB({'foo': 3})
print('foo: ', data.foo)
# foo:  3


# Similarly, you'll need __setattr__ methods that modify attributes on an
# object to use super().__setattr__.


# Things to remember

# 1. Use __getattr__ and __setattr__ to lazily load and save attributes for an
#     object.
# 2. Understand that __getattr__ only gets called once when accessing a
#     missing attribute, whereas __getattribute__ gets called every time an
#     attribute is accessed.
# 3. Avoid infinite recursion in __getattribute__ and __setattr__ by using
#     methods from super() (i.e., the object class) to access instance
#     attributes directly.
