# Item 57： Consider interactive debugging with pdb


# Everyone encounters bugs in their code while developing programs. Using the
# print function can help you track down the source of many issues (see Item
# 55: "Use repr strings for debugging output"). Writing tests for specific
# cases that cause trouble is another great way to isolate problems (see Item
# 56: "Test everything with unittest").

# But these tools aren't enough to find every root cause. When you need
# something more powerful, it's time to try Python's built-in interactive
# debugger. The debugger lets you inspect program state, print local
# variables, and set through a Python program one statement at a time.

# In most other programming language, you use a debugger by specifying what
# line of a source file you'd like to stop on, then execute the program. In
# contrast, with Python the easiest way to use the debugger is by modifying
# your program to directly initiate the debugger just before you think you'll
# have an issue worth investigating. There is no difference between running a
# Python program under a debugger and running it normally.

# To initiate the debugger, all you have to do is import the pdb built-in
# module and run its set_trace function. You'll often see this done in a
# single line so programmers can comment it out with a single # character.


def complex_func(a, b, c):
    # ...
    import pdb
    pdb.set_trace()


# As soon as this statement runs, the program will pause its execution. The
# terminal that started you program will turn into an interactive Python
# shell.

# -> import pdb; pdb.set_trace()
# (Pdb)

# At the (Pdb) prompt, you can type in the same of local variables to see
# their values printed out. You can see a list of all local variables by
# calling the locals built-in function. YOu can import modules, inspect global
# state, construct new objects, run the help built-in function, and even
# modify parts of the program--whatever you need to to to aid in your
# debugging. In addition, the debugger has three commands that make inspecting
# the running program easier.
# 1. bt: Print the trackback of the current execution call back. This lets you
#    figure out where you are in your program anc how you arrived at the
#    pdb.set_trace trigger point.
# 2. up: Move your scope up the function call stack to the caller of the
#    current function. This allows you to inspect the local variables in
#    higher levels of the call stack.
# 3. down: Move your scope back down the function call stack one level.

# Once you're done inspecting the current state, you can use debugger commands
# to resume the program's execution under precise control.
# 1. step: Run the program until the next line of execution in the program,
#    then return control back to the debugger. If the next line of execution
#    includes calling a function, the debugger will stop in the function that
#    was called.
# 2. next: Run the program until the line of execution in the current
#    function, then return control back to the debugger. If the next line of
#    execution includes calling a function, the debugger will not stop until
#    the called function has returned.
# 3. return: Run the program until the current function returns, then return
#    control back to the debugger.
# 4. continue: Continue running the program until the next breakpoint (or
#    set_trace is called again).


# Things to remember

# 1. You can initiate the Python interactive debugger at a point of interest
#    directly in your program with the import pdb; pdb.set_trace() statements.
# 2. The Python debugger prompt is a full Python shell that lets you inspect
#    and modify the state of a running program.
# 3. pdb shell commands let you precisely control program execution, allowing
#    you to alternate between inspecting program state and progressing program
#    execution.
