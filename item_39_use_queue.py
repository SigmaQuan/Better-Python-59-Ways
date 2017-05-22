# Item 39: Use queue to coordinate work between threads
from collections import deque
from threading import Thread
from threading import Lock
from time import sleep
from queue import Queue
import time

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
    def __init__(self):
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


def download(item):
    # print(item)
    # print("download()")
    pass


def resize(item):
    # print("resize()")
    # print(item)
    pass


def upload(item):
    # print("upload()")
    # print(item)
    pass

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
    pass

# This runs properly, but there's an interesting side effect caused by the
# threads polling their input queues for new work. The tricky part, where I
# catch IndexError exceptions in the run method, executes a large number of
# items.

processed = len(done_queue.items)
polled = sum(t.polled_count for t in threads)
print('Processed', processed, 'items after polling', polled, 'items')
# Processed 1000 items after polling 3008 items


# When the worker functions vary in speeds, an earlier phase can prevent
# progress in later phase, backing up the pipeline. This causes later phases
# to starve and constantly check their input queues for new work in a tight
# loop. The outcome is that worker threads waste CPU time doing nothing useful
# (they're constantly raising and catching IndexError exceptions).

# But that's just the beginning of what's wrong with this implementation.
# There are three more problems that you should also avoid. First, determining
# that all of the input work is complete requires yer another busy wait on the
# done_queue. Second, in Worker the run method will execute forever in its busy
# loop. There's no way to signal to a worker thread that it's time to exit.

# Third, and worst of all, a backup in the pipeline can cause the program to
# crash arbitrarily. If the first phase makes rapid progress but the second
# phase will constantly increase in size. The second phase won't be able to
# keep up. Given enough time and input data, the program will eventually run
# out of memory and die.


# Queue to Rescue

# The Queue class from the queue built-in module provides all of the
# functionality you need to solve these problems.

# Queue eliminates the busy waiting in the worker by making the get method
# block until new data is available. For example, here I start a thread that
# waits for some input data on a queue:

queue = Queue()


def consumer():
    print('Consumer waiting')
    queue.get()   # Runs after put() below
    print('Consumer done')

thread = Thread(target=consumer)
thread.start()


# Even though the thread is running first, it won't finish until an item is
# put on the Queue instance and the get method has something to return.

print('Producer putting')
queue.put(object())   # Runs before get() above
thread.join()
print('Producer done')
# Consumer waiting
# Producer putting
# Consumer done
# Producer done


# To solve the pipeline backup issue, the Queue class lets you specify the
# maximum amount of pending work you'll allow between two phases. This buffer
# size causes calls to put to block when the queue is already full. For
# example, here I define a thread that waits for a while before consuming a
# queue:

queue = Queue(1)   # Buffer size of 1


def consumer():
    time.sleep(0.1)  # Waits
    queue.get()      # Runs second
    print('Consumer got 1')
    queue.get()      # Runs fourth
    print('Consumer got 2')

thread = Thread(target=consumer)
thread.start()

# The wait should allow the producer thread to put both objects on the queue
# before the consume thread ever calls get. But the Queue size is one. That
# means the producer adding items to the queue will have to wait for the
# consumer thread to call get at least once before the second call to put will
# stop blocking and add the second item to the queue.

queue.put(object())
print('Producer put 1')  # Runs first
queue.put(object())
print('Producer put 2')
thread.join()
print('Producer done')
# Producer put 1
# Consumer got 1
# Producer put 2
# Consumer got 2
# Producer done

# The Queue class can also track the progress of work using the task_done
# method. This lets you wait for a phase's input queue to drain and eliminates
# the need for polling the done_queue at the end of your pipeline. For
# example, here I define a consumer thread that calls task_done when it
# finishes working on an item.

in_queue = Queue()

if __name__ == '__main__':
    def consumer():
        print("Consumer waiting")
        work = in_queue.get()  # Done second
        print('Consumer working')
        # Doning work
        # ..
        print('Consumer done')
        in_queue.task_done()   # Done third

Thread(target=consumer).start()

# Now, the producer code doesn't have to join the consumer thread or poll. The
# producer can just wait for the in_queue to finish by calling join on the
# Queue instance. Even once it's empty, the in_queue won't be joinable until
# after task_done is called for every item that was ever enqueued.

in_queue.put(object())  # Done first
print('Producer waiting')
in_queue.join()
print('Producer done')
# Consumer waiting
# Producer waiting
# Consumer working
# Consumer done
# Producer done

# I can put all of these behaviors together into a Queue subclass that also
# tells the worker thread when it should stop processing. Here, I define a
# close method that adds a special item to the queue that indicates these will
# be no more input items after it:


class ClosableQueue(Queue):
    SENTINEL = object()

    def close(self):
        self.put(self.SENTINEL)

# Then, I define an iterator for the queue that looks for this special object
# and stops iteration when it's found. This __iter__ method also calls
# task_done at appropriate times, letting me track the progress of work on the
# queue.
    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return  # Cause the thread to exit
                yield item
            finally:
                self.task_done()

# Now, I can redefine my worker thread to rely on the behavior of the
# ClosableQueue class. The thread will exit once the for loop is exhausted.


class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)

# Here, I re-create the set of worker threads using the new worker class:

download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()

threads = [
    StoppableWorker(download, download_queue, resize_queue),
    StoppableWorker(resize, resize_queue, upload_queue),
    StoppableWorker(upload, upload_queue, done_queue),
]

# After running the worker threads like before, I also send the stop signal
# once all the input work has been injected by closing the input queue of the
# first phase.

for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())

download_queue.close()

# Finally, I wait for the work to finish by joining each queue that connects
# the phases. Each time one phase is done, I signal the next phase to stop by
# closing its input queue. At the end, the done_queue contains all of the
# output objects as expected.

download_queue.join()
resize_queue.close()
resize_queue.join()
upload_queue.close()
upload_queue.join()
print(done_queue.qsize(), 'item finished')
# 1000 item finished


# Things to remember

# 1. Pipelines are a great way to organize sequences of work that run
#     concurrently using multiple Python threads.
# 2. Be aware of the many problems in building concurrent pipelines: busy
#     waiting, stopping workers, and memory explosion.
# 3. The Queue class has all of the facilities you need to build robust
#     pipelines: blocking operations, buffer sizes, and joining.
