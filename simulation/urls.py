# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *


urlpatterns = patterns('copula.simulation.views',
    url(r'^$', 'home', name='simulation_home'),

    # tymczasowe
    url(r'^sample/$', 'sample', name='sample'),
    url(r'^xls_sample/$', 'xls_sample', name='xls_sample'),
    url(r'^csv_sample/$', 'csv_sample', name='csv_sample'),
)