import tracemalloc
tracemalloc.start(10)   # Save up to 10 stack frames

time1 = tracemalloc.take_snapshot()
import item_59_use_tracemalloc_waste_memory as waste_memory
x = waste_memory.run()
time2 = tracemalloc.take_snapshot()

stats = time2.compare_to(time1, 'lineno')
for stat in stats[:3]:
    print(stat)

# /home/robot/Documents/PycharmProjects/BetterPython59Ways/item_59_use_tracemalloc_waste_memory.py:7: size=3539 KiB (+3539 KiB), count=100000 (+100000), average=36 B
# /home/robot/Documents/PycharmProjects/BetterPython59Ways/item_59_use_tracemalloc_top_n.py:6: size=1264 B (+1264 B), count=2 (+2), average=632 B
# <frozen importlib._bootstrap_external>:476: size=485 B (+485 B), count=6 (+6), average=81 B
