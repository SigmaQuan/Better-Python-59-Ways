# Item 33: Validate subclass with metaclass


# One of simplest applications of metaclass is verifying that a class was
# defined correctly. When you're building a complex class hierarchy, you may
# want to enforce style, require overriding methods, or have strict
# relationships between class attributes. Metaclass enable these use cases by
# providing a reliable way to run your validation code each time a new
# subclass is defined.

# Often a class's validation code runs in the __init__ method, when an object
# of the class's type is constructed ().
