# Item 47: Use decimal when precision ia paramount
from decimal import Decimal
from decimal import ROUND_UP


# Python is excellent language for writing code that interacts with numerical
# data. Python's integer type can represent values of any practical size. Its
# double-precision floating point type complies with the IEEE 754 standard.
# The language also provides a standard complex number type for imaginary
# values. However, these aren't enough for every situation.

# For example, say you want to compute the amount to charge a customer for an
# international phone call. You know the time in minutes and seconds that the
# customer was on the phone (say, 3 minutes 42 seconds). You also have a set
# rate for the cost of calling Antarctica from the United States
# ($1.45/minute). What should the charge be?

# With floating point math, the computed charge seems reasonable.

rate = 1.45
seconds = 3*60 + 42
cost = rate * seconds / 60
print(cost)
# 5.364999999999999

# But rounding it to the nearest whole cent rounds down when you want it to
# round up to properly cover all costs incurred by the customer.

print(round(cost, 2))
# 5.36

# Say you also want to support very short phone calls between places that are
# much cheaper to connect. Here, I compute the charge for a phone call that
# was 5 seconds long with a rate of $0.05/minute:

rate = 0.05
seconds = 5
cost = rate * seconds / 60
print(cost)
# 0.004166666666666667

# The resulting float is so low that it rounds down to zero. This won't do!

print(round(cost, 2))
# 0.0

# The solution is to use the Decimal class from the decimal built-in module.
# The Decimal class provides fixed point math of 28 decimal points by default.
# It can go even higher if required. This works around the precision issues in
# IEEE 754 floating point numbers. The class also gives you more control over
# rounding behaviors.

# For example, redoing the Antarctica calculation with Decimal results in an
# exact charge instead of an approximation.

rate = Decimal('1.45')
seconds = Decimal('222')  # 3*60 + 42
cost = rate * seconds / Decimal('60')
print(cost)
# 5.365

# The Decimal class has a built-in function for rounding to exactly the
# decimal place you need with rounding behavior you want.

rounded = cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
print(rounded)
# 5.37

# Using the quantize method this way also properly handles the small usage
# case for short, cheep phone calls. Here, you can see the Decimal cost is
# still less than 1 cent fro the call:

rate = Decimal('0.05')
seconds = Decimal('5')
cost = rate * seconds / Decimal('60')
print(cost)
# 0.004166666666666666666666666667

# But the quantize behavior ensures that this is rounded up to one whole cent.

rounded = cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
print(rounded)
# 0.01

# While Decimal works great for fixed point numbers, it still has limitations
# in its precision (e.g. 1/3 will be an approximation). For representing
# rational numbers with no limit to precision, consider using the Fraction
# class from the fractions built-in module.


# Things to remember

# 1. Python has built-in types and classes in modules that can represent
#    practically every type of numerical value.
# 2. The Decimal class is ideal for situations that require high precision and
#    exact rounding behavior, such as computations of monetary values.
