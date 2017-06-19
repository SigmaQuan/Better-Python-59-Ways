import gc
found_objects = gc.get_objects()
print('%d objects before' % len(found_objects))


import item_59_use_tracemalloc_waste_memory as waste_memory
x = waste_memory.run()
found_objects = gc.get_objects()
print('%d objects after' % len(found_objects))
for obj in found_objects[:3]:
    print(repr(obj)[:100])

# 4916 objects before
# 5446 objects after
# <class '_ast.withitem'>
# <attribute '__weakref__' of 'withitem' objects>
# {'_fields': ('context_expr', 'optional_vars'), '__doc__': None, '__module__': '_ast', '__weakref__':