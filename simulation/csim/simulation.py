# -*- coding: utf-8 -*-


class Simulation(object):
    def __init__(self, copula, marginal_x=None, marginal_y=None, censoring_x=None, censoring_y=None):
        self.copula = copula
        self.marginal_x = marginal_x if marginal_x else lambda t: t
        self.marginal_y = marginal_y if marginal_y else lambda t: t
        self.censoring_x = censoring_x if censoring_x else lambda t: t
        self.censoring_y = censoring_y if censoring_y else lambda t: t

