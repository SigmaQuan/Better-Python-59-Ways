# Item 44: Make pickle reliable with copyreg
import pickle
import copyreg


# The pickle built-in module can serialize Python objects into a stream of
# bytes and deserialize bytes back into objects. Pickled byte streams
# shouldn't be used to communicate between untrusted parties. The purpose of
# pickle is to let you pass Python objects between programs that you control
# over binary channels.


# NOTE
# The pickle module's serialization format is unsafe by design. The
# serialized data contains what is essentially a program that describes how to
# reconstruct the original Python. This means a malicious pickle payload could
# be used to compromise any part of the Python program that attempts to
# deserialize it.

# In contrast, the json module is safe by design. Serialized JSON data
# contains a simple description of an object hierarchy. Deserializing JSON
# data does not expose a Python program to any additional risk. Formats like
# JSON should be use for communication between programs or people that don't
# trust each other.


# For example, say you want to use a Python object to represent the state of
# a player's progress in a game. The game state includes the level the player
# is on and the number of lives he or she has remaining.


class GameState(object):
    def __init__(self):
        self.level = 0
        self.lives = 4


# The program modifies this object as the the game runs.

state = GameState()
state.level += 1  # Player beat a level
state.lives -= 1  # Player had to try again

# When the user quits playing, the program can save the state of the game to a
# file so it can be resumed at a later time. The pickle module makes it easy
# to do this. Here, I dump the GameState object directly to a file:

state_path = '/tmp/game_state.bin'
with open(state_path, 'wb') as f:
    pickle.dump(state, f)


# Later, I can load the file and get back the GameState object as if it had
# never been serialized.

with open(state_path, 'rb') as f:
    state_after = pickle.load(f)
print(state_after.__dict__)
# {'lives': 3, 'level': 1}

# The problem with approach is what happens as the game's features expand
# over time. Imagine you want the player to earn points towards a high score.
# To track the player's points, you'd add a new field to the GameState class.


class GameState(object):
    def __init__(self):
        self.level = 0
        self.lives = 4
        self.points = 0


# Serialzing the new version of the GameState class using pickle will work
# exactly as before. Here, I simulate the round-trip through a file by
# serializing to a string with dumps and back to an object with loads:

state = GameState()
serialized = pickle.dumps(state)
state_after = pickle.loads(serialized)
print(state_after.__dict__)
# {'level': 0, 'lives': 4, 'points': 0}

# But what happens to older saved GameState objects that the user may want to
# resume? Here, I unpickle an old game file using a program with the new
# definition of the GameState class:

with open(state_path, 'rb') as f:
    state_after = pickle.load(f)
print(state_after.__dict__)
# {'lives': 3, 'level': 1}

# The points attribute is missing! This is especially confusing because the
# returned object is an instance of the new GameState class.

assert isinstance(state_after, GameState)

# This behavior is a byproduct of the way the pickle module works. Its primary
# use case is making it easy to serialize objects. As soon as your use of
# pickle expands beyond trivial usage, the module's functionality starts to
# break down in surprising ways.

# Fixing these problems is straightforward using the copyreg built-in module.
# The copyreg module lets you register the functions responsible. The copyreg
# module lets you register the functions responsible for serializing Python
# objects, allowing you to control the behavior of pickle and make it more
# reliable.


# Default Attribute Values

# In the simplest case, you can use a constructor with default arguments (see
# Item 19: "Provide optional behavior with keyword arguments") to ensure that
# GameState objects will always have all attributes after unpickling. Here, I
# redefine the constructor this way:


class GameState(object):
    def __init__(self, level=0, lives=4, points=0):
    # def __init__(self, level=0, lives=4, points=0, magic=5):
        self.level = level
        self.lives = lives
        self.points = points


# To use this constructor for pickling, I define a helper function that takes
# a GameState object and turns it into a tuple of parameters for the copyreg
# module. The returned tuple contains the function to use for unpickling and
# the parameters to pass to the unpickling function.


def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    return unpickle_game_state, (kwargs,)


# Now, I need to define the unpickle_game_state helper. This function takes
# serialized data and parameters from pickle_game_state and returns the
# corresponding GameState object. It's a tiny wrapper around the constructor.


def unpickle_game_state(kwargs):
    return GameState(**kwargs)


# Now, I register these with the copyreg built-in module.

copyreg.pickle(GameState, pickle_game_state)

# Serializing and deserializing works as before.

state = GameState()
state.points += 1000
serialized = pickle.dumps(state)
state_after = pickle.loads(serialized)
print(state_after.__dict__)
# {'level': 0, 'lives': 4, 'points': 1004}

