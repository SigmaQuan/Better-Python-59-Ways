# Item 4: Write helper functions instead of complex expressions


# Python's pithy syntax makes it easy to write single-line expressions that
# implement a lot of logic. For example, say you want to decode the query
# string from a URL. Here, each query string parameter represents an integer
# value:


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

# Python's syntax makes this choice all too easy. The trick here is that the
# empty string, the empty list, and zero all evaluate to False implicitly.
# Thus, the expressions below will evaluate to the subexpression after the or
# operator when the first subexpression is False.


# For query string 'red=5&blue=0&green='
red = my_values.get('red', [''])[0] or 0
green = my_values.get('green', [''])[0] or 0
opacity = my_values.get('opacity', [''])[0] or 0
print("Red:     %r" % red)
print("Green:   %r" % green)
print("Opacity: %r" % opacity)
# Red:     '5'
# Green:   0
# Opacity: 0


# The red case works because the key is present in the my_values dictionary.
# The value is a list with one member: the string '5'. This string implicitly
# evaluates to True, so red is assigned to the first part of the or
# expression.

# The green case works because the value in the my_values dictionary is a list
# with one member: an empty string. The empty string implicitly evaluates to
# False, causing the or expression to evaluate to 0.

# The opacity case works because the value in the my_values dictionary is
# missing altogether. The behavior of the get method is to return its second
# argument if the key doesn't exist in the dictionary. The default value in
# this case is a list with one member, an empty string. When opacity isn't
# found in the dictionary, this code does exactly the same thing as the green
# case.

# 
