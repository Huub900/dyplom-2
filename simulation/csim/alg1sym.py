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
        self._phi = eval(self.copula.phistr()).subs(th, copula.th)
        self._k = t - self._phi / diff(self._phi, t)

    def phi(self, arg):
        return self._phi.subs(t, arg).evalf()

    def revphi(self, arg):
        return brenth(lambda x: self.phi(x) - arg, float_info.min, 1.0)

    def k(self, arg):
        return self._k.subs(t, arg).evalf()

    def revk(self, arg):
        return brenth(lambda x: self.k(x) - arg, float_info.min, 1.0)

    def sample(self):
        s, t = uniform(0, 1), uniform(0, 1)

class Gumbel(object):
    def __init__(self, th):
        self.th = th

    def phistr(self):
        return '(-log(t)) ** th'


if __name__ == '__main__':
    alg = AlgISym(Gumbel(5))
    for i in range(10):
        x = uniform(0, 1)
        print alg.revk(x), x - alg.k(alg.revk(x))
