# -*- coding: utf-8 -*-

from copulae import Clayton, Gumbel
from distributions import Normal, Uniform, LogNormal

class Simulation(object):
    def __init__(self, copula, marginal_x=None, marginal_y=None, censoring_x=None, censoring_y=None):
        self.copula = copula
        self.marginal_x = marginal_x
        self.marginal_y = marginal_y
        self.censoring_x = censoring_x
        self.censoring_y = censoring_y

        if marginal_x is not None:
            self.transform_marginal_x = marginal_x.revcdf()
        if marginal_y is not None:
            self.transform_marginal_y = marginal_y.revcdf()

    def transform_marginal_x(self, x):
        return x

    def transform_marginal_y(self, y):
        return y

    def censor_x(self, x):
        return x

    def censor_y(self, y):
        return y

    def sample(self):
        x, y = copula.sample()
        x = self.censoring_x(self.marginal_x(x))
        y = self.censoring_y(self.marginal_y(y))
        return x, y


if __name__ == '__main__':
    copula = Clayton(5)
    simulation = Simulation(copula, marginal_x=Normal(0, 1), marginal_y=Uniform(5))
    print "x,y"
    for i in range(500):
        print "%s,%s" % (simulation.sample())
