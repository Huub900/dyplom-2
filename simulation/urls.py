# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *


urlpatterns = patterns('copula.simulation.views',
    url(r'^$', 'start', name='simulation_start'),
    url(r'^form_1/$', 'form_1', name='simulation_form1'),
)