# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError

from django.forms import ModelForm
from simulation.csim.copulae import COPULAE
from simulation.csim.distributions import DISTRIBUTIONS
from simulation.models import Simulation


class DistributionsForm(ModelForm):
    class Meta:
        model = Simulation
        fields = ['copula', 'marg_x', 'marg_y', 'cens_x', 'cens_y']


class ParametersForm(ModelForm):
    class Meta:
        model = Simulation
        fields = ['theta',
                  'marg_x_par_0', 'marg_x_par_1',
                  'marg_y_par_0', 'marg_y_par_1',
                  'cens_x_par_0', 'cens_x_par_1',
                  'cens_y_par_0', 'cens_y_par_1']


class ParameterValidator(object):
    def __init__(self, parameter):
        self.min = parameter.get('min')
        self.max = parameter.get('max')
        self.excludes = parameter.get('excludes', [])

    def __call__(self, value):
        if self.min is not None and value < self.min:
            raise ValidationError('Minimalna dopuszczalna wartość: %s' % self.min)
        if self.max is not None and value > self.max:
            raise ValidationError('Maksymalna dopuszczalna wartość: %s' % self.max)
        if value in self.excludes:
            raise ValidationError('Niedozwolona wartość parametru')


def parameters_form_factory(data=None, instance=None):
    if instance is None:
        raise Exception('Wymagany argument "instance"')

    form = ParametersForm(data=data, instance=instance)

    copula = COPULAE[instance.copula]
    form.fields['theta'].validators = [ParameterValidator(copula.parameter)]

    for dist_type in ('marg_x', 'marg_y', 'cens_x', 'cens_y'):
        if instance.__getattribute__(dist_type):
            dist = DISTRIBUTIONS[instance.__getattribute__(dist_type)]
            for i in range(len(dist.parameters)):
                form.fields[dist_type + '_par_%s' % i].label = dist.parameters[i]['name']
                form.fields[dist_type + '_par_%s' % i].validators = [ParameterValidator(dist.parameters[i]),]
            if i == 0:
                del form.fields[dist_type + '_par_1']
        else:
            del form.fields[dist_type + '_par_0']
            del form.fields[dist_type + '_par_1']

    return form
