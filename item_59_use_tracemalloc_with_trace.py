import tracemalloc
tracemalloc.start(10)   # Save up to 10 stack frames

time1 = tracemalloc.take_snapshot()
import item_59_use_tracemalloc_waste_memory as waste_memory
x = waste_memory.run()
time2 = tracemalloc.take_snapshot()

stats = time2.compare_to(time1, 'traceback')
top = stats[0]
print('\n'.join(top.traceback.format()))

# File "/home/robot/Documents/PycharmProjects/BetterPython59Ways/item_59_use_tracemalloc_waste_memory.py", line 7
#     a.append(10 * 230 * i)
#   File "/home/robot/Documents/PycharmProjects/BetterPython59Ways/item_59_use_tracemalloc_with_trace.py", line 6
#     x = waste_memory.run()