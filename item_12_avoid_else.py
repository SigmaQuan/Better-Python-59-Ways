# Item 12: Avoid else blocks after for and while loops


# Python loops have an extra feature that is not available in most other
# programming language: you can put an else block immediately after a loop's
# repeated interior block.


for i in range(3):
    print('Loop %d' % i)
else:
    print('Else block!')
# Loop 0
# Loop 1
# Loop 2
# Else block!


# Surprisingly, the else block runs immediately after the loop finishes. Why
# is the clause called "else"? Why not "and"? In an if/else statement, else
# means, "Do this if the block before this doesn't happen." In a try/except
# statement, except has the definition: "Do this if trying the block before
# this failed."


# Similarly, else from try/except/else follows this pattern (see item 13: Take
# advantage of each block in try/except/else/finally) because it means, "Do
# this if the block before did not fail". try/finally is also intuitive
# because it means, "Always do what is final after trying the block before.

# Given all of the uses of else, except, and finally in Python, a new
# programmer might assume that the else part of for/else means, "Do this if
# the loop wan't completed". In reality, it does exactly the opposite. Using
# a break statement in a loop will actually skip the else block.


for i in range(3):
    print('Loop %d' % i)
    if i == 1:
        break
else:
    print('Else block!')
# Loop 0
# Loop 1


# Another surprise is that the else block will run immediately if you loop
# over an empty sequence.


for x in []:
    print('Never runs')
else:
    print('For Else block!')
# For Else block!


# The else block also runs when while loops are initially false.


while False:
    print('Never runs!')
else:
    print('While Else block!')
# While Else block!


# The rationale for these behaviors is that else blocks after loops are useful
# when you're using loops to search for something. For example, say you want
# to determine whether two numbers are coprime (their only common divisor is
# 1). Here, I iterate through every possible common divisor and test the
# numbers. After every option has been tried, the loop ends. The else block
# runs when the numbers are coprime because the loop doesn't encounter a
# break.


a = 4
b = 9
for i in range(2, min(a, b) + 1):
    print('Testing', i)
    if a % i == 0 and b % i == 0:
        print('Not coprime')
        break
else:
    print('Coprime')
# Testing 2
# Testing 3
# Testing 4
# Coprime


# In practice, you wouldn't write the code this way. Instead, you'd write a
# helper function to do the calculation. Such a helper function is writen in
# two common styles.

# The first approach is to return early when you find the condition you're
# looking for. You return the default outcome if you fall through the loop.


def coprime(a, b):
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            return False
    return True


# The second way is to have a result variable that indicates whether you've
# found what you're looking for in the loop. You break out of the loop as soon
# as you find something.


def coprime2(a, b):
    is_coprime = True
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            is_coprime = False
            break
    return is_coprime


# Both of these approaches are so much clearer to readers of unfamiliar code.
# The expressively you gain from the else block doesn't outweigh the burden
# you put on people (including yourself) who want to understand your code in
# the future. Simple constructs like loops should be self-evident in Python.
# You should avoid using else blocks after loops entirely.


# Things to remember

# 1. Python has special syntax that allows else blocks to immediately follow
#     for and while loop interior blocks.
# 2. The else block after a loop only runs if the loop body did not encounter
#     a break statement.
# 3. Avoid using else blocks after loops because their behavior isn't
#     intuitive and can be confusing.
