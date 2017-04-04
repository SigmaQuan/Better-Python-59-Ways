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


# Pro
