# -*- coding: utf-8 -*-

from random import uniform
from math import log, exp
from scipy.optimize import bisect
from sys import float_info


class CopulaI(object):
    def phi(self, t):
        raise NotImplementedError

    def revphi(self, t):
        return bisect(lambda x: self.phi(x) - t, float_info.min, 1.0)

    def kc(self, t):
        raise NotImplementedError

    def revkc(self, t):
        return bisect(lambda x: self.kc(x) - t, float_info.min, 1.0)

    def sample(self):
        s, t = uniform(0, 1), uniform(0, 1)
        w = self.revkc(t)
        u = self.revphi(s * self.phi(w))
        v = self.revphi((1 - s) * self.phi(w))
        return u, v


class CopulaII(object):
    def phi(self, t):
        raise NotImplementedError

    def revphi(self, t):
        raise NotImplementedError

    def dphi(self, t):
        raise NotImplementedError

    def revdphi(self, t):
        raise NotImplementedError

    def sample(self):
        u, t = uniform(0, 1), uniform(0, 1)
        w = self.revdphi(self.dphi(u) / t)
        v = self.revphi(self.phi(w) - self.phi(u))
        return u, v


class Gumbel(CopulaI):
    def __init__(self, theta):
        self.theta = float(theta)

    def phi(self, t):
        return (-log(t)) ** self.theta

    def revphi(self, t):
        return exp(-t ** (1 / self.theta))

    def kc(self, t):
        return t + t * log(t) / self.theta


class Clayton(CopulaII):
    def __init__(self, theta):
        self.theta = float(theta)

    def phi(self, t):
        return (t ** -self.theta - 1) / self.theta

    def revphi(self, t):
        return (self.theta * t + 1) ** (-1 / self.theta)

    def dphi(self, t):
        return -(t ** (-self.theta - 1))

    def revdphi(self, t):
        return (-t) ** (1 / (-self.theta - 1))


class AliMikhailHaq(CopulaI):
    def __init__(self, theta):
        self.theta = theta

    def phi(self, t):
        return log((1 - self.theta * (1 - t)) / t)

    def kc(self, t):
        a = 1 - self.theta * (1 - t)
        return t - log(a / t) * t * a / (1 + self.theta)


class Nelsen2(object):
    def __init__(self, theta):
        self.theta = theta

    def sample(self):
        th = self.theta
        u, w = uniform(0, 1), uniform(0, 1)
        v = 1 - ((1 - u) ** th * (w ** (th / (1 - th)) - 1) + 1) ** (1 / th)
        return u, v


if __name__ == '__main__':
    copula = AliMikhailHaq(0.9)
    for i in range(500):
        sample = copula.sample()
        print("%s,%s" % (sample[0], sample[1]))

