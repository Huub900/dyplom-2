# -*- coding: utf-8 -*-

from random import uniform
from math import log, exp
from scipy.optimize import bisect
from sys import float_info


class CopulaI(object):
    def __init__(self, theta):
        self.theta = float(theta)

    def phi(self, t):
        raise NotImplementedError

    def dphi(self, t):
        raise NotImplementedError

    def revphi(self, t):
        return bisect(lambda x: self.phi(x) - t, float_info.min, 1.0)

    def kc(self, t):
        print t, self.dphi(t)
        return t - self.phi(t) / self.dphi(t)

    def revkc(self, t):
        return bisect(lambda x: self.kc(x) - t, float_info.min, 1.0)

    def sample(self):
        s, t = uniform(0, 1), uniform(0, 1)
        w = self.revkc(t)
        u = self.revphi(s * self.phi(w))
        v = self.revphi((1.0 - s) * self.phi(w))
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
        return exp(-t ** (1.0 / self.theta))

    def kc(self, t):
        return t + t * log(t) / self.theta


class Clayton(CopulaII):
    def __init__(self, theta):
        self.theta = float(theta)

    def phi(self, t):
        return (t ** -self.theta - 1.0) / self.theta

    def revphi(self, t):
        return (self.theta * t + 1.0) ** (-1.0 / self.theta)

    def dphi(self, t):
        return -(t ** (-self.theta - 1.0))

    def revdphi(self, t):
        return (-t) ** (1.0 / (-self.theta - 1.0))


class AliMikhailHaq(CopulaI):
    def phi(self, t):
        return log((1.0 - self.theta * (1.0 - t)) / t)

    def kc(self, t):
        a = 1.0 - self.theta * (1.0 - t)
        return t - log(a / t) * t * a / (1.0 + self.theta)


class Nelsen2(CopulaI):
    def phi(self, t):
        return (1.0 - t) ** self.theta

    def revphi(self, t):
        return 1.0 - t ** (1.0 / self.theta)

    def kc(self, t):
        return 0.0 if t <= 1.0 else t + (1.0 - t) * self.theta

    def revkc(self, t):
        return (self.theta * t- 1.0) / (self.theta - 1.0)


class Nelsen22(object):
    def __init__(self, theta):
        self.theta = float(theta)

    def sample(self):
        th = self.theta
        u, w = uniform(0, 1), uniform(0, 1)
        v = 1.0 - ((w ** (th / (1.0 - th)) - 1.0) * (1.0 - u) ** th) ** (1.0 / th)
        return u, v


if __name__ == '__main__':
    copula = Nelsen22(3)
    for i in range(500):
        sample = copula.sample()
        print("%s,%s" % (sample[0], sample[1]))

