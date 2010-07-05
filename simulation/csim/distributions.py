# -*- coding: utf-8 -*-

import math
from random import uniform


class Weibull(object):
    def __init__(self, l, k):
        self.l = float(l)
        self.k = float(k)

    def revcdf(self, x):
        return math.log(1 / (1 - x)) ** (1 / self.k) / self.l

    def sample(self):
        return self.revcdf(uniform(0, 1))


if __name__ == '__main__':
    w = Weibull(1, 1.5)
    for i in range(500):
        print(w.sample())