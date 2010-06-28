# -*- coding: utf-8 -*-

from random import uniform
from scipy.stats import norm


class AlgII(object):
    def __init__(self, copula):
        self.copula = copula

    def v(self, u, t):
        w = self.copula.revdphi(self.copula.dphi(u) / t)
        return self.copula.prevphi(self.copula.phi(w) - self.copula.phi(u))


    def sample(self):
        u, t = uniform(0, 1), uniform(0, 1)
        return u, self.v(u, t)


class Copula(object):
    def __init__(self, theta):
        self.theta = theta
        self.phi0 = self.phi(0)

    def revphi(self, t):
        raise NotImplementedError

    def prevphi(self, t):
        return 0 if t >= self.phi0 else self.revphi(t)


class Clayton(object):
    def __init__(self, theta):
        self.theta = float(theta)

    def phi(self, t):
        return (t ** -self.theta - 1) / self.theta

    def revphi(self, t):
        return (self.theta * t + 1) ** (-1 / self.theta)

    def prevphi(self, t):
        return self.revphi(t)

    def dphi(self, t):
        return -(t ** (-self.theta - 1))

    def revdphi(self, t):
        return (-t) ** (1 / (-self.theta - 1))


class Nelsen2(Copula):
    def __init__(self, theta):
        self.theta = float(theta)
        self.phi0 = self.phi(0.0)

    def phi(self, t):
        return (1 - t) ** self.theta

    def revphi(self, t):
        return 1 - t ** (1 / self.theta)

    def prevphi(self, t):
        return self.revphi(t)

    def dphi(self, t):
        return -self.theta * (1 - t) ** (self.theta - 1)

    def revdphi(self, t):
        return 1 - (t / -self.theta) ** (1 / (self.theta - 1))


if __name__ == '__main__':
    #copula = Nelsen2(2.0)
    copula = Clayton(5)
    algII = AlgII(copula)

    for i in range(500):
        p = algII.sample()
        print p[0], p[1]
