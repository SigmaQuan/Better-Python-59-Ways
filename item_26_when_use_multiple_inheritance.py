# Item 26: Use multiple inheritance only for mix-in utility classes


# Python is an object-oriented language with built-in facilities for making
# multiple inheritance tractable (see Item 25: "Initialize parent classes with
# super"). However, it's better to multiple inheritance altogether.

# If you find yourself desiring the convenience and encapsulation that comes
# with multiple inheritance, consider writing a mix-in instead. A mix-in is a
# small class that only defines a set of additional methods that a class
# should provide. Mix-in classes don't define their own instance attributes
# nor require their __init__ constructor to be called.

# Writing mix-ins is easy because Python makes it trivial to inspect the
# current state of any object regardless of its type. Dynamic inspection lets
# you write generic functionality a single time, in a mix-in, that can be
# applied to many other classes. Mix-ins can be composed and layered to
# minimize repetitive code and maximize reuse.

# For example, say you want the ability to convert a Python object from its
# in-memory representation to a dictionary that's ready for serialization.
# Why not write this functionality generically so you can use it with all of
# your classes?

# Here, I define an example mix-in that accomplishes this with a new public
# method that's added to any class that inherits from it:


class ToDictMixin(object):
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

# The implementation details are straightforward and rely on dynamic attribute
# access using hasattr, dynamic type inspection with isinstance, and accessing
# the instance dictionary __dict__.

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key, value):
        if isinstance(value, ToDictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value


# Here, I define an example class that uses the mix-in to make a dictionary
# representation of a binary tree:


class BinaryTree(ToDictMixin):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


# Translating a large number of related Python objects into a dictionary
# becomes easy.


tree = BinaryTree(10,
                  left=BinaryTree(7, right=BinaryTree(9)),
                  right=BinaryTree(13, left=BinaryTree(11)))
print(tree.to_dict())
# {'value': 10,
#  'right': {'value': 13,
#           'right': None,
#           'left': {'value': 11,
#                    'right': None,
#                    'left': None
#                   }
#           },
#  'left': {'value': 7,
#           'right': {'value': 9,
#                     'right': None,
#                     'left': None
#                    },
#           'left': None
#          }
# }


# The best part about mix-ins is that you can make their generic functionality
# pluggable so behaviors can be overridden when required. For example, here I
# define a subclass of BinaryTree that holds a reference to its parent. This
# circular reference would cause the default implementation of
# ToDictMixin.to_dict to loop forever.


class BinaryTreeWithParent(BinaryTree):
    def __init__(self, value, left=None, right=None, parent=None):
        super().__init__(value, left=left, right=right)
        self.parent = parent

# The solution is to override the ToDictMixin._traverse method in the
# BinaryTreeWithParent class to only process values that matter, preventing
# cycles encountered by the mix-in. Here, I override the _traverse method to
# not traverse the parent and just insert its numerical value:

    def _traverse(self, key, value):
        if (isinstance(value, BinaryTreeWithParent) and key == 'parent'):
            return value.value  # Prevent cycles
        else:
            return super()._traverse(key, value)


# Calling BinaryTreeWithParent.to_dict will work without issue because the
# circular referencing properties aren't followed.


root = BinaryTreeWithParent(10)
root.left = BinaryTreeWithParent(7, parent=root)
root.left.right = BinaryTreeWithParent(9, parent=root.left)
print(root.to_dict())
# {'parent': None,
#  'left': {'parent': 10,
#           'left': None,
#           'value': 7,
#           'right': {'parent': 7,
#                     'left': None,
#                     'value': 9,
#                     'right': None
#                    }
#           },
#  'value': 10,
#  'right': None
# }


#