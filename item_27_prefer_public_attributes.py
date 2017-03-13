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
# underscore.

#

#

#

#

#

#

#

#

#

#

#

#

#

#

#

#
#

#

#
#

#

#
