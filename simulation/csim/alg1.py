from scipy.optimize import brenth
from sys import float_info
from math import log
from random import uniform

class AlgI(object):
    def __init__(self, copula):
        self.copula = copula

    def sample(self, size):
        pass

class Gumbel(object):
    def __init__(self, theta):
        self.theta = theta

    def phi(self, t):
        return (-log(t)) ** self.theta

    def revphi(self, t):
        pass

    def kc(self,t):
        return t - t * log(t) / self.theta

    def revkc(self, t):
        def fn(x):
            return self.kc(x) - t
        return brenth(fn, float_info.min, 1.0)

    def uv(self, s, t):
        pass

for i in range(100):
    copula = Gumbel(5)
    u = uniform(0, 1)
    t = copula.revkc(u)
    print u - copula.kc(t)
