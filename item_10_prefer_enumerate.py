# Item 10: Prefer enumerate over range
import random

# The range built-in function is useful for loops that iterate over a set of
# integers.

random_bits = 0
for i in range(64):
    if random.randint(0, 1):
        random_bits |= 1 << i


# When you
