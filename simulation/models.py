# -*- coding: utf-8 -*-

from django.db import models
from simulation.csim.copulae import COPULAE
from simulation.csim.distributions import DISTRIBUTIONS
from simulation.csim import simulation


COPULAE_CHOICES = sorted(((cop, COPULAE[cop].name) for cop in COPULAE.keys()))
MARGINALS = ('normal', 'weibull', 'lognormal',)
MARGINALS_CHOICES = sorted([(dist, DISTRIBUTIONS[dist].name) for dist in MARGINALS])
CENSORING = ('constant', 'weibull',)
CENSORING_CHOICES = sorted([(dist, DISTRIBUTIONS[dist].name) for dist in CENSORING])


class Simulation(models.Model):
    copula = models.CharField(u'kopuła', max_length=256, choices=COPULAE_CHOICES)
    theta = models.FloatField(u'theta', null=True)
    marg_x = models.CharField(u'rozkład brzegowy x', max_length=256, choices=MARGINALS_CHOICES, blank=True)
    marg_x_par_0 = models.FloatField(null=True)
    marg_x_par_1 = models.FloatField(null=True)
    marg_y = models.CharField(u'rozkład brzegowy y', max_length=256, choices=MARGINALS_CHOICES, blank=True)
    marg_y_par_0 = models.FloatField(null=True)
    marg_y_par_1 = models.FloatField(null=True)
    cens_x = models.CharField(u'cenzorowanie x', max_length=256, choices=CENSORING_CHOICES, blank=True)
    cens_x_par_0 = models.FloatField(null=True)
    cens_x_par_1 = models.FloatField(null=True)
    cens_y = models.CharField(u'cenzorowanie y', max_length=256, choices=CENSORING_CHOICES, blank=True)
    cens_y_par_0 = models.FloatField(null=True)
    cens_y_par_1 = models.FloatField(null=True)
    valid = models.BooleanField(default=False)

    def create_simulation_object(self):
        copula_dist = COPULAE[self.copula](self.theta)
        marg_x_dist = None
        if self.marg_x:
            marg_x_args = [self.marg_x_par_0,]
            if len(self.marg_x_parameters) == 2:
                marg_x_args.append(self.marg_x_par_1)
            marg_x_dist = DISTRIBUTIONS[self.marg_x](*marg_x_args)
        marg_y_dist = None
        if self.marg_y:
            marg_y_args = [self.marg_y_par_0,]
            if len(self.marg_y_parameters) == 2:
                marg_y_args.append(self.marg_y_par_1)
            marg_y_dist = DISTRIBUTIONS[self.marg_y](*marg_y_args)
        cens_x_dist = None
        if self.cens_x:
            cens_x_args = [self.cens_x_par_0,]
            if len(self.cens_x_parameters) == 2:
                cens_x_args.append(self.cens_x_par_1)
            cens_x_dist = DISTRIBUTIONS[self.cens_x](*cens_x_args)
        cens_y_dist = None
        if self.cens_y:
            cens_y_args = [self.cens_y_par_0,]
            if len(self.cens_y_parameters) == 2:
                cens_y_args.append(self.cens_y_par_1)
            cens_y_dist = DISTRIBUTIONS[self.cens_y](*cens_y_args)
        return simulation.Simulation(copula_dist, marg_x_dist, marg_y_dist, cens_x_dist, cens_y_dist)

    def sample(self, size):
        simulation_object = self.create_simulation_object()
        return (simulation_object.sample() for i in range(size))

    @property
    def copula_name(self):
        return COPULAE[self.copula].name

    @property
    def copula_parameter(self):
        return COPULAE[self.copula].parameter

    @property
    def marg_x_name(self):
        return DISTRIBUTIONS[self.marg_x].name if self.marg_x else None

    @property
    def marg_x_parameters(self):
        return DISTRIBUTIONS[self.marg_x].parameters if self.marg_x else None

    @property
    def marg_y_name(self):
        return DISTRIBUTIONS[self.marg_y].name if self.marg_y else None

    @property
    def marg_y_parameters(self):
        return DISTRIBUTIONS[self.marg_y].parameters if self.marg_y else None

    @property
    def cens_x_name(self):
        return DISTRIBUTIONS[self.cens_x].name if self.cens_x else None

    @property
    def cens_x_parameters(self):
        return DISTRIBUTIONS[self.cens_x].parameters if self.cens_x else None

    @property
    def cens_y_name(self):
        return DISTRIBUTIONS[self.cens_y].name if self.cens_y else None

    @property
    def cens_y_parameters(self):
        return DISTRIBUTIONS[self.cens_y].parameters if self.cens_y else None
