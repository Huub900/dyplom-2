# -*- coding: utf-8 -*-

from django.forms import ModelForm
from simulation.models import Simulation


class SimulationForm(ModelForm):
    class Meta:
        model = Simulation