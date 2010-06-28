# -*- coding: utf-8 -*-

from sympy import *
from random import uniform
from sys import float_info
from scipy.optimize import brenth
from random import uniform


t = Symbol('t')
th = Symbol('th')


class AlgISym(object):
    def __init__(self, copula):
        self.copula = copula
        self._phi = eval(self.copula.phistr()).subs(th, copula.theta)
        self._k = t - self._phi / diff(self._phi, t)

    def phi(self, arg):
        return self._phi.subs(t, arg).evalf()

    def revphi(self, arg):
        if t >= self.phi(0):
            return 0
        else:
            return brenth(lambda x: self.phi(x) - arg, float_info.min, 1.0)

    def k(self, arg):
        return self._k.subs(t, arg).evalf()

    def revk(self, arg):
        return brenth(lambda x: self.k(x) - arg, float_info.min, 1.0)

    def sample(self):
        try:
            s, r = uniform(0, 1), uniform(0, 1)
            w = self.revk(r)
            print s, w, s * self.phi(w)
            u = self.revphi(s * self.phi(w))
            v = self.revphi((1 - s) * self.phi(w))
            return u, v
        except:
            pass


class Copula(object):
    def __init__(self, theta):
        self.theta = theta


class Gumbel(Copula):
    def phistr(self):
        return '(-log(t)) ** th'


class Clayton(Copula):
    def phistr(self):
        return '(t ** -th - 1) / th'


class Nelsen2(Copula):
    def phistr(self):
        return '(1 - t) ** th'


class Frank(Copula):
    def phistr(self):
        return '-log((exp(-th * t) - 1) / ( exp(-th) - 1))'


if __name__ == '__main__':
    alg = AlgISym(Nelsen2(10))
    for i in range(100):
        print alg.sample()
