# Chapter 5: concurrency and parallelism


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


# Things to remember

# 1. Use the subprocess to run child processes and manage their input and
#    output streams.
# 2. Child processes run in parallel with the Python interpreter, enabling you
#    to maximize your CPU usage.
# 3. Use the timeout parameter with communicate to avoid deadlocks and hanging
#    child processes.
