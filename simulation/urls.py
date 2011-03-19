# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *


urlpatterns = patterns('copula.simulation.views',
    url(r'^$', 'start', name='simulation_start'),
    url(r'^distributions/$', 'distributions', name='simulation_distributions'),
    url(r'^parameters/$', 'parameters', name='simulation_parameters'),
    url(r'^new/$', 'new', name='simulation_new'),
)