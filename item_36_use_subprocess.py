# Chapter 5: concurrency and parallelism
import subprocess
import time
import os


# Concurrency is when a computer does many different things seemingly at the
# same time. For example, on a computer with one CPU core, the operating
# system will rapidly change which program is running on the single processor.
# This interleaves execution of the programs, providing the illusion that the
# programs are running simultaneously.

# Parallelism is actually doing many different things at the same time.
# Computers with multiple CPU cores can execute multiple programs
# simultaneously. Each CPU core runs the instructions of a separate program,
# allowing each program to make forward progress during the same instant.

# Within a single program, concurrency is a tool that makes it easier for
# programmers to solve certain types of problems. Concurrent programs enable
# many distinct paths of execution to make forward progress in a way that
# seems to be both simultaneous and independent.

# The key difference between parallelism and concurrency is speedup. When two
# distinct paths of execution in a program make forward progress in parallel,
# the time it takes to do the total work is cut in half; the speed of
# execution is faster by a factor of two. In contrast, concurrent programs
# may run thousands of separate paths of execution seemingly in parallel but
# provide no speedup for the total work.

# Python makes it easy to write concurrent programs. Python can also be used
# to do parallel work through system calls, sub-processes and C-extensions.
# But it can be very difficult to make concurrent Python code truly run in
# parallel. It's important to understand how to best utilize Python in these
# subtly different situations.


# Item 36: use subprocess to manage child processes.


# Python has battle-hardened libraries for running and managing child
# processes. This makes Python a great language for gluing other tools
# together, such as command-line utilities. When existing shell scripts get
# complicated, as they often do over time, graduating them to a rewrite in
# Python is a natural choice for the sake of readability and maintainability.

# Child processes started by Python are able to run in parallel, enabling you
# to use Python to consume all of the CPU cores of your machine and maximize
# the throughput of your programs. Although Python itself may be CPU bound
# ("see Item 37: Use threads for blocking I/O, avoid for parallelism"), it's
# easy to use Python to drive and coordinate CPU-intensive workloads.

# Python has had many ways to run sub-processes over the years, including
# popen, popen2, and os.exec*. With the Python of today, the best and simplest
# choice for managing child processes is to use the subprocess built-in module.

# Running a child process with subprocess is simple. Here, the Popen
# constructor starts the process. The communicate method reads the child
# process's output and waits for termination.


proc = subprocess.Popen(
    ['echo', 'Hello from the child!'],
    stdout=subprocess.PIPE
)
out, err = proc.communicate()
print(out.decode('utf-8'))
# Hello from the child!


# Child processes will run independently from their parent process, the Python
# interpreter. Their status can be polled periodically while Python does other
# work.


proc = subprocess.Popen(['sleep', '0.0001'])
while proc.poll() is None:
    print('Working...')
    # some time-consuming work here
    total = 0
    for i in range(1000):
        total += i
    print(total)
print('Exit status', proc.poll())
# Working...
# 499500
# Working...
# 499500
# Working...
# 499500
# Exit status 0


# Decoupling the child process from the parent means that the parent process
# is free to run many child processes in parallel. You can do this by starting
# all the child processes together upfront.


def run_sleep(period):
    proc = subprocess.Popen(['sleep', str(period)])
    return proc

start = time.time()
procs = []
for _ in range(10):
    proc = run_sleep(0.0001)
    procs.append(proc)

# Later, you can wait for them to finish their I/O and terminate with the
# communicate method.

for proc in procs:
    proc.communicate()

end = time.time()
print('Finished in %.3f seconds' % (end-start))
# Finished in 0.008 seconds

# Note
# If these process ran in sequence, the total delay would be 1 second, not the
# 0.008 second I measured.


# You can also pipe data from your Python program into a subprocess and
# retrieve its output. This allows you to utilize other programs to do work
# in parallel. For example, say you want to use the openssl command-line tool
# to encrypt some data. Starting the child process with command-line arguments
# and I/O pipes is easy.

# Here, I pipe random bytes into the encryption function, but in practice this
# would be user input, a file handle, a network socket, etc.:


def run_openssl(data):
    env = os.environ.copy()
    env['password'] = b'\xe24U\n\xd0Q13S\x11'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )
    proc.stdin.write(data)
    proc.stdin.flush()   # Ensure the child gets input
    return proc

procs = []
for _ in range(3):
    data = os.urandom(10)
    proc = run_openssl(data)
    procs.append(proc)

# The child processes will run in parallel and consume their input. Here, I
# wait for them to finish and then retrieve their final output:

for proc in procs:
    out, err = proc.communicate()
    print(out[-10:])
# b'\xc9/"\xf4\x902S\xa5z\x98'
# b'\xa7\x1d\xd1\x7f\x91\xa3\x14\x82\xb5\x83'
# b'Nh_\x82\xfc\x8c+DH\xb0'


# You can also create chains of parallel processes just like UNIX pipes,
# connecting the output of one child process into the input of another, and
# so on. Here's a function that starts a child process that will cause the
# md5 command-line tool to consume an input stream:


def run_md5(input_stdin):
    proc = subprocess.Popen(
        ['md5sum'],
        stdin=input_stdin,
        stdout=subprocess.PIPE
    )
    return proc
# Note
# Python's hashlib built-in module provides the md5 function, so running a
# subprocess like this isn't always necessary. The goal here is to demonstrate
# how sub-processes can pipe inputs and outputs.

# Now, I can kick off a set of openssl processes to encrypt some data and
# another set of processes to md5 hash the encrypted output.

input_procs = []
hash_procs = []
for _ in range(3):
    data = os.urandom(10)
    proc = run_openssl(data)
    input_procs.append(proc)
    hash_proc = run_md5(proc.stdout)
    hash_procs.append(hash_proc)

# The I/O between the child processes will happen automatically once you get
# them started. All you need to do is wait for them to finish and print the
# final output.

for proc in input_procs:
    proc.communicate()

for proc in hash_procs:
    out, err = proc.communicate()
    print(out.strip())
# b'e8afc9c05add1f659486b28f54fdbfbe  -'
# b'8e1b214eb900553421a9fef43e93479b  -'
# b'd9d4a0381bb3d04e961c3d7a9ba84ee9  -'


# If you're worried about the child processes never finishing or somehow
# blocking on input or output pipes, then be sure to pass the timeout
# parameter to the communicate method. This will cause an exception to be
# raised if the child process hasn't responded within a time period, giving
# you a chance to terminate the misbehaving child.


proc = run_sleep(10)
try:
    proc.communicate(timeout=0.1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()

print('Exit status', proc.poll())
# Exit status -15

# Unfortunately, the timeout parameter is only available in Python 3.3 and
# later. In earlier versions of Python, you'd need to use the select built-in
# module on proc.stdin, proc.stdout, and proc.stderr in order to enforce
# timeouts on I/O.


# Things to remember

# 1. Use the subprocess to run child processes and manage their input and
#    output streams.
# 2. Child processes run in parallel with the Python interpreter, enabling you
#    to maximize your CPU usage.
# 3. Use the timeout parameter with communicate to avoid deadlocks and hanging
#    child processes.
