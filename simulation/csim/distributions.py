# -*- coding: utf-8 -*-

import math
from random import uniform
from scipy import stats

# TODO: nie wiem, czy to tak dokładnie ma być
# raczej location + scale
# w przypadku stałego ucinania -- tylko jeden parametr

class Distribution(object):
    def __init__(self):
        raise Exception("Klasa abstrakcyjna.")

    def revcdf(self, x):
        return self.dist.ppf(x)

    def sample(self):
        return self.dist.rvs()


class Weibull(Distribution):
    def __init__(self, l, k):
        self.l = float(l)
        self.k = float(k)

    def revcdf(self, x):
        return math.log(1 / (1 - x)) ** (1 / self.k) / self.l

    def sample(self):
        return self.revcdf(uniform(0, 1))


class LogNorm(Distribution):
    def __init__(self, *args):
        self.dist = stats.lognorm(float(args[0]), scale=float(args[1]))


class Normal(Distribution):
    def __init__(self, *args):
        self.dist = stats.norm(loc=float(args[0]), scale=float(args[1]))


if __name__ == '__main__':
    w = Weibull(1, 1.5)
    for i in range(500):
        print(w.sample())