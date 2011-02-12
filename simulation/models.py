# -*- coding: utf-8 -*-

from django.db import models


COPULAE = (
    ('gumbel', 'Gumbel'),
    ('clayton', 'Clayton'),
    ('alimikhailhaq', 'AliMikhailHaq'),
    ('nelsen2', 'Nelsen #2'),
)


MARGINALS = (
    ('normal', 'Normal'),
    ('weibull', 'Weibull'),
    ('lognormal', 'LogNormal'),
)


CENSORING = (
    ('constant', 'Constant'),
    ('weibull', 'Weibull'),
)


class Copula(models.Model):
    type = models.CharField(max_lenght=256, choices=COPULAE)
    theta = models.FloatField()


class Distribution(models.Model):
    type = models.CharField(max_length=256)
    par1 = models.FloatField()
    par2 = models.FloatField()


class Simulation(models.Model):
    copula = models.ForeignKey(Copula)
    marginal_x = models.ForeignKey(Distribution)
    marginal_y = models.ForeignKey(Distribution)
    censoring_x = models.ForeignKey(Distribution)
    censoring_y = models.ForeignKey(Distribution)
