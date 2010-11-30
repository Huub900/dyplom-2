# -*- coding: utf-8 -*-

from django.db import models


class Simulation(models.Model):
    algorithm = models.CharField(u'algorytm', max_length=256)
    copula = models.CharField(u'kopuła', max_length=256)
    theta = models.FloatField()
    marginal_u = models.CharField(u'rozkład brzegowy u', max_length=256)
    marginal_v = models.CharField(u'rozkład brzegowy u', max_length=256)
    censoring = models.CharField(u'cenzorowanie', max_length=256)

    class Meta:
        verbose_name = 'symulacja'
        verbose_name_plural = 'symulacje'