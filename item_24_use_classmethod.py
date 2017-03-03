# Item 24: Use @classmethod polymorphism to construct objects generically


# In Python, not only do the objects support polymorphism, but the classes do
# as well. What does that mean, and what is it good for?

# Polymorphism is a way for multiple classes in a hierarchy to implement their
# own unique versions of a method. This allows many classes to fulfill the
# same interface or abstract base class while providing different
# functionality (see Item 28: "Inherit from collections.abc for custom
# container types" for an example).

# For example, say you're writing a MapReduce implementation and you want a
# common class to represent the input data. Here, I define such a class with
# a read method that must be defined by subclasses:


class InputData(object):
    def read(self):
        raise NotImplementedError


# Here, I have a concrete subclass of InputData that reads data from a file on
# disk:


class PathInputData(InputData):
    def __int__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        return open(self.path).read()


# You could have any number of InputData subclasses like PathInputData and
# each of them could implement the standard interface for read to return the
# bytes of data to process. Other InputData subclasses could read from the
# network, decompress data transparently, etc.

# You'd want a similar abstract interface for the MapReduce worker that
# consumes the input data in a standard way.


class Worker(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError


# Here, I define a concrete subclass of Worker to implement the specific
# MapReduce function I want to apply: a simple newline counter:


class LineCountWorker(Worker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


#




#

#




#

#

