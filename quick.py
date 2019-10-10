#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@author: d00ms(--)
@file: quick.py
@time: 2019-7-12 15:34
@desc:
"""

from copy import deepcopy

# we assume the time unit is -- 1
if __name__ == '__main__':
    A=[0,3,4,6,1,5]
    B=[2,5,7,7,3,8]

    copyA= deepcopy(A)
    copyB= deepcopy(B)
    copyA.sort()
    copyB.sort(reverse=True)

    start = copyA[0]
    end = copyB[0]

    N = len(A)
    def hit(time):
        ret = 0
        for i in range(N):
            if time>=A[i] and time<=B[i]:
                ret += 1
        return ret
    # every entry is a tuple( start, end, hits )
    intervals = []
    s, e, max = start, start, hit(start)
    step = 0.5
    time = start + step
    while time < end-step:
        if hit(time)> max and hit(time+ 0.5)> hit(time- 0.5):
            s, max = time, hit(time)
        elif hit(time+0.5) < hit(time-0.5):
            e = time
            intervals.append((s, e, max))
            s = e
        time += step
    print("the most exciting intervals are {}-{}, the number is {}".format(*intervals[-1]))
