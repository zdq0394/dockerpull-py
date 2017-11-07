'''
stats ...
'''

import time
from functools import wraps
from collections import defaultdict

Exec_times = "exec_times"
Exec_av_seconds = "exec_av_seconds"

def init_func_stats():
    return {Exec_times: 0, Exec_av_seconds: 0}

FunctionsSecondsDict = defaultdict(init_func_stats)

def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        period = t1-t0
        func_stats = FunctionsSecondsDict[function.func_name]
        func_stats[Exec_av_seconds] = (func_stats[Exec_av_seconds] * func_stats[Exec_times] + period) / (func_stats[Exec_times]+1)
        func_stats[Exec_times] += 1
        FunctionsSecondsDict[function.func_name] = func_stats
        print "Running %s: %s seconds, Average %s seconds" % (function.func_name, str(period), func_stats[Exec_av_seconds])
        return result
    return function_timer 