# -*- coding: utf-8 -*-

import math
from random import uniform

# TODO: nie wiem, czy to tak dokładnie ma być
# raczej location + scale
# w przypadku stałego ucinania -- tylko jeden parametr

class Weibull(object):
    def __init__(self, l, k):
        self.l = float(l)
        self.k = float(k)

    def revcdf(self, x):
        return math.log(1 / (1 - x)) ** (1 / self.k) / self.l

    def sample(self):
        return self.revcdf(uniform(0, 1))


class LogNorm(object):
    def __init__(self, m, s):
        self.m = float(m)
        self.s = float(s)

    def revcdf(self, x):
        pass

    def sample(self):
        pass

class Normal(object):
    def __init__(self, m, s):
        self.m = float(m)
        self.s = float(s)

    def revcdf(self, x):
        pass

    def sample(self):
        pass


if __name__ == '__main__':
    w = Weibull(1, 1.5)
    for i in range(500):
        print(w.sample())