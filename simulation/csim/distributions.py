# -*- coding: utf-8 -*-

import math
from random import uniform
from scipy import stats


class Distribution(object):
    def __init__(self):
        raise Exception("Klasa abstrakcyjna.")

    def revcdf(self, x):
        return self.dist.ppf(x)

    def sample(self):
        return self.dist.rvs()


class Weibull(Distribution):
    name = u'weibulla'
    parameters = (
        {'name': u'parametr skali', 'min': 0.0,},
        {'name': u'paremetr kształtu', 'min': 0.0}
    )

    def __init__(self, params):
        self.l = float(params[0])
        self.k = float(params[1])

    def revcdf(self, x):
        return math.log(1 / (1 - x)) ** (1 / self.k) / self.l

    def sample(self):
        return self.revcdf(uniform(0, 1))


class LogNormal(Distribution):
    name = u'logarytmicznie normalny'
    parameters = (
        {'name': u'parametr kształtu', 'min': 0.0},
        {'name': u'parametr skali', 'min': 0.0},
    )

    def __init__(self, *params):
        self.dist = stats.lognorm(float(params[0]), scale=float(params[1]))


class Normal(Distribution):
    name = u'normalny'
    parameters = (
        {'name': u'wartość oczekiwana',},
        {'name': u'wariancja', 'min': 0.0,},
    )

    def __init__(self, *params):
        self.dist = stats.norm(loc=float(params[0]), scale=float(params[1]))


class Uniform(Distribution):
    name = u'jednostajny'
    parameters = (
        {'name': u'górna granica', 'min': 0.0,},
    )
    def __init__(self, *params):
        self.tmax = float(params[0])

    def sample(self):
        return uniform(0, self.tmax)


class Constant(Distribution):
    name = u'jednopunktowy' # wstęp do teorii prawdopodobieństwa
    parameters = (
        {'name': u'wartość', 'min': 0.0,},
    )
    def __init__(self, *params):
        self.c = params[0]

    def sample(self):
        return self.c


if __name__ == '__main__':
    w = Constant(3)
    for i in range(500):
        print(w.sample())