# -*- coding: utf-8 -*-

from copulae import Clayton, Gumbel
from distributions import Normal, LogNormal

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
            return x, x < xc
        else:
            return x, False

    def censor_y(self, y):
        if self.censoring_y:
            yc = self.censoring_y.sample()
            return y, y < yc
        else:
            return y, False

    def sample(self):
        x, y = copula.sample()
        #TODO: osobne cenzorowanie każdej zmiennej
        if self.censoring_x:
            x, xd = self.censor_x(self.transform_marginal_x(x))
            y, yd = self.censor_y(self.transform_marginal_y(y))
            return x, xd, y, yd
        else:
            x = self.transform_marginal_x(x)
            y = self.transform_marginal_y(y)
            return x, y


if __name__ == '__main__':
    copula = Clayton(5)
    simulation = Simulation(copula, marginal_x=Normal(0, 1), marginal_y=Normal(0, 1))
    print "x,y"
    for i in range(500):
        print simulation.sample()
