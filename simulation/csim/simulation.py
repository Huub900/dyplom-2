# -*- coding: utf-8 -*-

from copulae import Clayton, Gumbel
from distributions import Normal, LogNormal, Constant

class Simulation(object):
    def __init__(self, copula, marginal_x=None, marginal_y=None, censoring_x=None, censoring_y=None):
        self.copula = copula
        self.marginal_x = marginal_x
        self.marginal_y = marginal_y
        self.censoring_x = censoring_x
        self.censoring_y = censoring_y

    def transform_marginal_x(self, x):
        if self.marginal_x:
            return self.marginal_x.revcdf(x)
        else:
            return x

    def transform_marginal_y(self, y):
        if self.marginal_y:
            return self.marginal_y.revcdf(y)
        else:
            return y

    def censor_x(self, x):
        if self.censoring_x:
            xc = self.censoring_x.sample()
            return min(x, xc), 1 if x < xc else 0
        else:
            return x, 1

    def censor_y(self, y):
        if self.censoring_y:
            yc = self.censoring_y.sample()
            return min(y, yc), 1 if y < yc else 0
        else:
            return y, 1

    def sample(self):
        x, y = self.copula.sample()
        if self.censoring_x or self.censoring_y:
            x, xd = self.censor_x(self.transform_marginal_x(x))
            y, yd = self.censor_y(self.transform_marginal_y(y))
            return x, xd, y, yd
        else:
            x = self.transform_marginal_x(x)
            y = self.transform_marginal_y(y)
            return x, y
