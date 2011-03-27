# -*- coding: utf-8 -*-

from random import uniform
from math import log, exp
from scipy.optimize import bisect
from sys import float_info


class Copula(object):
    def __init__(self, theta):
        self.theta = float(theta)


class CopulaI(Copula):
    def phi(self, t):
        raise NotImplementedError

    def dphi(self, t):
        raise NotImplementedError

    def revphi(self, t):
        return bisect(lambda x: self.phi(x) - t, float_info.min, 1.0)

    def kc(self, t):
        return t - self.phi(t) / self.dphi(t)

    def revkc(self, t):
        return bisect(lambda x: self.kc(x) - t, float_info.min, 1.0)

    def sample(self):
        s, t = uniform(0, 1), uniform(0, 1)
        w = self.revkc(t)
        u = self.revphi(s * self.phi(w))
        v = self.revphi((1.0 - s) * self.phi(w))
        return u, v


class CopulaII(Copula):
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
    name = 'Gumbel'
    parameter = {'mini': 1.0}

    def phi(self, t):
        return (-log(t)) ** self.theta

    def revphi(self, t):
        return exp(-t ** (1.0 / self.theta))

    def kc(self, t):
        return t + t * log(t) / self.theta


class Clayton(CopulaII):
    name = 'Clayton'
    parameter = {'mini': -1.0, 'excludes': [0.0,]}

    def phi(self, t):
        return (t ** -self.theta - 1.0) / self.theta

    def revphi(self, t):
        return (self.theta * t + 1.0) ** (-1.0 / self.theta)

    def dphi(self, t):
        return -(t ** (-self.theta - 1.0))

    def revdphi(self, t):
        return (-t) ** (1.0 / (-self.theta - 1.0))


class AliMikhailHaq(CopulaI):
    name = 'Ali-Mikhail-Haq'
    parameter = {'mini': -1.0, 'maxe': 1.0}

    def num(self, t):
        return 1.0 - self.theta * (1.0 - t)

    def phi(self, t):
        return log(self.num(t) / t)

    def kc(self, t):
        a = self.num(t)
        return t - log(a / t) * t * a / (self.theta - 1.0)


#class Nelsen2(CopulaI):
#    name = 'Nelsen #2'
#    parameter = {'mini': 1.0}
#
#    def phi(self, t):
#        return (1.0 - t) ** self.theta
#
#    def revphi(self, t):
#        return 1.0 - t ** (1.0 / self.theta)
#
#    def kc(self, t):
#        return 0.0 if t <= 1.0 else t + (1.0 - t) * self.theta
#
#    def revkc(self, t):
#        return (self.theta * t- 1.0) / (self.theta - 1.0)


class Frank(CopulaII):
    name = 'Frank'
    parameter = {'excludes': [0.0,]}

    def __init__(self, theta):
        self.theta = float(theta)
        self.den = exp(-self.theta) - 1.0

    def phi(self, t):
        return -log((exp(-self.theta * t) - 1.0) / self.den)

    def revphi(self, t):
        return -log(exp(-t) * self.den + 1.0) / self.theta

    def dphi(self, t):
        return self.theta * (1.0 + 1.0 / (exp(-self.theta * t) - 1.0))

    def revdphi(self, t):
        return log((t - self.theta) / t) / self.theta


COPULAE = {
    'gumbel': Gumbel,
    'clayton': Clayton,
    'alimikhailhaq': AliMikhailHaq,
    #'nelsen2': Nelsen2,
    'frank': Frank,
}
