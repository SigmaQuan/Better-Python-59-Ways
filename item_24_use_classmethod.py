# Item 24: Use @classmethod polymorphism to construct objects generically
import os
import threading


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


# It may look like this implementation is going great, but I've reached the
# biggest hurdle in all of this. What connects all of these pieces? I have a
# nice set of classes with reasonable interfaces and abstractions--but that's
# only useful once the objects are constructed. What's responsible for
# building the objects and orchestrating the MapReduce?


def generate_inputs(data_dir):
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, name))


# Next, I create the LineCountWorker instances using the InputData instances
# returned by generate_inputs.


def create_workers(input_list):
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers


# I execute these worker instances by fanning out the map step to multiple
# threads (see Item 37: "Use threads for blocking I/O, Avoid for
# parallelism"). Then, I call reduce repeatedly to combine the results into
# one final value.


def execute(workers):
    threads = [threading.Thread(target=w.wap) for w in workers]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    first, rest = workers[0], workers[1:]
    for worker in rest:
        first.reduce(worker)
    return first.result


# Finally, I connect all of the pieces together in a function to run each
# step.


def mapreduce(data_dir):
    inputs = generate_inputs(data_dir)
    workers = create_workers(inputs)
    return execute(workers)


# Running this function on a set of test input files works great.


from tempfile import TemporaryDirectory


def write_test_files(tmpdir):
    # ...
    print('write_test_file')


with TemporaryDirectory() as tmpdir:
    write_test_files(tmpdir)
    result = mapreduce(tmpdir)

print('There are', result, 'lines')
# write_test_file
# Traceback (most recent call last):
#   File "item_24_use_classmethod.py", line 136, in <module>
#     result = mapreduce(tmpdir)
#   File "item_24_use_classmethod.py", line 120, in mapreduce
#     return execute(workers)
#   File "item_24_use_classmethod.py", line 107, in execute
#     first, rest = workers[0], workers[1:]
# IndexError: list index out of range


# What's the problem? The huge issue is the mapreduce function is not generic
# at all. If you want to write another InputData or Worker subclass, you would
# also have to rewrite the generate_inputs, create_workers, and mapreduce
# functions to match.


# This problem boils down to needing a generic way to construct objects. In
# other languages, you'd solve this problem with constructor polymorphism,
# requiring that each InputData subclass provides a special constructor that
# can be used generically by the helper methods that orchestrate the
# MapReduce. The trouble is that Python only allows for the single
# constructor method __init__. It's unreasonable to require every InputData
# subclass to have a compatible constructor.


# The best way to solve this problem is with @classmethod polymorphism. This
# is exactly like the instance method polymorphism I used for InputData.read,
# except that it applies to whole classes instead of their constructed
# objects.

# Let me apply this idea to the MapReduce classes. Here, I extend the
# InputData class with a generic class method that's responsible for creating
# new InputData instances using a common interface:


class GenericInputData(object):
    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError


# I have generate_inputs take a dictionary with a set of configuration
# parameters that are up to the InputData concrete subclass to interpret.
# Here, I use the config to find the directory to list for input files:


class PathInputData(GenericInputData):
    # ...
    def read(self):
        return open(self.path).read()

    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))


# Similarly, I can make the create_workers helper part of the GenericWorker
# class.


#

