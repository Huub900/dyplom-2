# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *


urlpatterns = patterns('copula.simulation.views',
    url(r'^$', 'home', name='simulation_home'),
)