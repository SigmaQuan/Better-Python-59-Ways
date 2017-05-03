# Item 39: Use queue to coordinate work between threads


# Python programs that do many things concurrently often need to coordinate
# their work. One of the most useful arrangements for concurrent work is a
# pipeline of functions.

# A pipeline works like an assembly line used in manufacturing. Pipelines have
# many phases in serial with a specific function for each phase. Each function
# can operate concurrently on the piece of work in its phase. The work moves
# forward as each function completes until there are no phases remaining. This
# approach is especially good for work that includes blocking I/O or
# sub-processes-activities that can easily be parallelized using Python (see
# Item 37: "Use threads for blocking I/O, avoid for parallelism").

# For example, say you want to build a system that will take a  constant
# stream of images from your digital camera, resize them, and then add them to
# a photo gallery online. New images are retrieved in the first phase. The
# The downloaded images are passed through the resize function int he second
# phase. The resized images are consumed by the upload function in the final
# phase.

# Imagine you had already written Python functions that execute the phases:
# download, upload. How do you assemble a pipeline to do the work
# concurrently.

# The first thing you need is a way to hand off work between the pipeline
# phases. This can be modeled as a thread-safe producer-consumer queues (see
# Item 38: "Use lock to prevent data races in threads" to understand the
# importance of thread safely in Python; see Item 46: "Use built-in algorithms
# and data structures" for the deque class).




# Things to remember
# 1. Pipelines are a great way to organize sequences of work that run
#     concurrently using multiple Python threads.
# 2. Be aware of the many problems in building concurrent pipelines: busy
#     waiting, stopping workers, and memory explosion.
# 3. The Queue class has all of the facilities you need to build robust
#     pipelines: blocking operations, buffer sizes, and joining.
