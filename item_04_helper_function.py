# Item 4: Write helper functions instead of complex expressions


# Python's pithy syntax makes it easy to write single-line expressions that
# implement a lot of logic. For example, say you want to decode the query
# string from a URL. Here, each query string parameter represents an integer
# value:


# Python 3
from urllib.parse import parse_qs
my_values = parse_qs('red=5&blue=0&green=', keep_blank_values=True)
print(repr(my_values))
# $ python3 item_04_helper_function.py
# {'red': ['5'], 'green': [''], 'blue': ['0']}


# Some query string parameters may have multiple values, some may have single
# values, some may be present but have blank values, and some may be missing
# entirely. Using the get method on the result dictionary will return
# different values in each circumstance.


print("Red:     ", my_values.get('red'))
print("Green:   ", my_values.get('green'))
print("Opacity: ", my_values.get('opacity'))
# $ python3 item_04_helper_function.py
# Red:      ['5']
# Green:    ['']
# Opacity:  None


# It'd be nice if a default value of 0 was assigned when a parameter isn't
# supplied or is blank. You might choose to do this with Boolean expressions
# because it feels like this logic doesn't merit a whole if statement or
# helper function quite yet.