# With this registration done, now I can change the definition of GameState to
# give the player a count of magic spells to use. This change is similar to
# when I added the points field to GameState.


class GameState(object):
    def __init__(self, level=0, lives=4, points=0, magic=5):
        self.level = level
        self.lives = lives
        self.points = points
        self.magic = magic


# But unlike before, deserializing an old GameState object will result in
# valid game data instead of missing attributes. This works because
# unpickle_game_state calls the GameState constructor directly. The
# constructor's keyword arguments have default values when parameters are
# missing. This causes old game state files to receive the default value for
# the new magic field when they are deserialized.

state_after = pickle.loads(serialized)
print(state_after.__dict__)
# {'level': 0, 'points': 1000, 'magic': 5, 'lives': 4}


# Versioning Classes

# Sometimes you'll need to make backwards-incompatible changes to your Python
# objects by removing fields. This prevents the default argument approach to
# serialization from working.

# For example, say you realize that a limited number of lives is a bac idea,
# and you want to remove the concept of lives from the game. Here, I redefine
# the GameState to no longer have a lives field:


class GameState(object):
# class BetterGameState(object):
    def __init__(self, level=0, points=0, magic=5):
        self.level = level
        self.points = points
        self.magic = magic


# The problem is that this breaks deserializing old game data. All fields from
# the old data, even ones removed from the class, will be passed to the
# GameState constructor by the unpick_game_state function.

# pickle.loads(serialized)
# TypeError: __init__() got an unexpected keyword argument 'lives'

# The solution is to add a version parameter to the functions supplied to
# copyreg. New serialized data will have a version of 2 specified when
# pickling a new GameState object.


def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    kwargs['version'] = 2
    return unpickle_game_state, (kwargs,)


# Old versions of the data will not have a version argument present, allowing
# you to manipulate the arguments passed to the GameState constructor
# accordingly.


def unpickle_game_state(kwargs):
    version = kwargs.pop('version', 1)
    if version == 1:
        kwargs.pop('lives')
    return GameState


# Now, deserializing an old object works properly.

copyreg.pickle(GameState, pickle_game_state)
state_after = pickle.loads(serialized)
# print(state_after.__dict__)
# {'__init__': <function GameState.__init__ at 0x7f4cc7da5730>,
# '__module__': '__main__',
# '__dict__': <attribute '__dict__' of 'GameState' objects>,
# '__weakref__': <attribute '__weakref__' of 'GameState' objects>,
# '__doc__': None}

# You can continue this approach to handle changes between future version of
# the same class. Any logic you need to adapt an old version of the class to
# a new version of the class can go in the unpickle_game_state function.


# Stable Import Paths

# One other issue you may encounter with pickle is breakage from renaming a
# class. Often over the life cycle of a program, you'll refactor your code by
# renaming classes and moving them to other modules. Unfortunately, this will
# break the pickle module unless you're careful.

# Here, I rename the GameState class to BetterGameState, removing the old
# class from the program entirely:


class BetterGameState(object):
    def __init__(self, level=0, points=0, magic=5):
        self.level = level
        self.points = points
        self.magic = magic

# Attempting to deserialize an old GameState object will now fail because the
# class can't be found.

pickle.loads(serialized)
# ...

# The cause of this exception is that the import path of the serialized
# object's class is encoded in the pickled data.

print(serialized[:25])
# b'\x80\x03c__main__\nunpickle_game'

# The solution is to use copyreg again. You can specify a stable identifier
# for the function to use for unpickling an object. This allows you to
# transition pickled data to different classes with different names when it's
# deserialized. It gives you a level of indirection.

copyreg.pickle(BetterGameState, pickle_game_state)

# After using copyreg, you can see that the import path to pickle_game_state
# is encoded in the serialized data instead of BetterGameState.

state = BetterGameState()
serialized = pickle.dumps(state)
print(serialized[:35])
# b'\x80\x03c__main__\nunpickle_game_state\nq\x00}'

# The only gotcha is that you can't change the path of the module in which
# the unpickle_game_state function is present. Once you serialize data with a
# function, it must remain available on that import path for deserializing in
# the future.


# Things to remember

# 1. The pickle built-in module is only useful for serializing and
#    de-serializing objects between trusted programs.
# 2. The pickle module may break down when used for more than trivial use
#    cases.
# 3. Use the copyreg built-in module with pickle to add missing attributes
#    values, allow versioning of classes, and provide stable import paths.
