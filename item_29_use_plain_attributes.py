# Chapter 4: Metaclasses and Attributes


# Metaclasses are often mentioned in lists of Python's features, but few
# understand what they accomplish in practice. The name metaclass vaguely
# implies a concept above and beyond a class. Simply but, metaclasses let you
# intercept Python's class statement and provide special behavior each time a
# class is defined.


# Similarly mysterious and powerful are Python's built-in features for
# dynamically customizing attribute accesses. Along with Python's
# object-oriented constructs, these facilities provide wonderful tools to ease
# the transition from simple classes to complex ones.


# However, with these powers come many pitfalls. Dynamic attributes enable you
# to override objects and cause unexpected side effects. Metaclasses can
# create extremely bizarre behaviors that are unapproachable to newcomers. It's
# important that you follow the rule of least surprise and only use these
# mechanisms to implement well understood idioms.


# Item 29: Use plain attributes instead of get and set methods


# Programmers coming to Python from other languages may naturally try to
# implement explicit getter and setter methods in their classes.


class OldDResistor(object):
    def __init__(self, ohms):
        self._ohms = ohms

    def get_ohms(self):
        return self._ohms

    def set_ohms(self, ohms):
        self._ohms = ohms


# Using these setters and getters is simple, but it's not Pythonic.


r0 = OldDResistor(50e3)
print('Before: %5r' % r0.get_ohms())
r0.set_ohms(10e3)
print('After:  %5r' % r0.get_ohms())
# Before: 50000.0
# After:  10000.0


# Such methods are especially clumsy for operations like incrementing in
# place.


r0.set_ohms(r0.get_ohms() + 5e3)
print('Add 5e3: %5r' % r0.get_ohms())
# Add 5e3: 15000.0


# These utility methods do help define the interface for your class, making it
# easier to encapsulate functionality, validate usage, and define boundaries.
# Those are important goals when designing a class to ensure  you don't break
# callers as your class evolves over time.

# In Python, however, you almost never need to implement explicit setter or
# getter methods. Instead, you should always start your implementations with
# simple public attributes.


class Resistor(object):
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0

r1 = Resistor(50e3)
print('Before: %5r' % r1.ohms)
# These make operations like incrementing in place natural and clear.
r1.ohms = 10e3
print('After:  %5r' % r1.ohms)
r1.ohms += 5e3
print('Add 5e3: %5r' % r1.ohms)
# Before: 50000.0
# After:  10000.0
# Add 5e3: 15000.0


# Later, if you decide you need special behavior when an attribute is set, you
# can migrate to the @property decorator and its corresponding setter
# attribute. Here, I define a new subclass of Resistor that lets me vary the
# current by assigning the voltage property. Note that in order to work
# properly the name of both the setter and getter methods mush match the
# intended property name.


class VoltageResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0


    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms


# Now, assigning the voltage property will run the voltage setter method,
# updating the current property of the object to match.


r2 = VoltageResistance(1e3)
print('Before: %5r amps' % r2.current)
r2.voltage = 10
print('After:  %5r amps' % r2.current)
# Before:     0 amps
# After:   0.01 amps


# Specifying a setter on a property also lets you perform type checking and
# validation on values passed to your class. Here, I define a class that
# ensures all resistance values are above zero ohms:


class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError('%f ohms mush be > 0' % ohms)
        self._ohms = ohms


# Assigning an invalid resistance to the attribute raises an excpetion.


r3 = BoundedResistance(1e3)
# r3.ohms = 0
# ValueError: 0.000000 ohms mush be > 0


# An exception will also be raise if you pass an invalid value to the
# constructor.


# BoundedResistance(-5)
# ValueError: -5.000000 ohms mush be > 0


# This happens because BoundedResistance.__init__ calls Resistorl.__init__,
# which assigns self.ohms = -5. That assignment causes the @ohms.setter method
# from BoundedResistance to be called, immediately running the validation code
# before object construction has completed.

# You can even use @property to make attributes from parent classes immutable.


class FixedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError("Can't set attribute")
        self._ohms = ohms


# Trying to assign to the property after construction raise an exception.

r4 = FixedResistance(1e3)
# r4.ohms = 2e3
# AttributeError: Can't set attribute


# The biggest shortcoming of @property is that the methods for an attribute
# can be shared by subclass. Unrelated classes can't share the same
# implementation. However, Python also supports descriptors (see Item 31: Use
# descriptors for reusable @property methods) that enable reusable property
# logic and many other use cases.

# Finally, when you use @property methods to implement setters and getters, be
# sure that the behavior you implement is not surprising. For example, don't
# set other attributes in getter property methods.

class MysteriousResistor(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        self.voltage = self._ohms * self.current
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        # if hasattr(self, '_ohms'):
        #     raise AttributeError("Can't set attribute")
        self._ohms = ohms


# This leads to extremely bizarre behavior.


r7 = MysteriousResistor(10)
r7.current = 0.01
print('Before:  %5r' % r7.voltage)
r7.ohms
print('After:   %5r' % r7.voltage)
# Before:      0
# After:     0.1


# The best policy is to only modify related object state in @property.setter
# methods. Be sure to avoid any other side effects the caller may not expect
# beyond the object, such as importing modules dynamically, running slow
# helper functions, or making expensive database queries. Users of your class
# will expect its attributes to be like any other Python object: quick and
# easy. Use normal methods to do anything more complex or slow.


# Things to remember

# 1. Define new class interfaces using simple public attributes, and avoid set
#     and get methods.
# 2. Use @property to define special behavior when attributes are accessed on
#     your objects, if necessary.
# 3. Follow the rule of least surprise and void weird side effects in your
#    @property methods.
# 4. Ensure that @property methods are fast; do slow or complex work using
#    normal methods.
