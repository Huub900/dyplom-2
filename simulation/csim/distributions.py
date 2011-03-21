# -*- coding: utf-8 -*-

import math
from scipy import stats
from random import uniform


class Distribution(object):
    def __init__(self):
        raise Exception("Klasa abstrakcyjna.")

    def revcdf(self, x):
        return self.dist.ppf(x)

    def sample(self):
        return self.dist.rvs()


class Weibull(Distribution):
    name = u'Weibulla'
    parameters = (
        {'name': u'parametr skali', 'mine': 0.0,},
        {'name': u'parametr kształtu', 'mine': 0.0}
    )

    def __init__(self, *params):
        self.l = float(params[0])
        self.k = float(params[1])

    def revcdf(self, x):
        return self.l * (-math.log(1 - x)) ** (1 / self.k)

    def sample(self):
        return self.revcdf(uniform(0, 1))


class LogNormal(Distribution):
    name = u'logarytmicznie normalny'
    parameters = (
        {'name': u'parametr kształtu', 'mine': 0.0},
        {'name': u'parametr skali', 'mine': 0.0},
    )

    def __init__(self, *params):
        self.dist = stats.lognorm(float(params[0]), loc=0, scale=float(params[1]))


class Normal(Distribution):
    name = u'normalny'
    parameters = (
        {'name': u'wartość oczekiwana',},
        {'name': u'wariancja', 'mine': 0.0,},
    )

    def __init__(self, *params):
        self.dist = stats.norm(loc=float(params[0]), scale=float(params[1]))


class Constant(Distribution):
    name = u'jednopunktowy' # wstęp do teorii prawdopodobieństwa
    parameters = (
        {'name': u'wartość', 'mine': 0.0,},
    )
    def __init__(self, *params):
        self.c = params[0]

    def sample(self):
        return self.c


DISTRIBUTIONS = {
    'constant': Constant,
    'normal': Normal,
    'lognormal': LogNormal,
    'weibull': Weibull,
}
