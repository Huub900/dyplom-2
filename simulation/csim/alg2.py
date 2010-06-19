# -*- coding: utf-8 -*-

from random import uniform
from scipy.stats import norm

class AlgII(object):
    def __init__(self, copula):
        self.copula = copula

    def sample(self, size):
        for i in range(size):
            u, t = uniform(0, 1), uniform(0, 1)
            yield u, self.copula.v(u, t)

class Clayton(object):
    def __init__(self, theta):
        self.theta = float(theta)

    def v(self, u, t):
        th = self.theta
        return pow(pow(u, -th) * pow(t, -th / (th + 1.0)) - pow(u, -th) + 1.0, -1.0 / th)


if __name__ == '__main__':
    algII = AlgII(Clayton(-0.5))

    for point in algII.sample(1000):
        print norm.ppf(point[0]), norm.ppf(point[1])
