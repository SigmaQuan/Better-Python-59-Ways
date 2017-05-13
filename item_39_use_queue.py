# Item 39: Use queue to coordinate work between threads
from collections import deque
from threading import Lock
from threading import Thread
from time import sleep


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

class MyQueue(object):
    def __int__(self):
        self.items = deque()
        self.lock = Lock()

# The producer, your digital camera, adds new images to the end of th list of
# pending items.
    def put(self, item):
        with self.lock:
            self.items.append(item)

# The consumer, the first phase of your processing pipeline, removes images
# from the front of the list of pending items.
    def get(self):
        with self.lock:
            return self.items.popleft()


# Here, I represent each phase of the pipeline as a Python thread that takes
# work from one queue like this, runs a function on it, and puts the results
# on another queue. I also track how many times the worker has checked for new
# input and how much work it's completed.


class Worker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0

# The trickiest pat is that the worker thread must properly handle the case
# where the input queue is empty because the previous phase hasn't completed
# its work yet. This happens where I catch the Index Error exceptions below.
# You can think of this as a holdup in the assembly line.
    def run(self):
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
                sleep(0.01)  # No work to do
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1


# Now I can connect the three phases together by creating the sequence for
# their coordination point and the corresponding worker threads.

download_queue = MyQueue()
resize_queue = MyQueue()
upload_queue = MyQueue()
done_queue = MyQueue()
threads = [
    Worker(download, download_queue, resize_queue),
    Worker(resize, resize_queue, upload_queue),
    Worker(upload, upload_queue, done_queue),
]


# I can start the threads and then inject a bunch of work into the first
# phase of the pipeline. Here, I use a plain object instance as a porxy for
# the real data required by the download function:


for thread in threads:
    thread.start()
for _ in range(1000):
    download_queue.put(object())

# Now I wait for all of the items to be processed by the pipeline and end up
# in the done_queue.


while len(done_queue.items) < 1000:
    # Do something useful while waiting
    # ....

# This runs properly, but there's an interesting side effect caused by the
# threads polling their input queues for new work. The tricky part, where I
# catch IndexError exceptions in the run method, executes a large number of
# items.

processed = len(done_queue.items)
polled = sum(t.polled_count for t in threads)
print('Processed', processed, 'items after polling', polled, 'items')




# Things to remember
# 1. Pipelines are a great way to organize sequences of work that run
#     concurrently using multiple Python threads.
# 2. Be aware of the many problems in building concurrent pipelines: busy
#     waiting, stopping workers, and memory explosion.
# 3. The Queue class has all of the facilities you need to build robust
#     pipelines: blocking operations, buffer sizes, and joining.
