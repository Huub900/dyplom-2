# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError

from django import forms
from simulation.csim.copulae import COPULAE
from simulation.csim.distributions import DISTRIBUTIONS
from simulation.models import Simulation


class DistributionsForm(forms.ModelForm):
    class Meta:
        model = Simulation
        fields = ['copula', 'marg_x', 'marg_y', 'cens_x', 'cens_y']


class ParametersForm(forms.ModelForm):
    class Meta:
        model = Simulation
        fields = ['theta',
                  'marg_x_par_0', 'marg_x_par_1',
                  'marg_y_par_0', 'marg_y_par_1',
                  'cens_x_par_0', 'cens_x_par_1',
                  'cens_y_par_0', 'cens_y_par_1']


SAMPLE_FORMAT_CHOICES = (
    ('csv', 'CSV - tekst rozdzielany przecinkami'),
    ('xsl', 'XLS - arkusz MS Excel'),
)

class SamplingForm(forms.Form):
    sample_size = forms.IntegerField(label=u'wielkość próbki', min_value=10, max_value=500)
    sample_format = forms.ChoiceField(label='format danych', choices=SAMPLE_FORMAT_CHOICES)


class ParameterValidator(object):
    def __init__(self, parameter):
        self.mini = parameter.get('mini')
        self.mine = parameter.get('mine')
        self.maxi = parameter.get('maxi')
        self.maxe = parameter.get('maxe')
        self.excludes = parameter.get('excludes', [])

    def __call__(self, value):
        if self.mini is not None and value < self.mini:
            raise ValidationError('Wartość nie może być mniejsza od %s' % self.mini)
        if self.mine is not None and value <= self.mine:
            raise ValidationError('Wartość musi być większa od %s' % self.mine)
        if self.maxi is not None and value > self.maxi:
            raise ValidationError('Wartość nie może być większa od %s' % self.maxi)
        if self.maxe is not None and value >= self.maxe:
            raise ValidationError('Wartość musi być mniejsza od %s' % self.maxe)
        if value in self.excludes:
            raise ValidationError('Wartość musi być różna od %s' % value)


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
                form.fields[dist_type + '_par_%s' % i].label = dist.parameters[i]['name'].capitalize()
                form.fields[dist_type + '_par_%s' % i].validators = [ParameterValidator(dist.parameters[i]),]
            if i == 0:
                del form.fields[dist_type + '_par_1']
        else:
            del form.fields[dist_type + '_par_0']
            del form.fields[dist_type + '_par_1']

    return form
