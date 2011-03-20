# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *


urlpatterns = patterns('copula.simulation.views',
    url(r'^$', 'start', name='simulation_start'),
    url(r'^new/$', 'new', name='simulation_new'),
    url(r'^distributions/$', 'distributions', name='simulation_distributions'),
    url(r'^distributions/(?P<id>\d+)/$', 'distributions', name='simulation_distributions'),
    url(r'^parameters/(?P<id>\d+)/$', 'parameters', name='simulation_parameters'),
    url(r'^sampling/(?P<id>\d+)/$', 'sampling', name='simulation_sampling'),
    url(r'^sample/(?P<size>\d+)/(?P<format>(xls|csv))', 'sample', name='simulation_sample'),

)