# -*- coding: utf-8 -*-

from django.forms import ModelForm
from simulation.models import Simulation


class DistributionsForm(ModelForm):
    class Meta:
        model = Simulation