# -*- coding: utf-8 -*-

from django.db import models
from simulation.csim.copulae import COPULAE
from simulation.csim.distributions import DISTRIBUTIONS


COPULAE_CHOICES = ((cop, COPULAE[cop].name) for cop in COPULAE.keys())
MARGINALS = ('normal', 'weibull', 'lognormal',)
MARGINALS_CHOICES = [(dist, DISTRIBUTIONS[dist].name) for dist in MARGINALS]
CENSORING = ('constant', 'weibull',)
CENSORING_CHOICES = [(dist, DISTRIBUTIONS[dist].name) for dist in MARGINALS]

class Simulation(models.Model):
    copula = models.CharField(u'kopuła', max_length=256, choices=COPULAE_CHOICES)
    marginal_x = models.CharField(u'rozkład brzegowy x', max_length=256, choices=MARGINALS_CHOICES, blank=True)
    marginal_y = models.CharField(u'rozkład brzegowy y', max_length=256, choices=MARGINALS_CHOICES, blank=True)
    censoring_x = models.CharField(u'cenzorowanie x', max_length=256, choices=CENSORING_CHOICES, blank=True)
    censoring_y = models.CharField(u'cenzorowanie y', max_length=256, choices=CENSORING_CHOICES, blank=True)

#class Copula(models.Model):
#    type = models.CharField(max_lenght=256, choices=COPULAE)
#    theta = models.FloatField()
#
#
#class Distribution(models.Model):
#    type = models.CharField(max_length=256)
#    par1 = models.FloatField()
#    par2 = models.FloatField()
#
#
#class Simulation(models.Model):
#    copula = models.ForeignKey(Copula)
#    marginal_x = models.ForeignKey(Distribution)
#    marginal_y = models.ForeignKey(Distribution)
#    censoring_x = models.ForeignKey(Distribution)
#    censoring_y = models.ForeignKey(Distribution)
