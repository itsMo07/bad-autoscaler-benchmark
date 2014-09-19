#!/usr/bin/env python3

# This is a tool to test if your cpu has bad autoscaling.  First it runs a single-threaded benchmark meant to max out 
# a single core of a CPU.  Then it repeats the same benchmark but runs it concurrently with multiple junk processes 
# designed to waste the other cores.

# A bad autoscaler will get a FASTER result for the second test.  The reason is that a bad "on demand" autoscaler
# won't detect the first case as something needing upscaling, since only one core is busy and the CPU hasn't hit
# some overall core-usage threshold to be "in use"

from math import sqrt
from timeit import timeit
import subprocess
import multiprocessing

LENGTH = 10000
TRIALS = 10000
number_of_cores = multiprocessing.cpu_count()

def benchmark():
    for x in range(LENGTH):
        y = sqrt(x)

def test():
    return timeit(benchmark, number=TRIALS)

print("Benchmark running alone:")
solo_result = test()
print(solo_result)

processes = set()
anomolies = []

for wasted_cores in range(1,number_of_cores):
    processes.add(subprocess.Popen("while :; do :; done", shell=True))
    print("Benchmark running alongside", wasted_cores, "waste processes:")
    result = test()
    if result < solo_result:
        print(result, "***")
        anomolies.append(wasted_cores)
    else:
        print(result)

for x in processes:
    x.kill()

for x in anomolies:
    print("Faster results due to possible bad autoscaler found when running with", x, "waste processes!")
