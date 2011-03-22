# -*- coding: utf-8 -*-

import csv
from django.core.urlresolvers import reverse
from csim import copulae
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from xlwt import Workbook
from simulation.forms import DistributionsForm, ParametersForm, parameters_form_factory, SamplingForm
from simulation.models import Simulation


def start(request):
    success = False
    try:
        simulation = Simulation.objects.get(id=request.session.get('simulation_id'))
        if simulation.valid:
            success = True
    except Simulation.DoesNotExist:
        pass

    if success:
        return HttpResponseRedirect(reverse('simulation_sampling', kwargs={'id': simulation.id}))
    else:
        return HttpResponseRedirect(reverse('simulation_new'))


def help(request):
    template = 'help.xhtml'
    data = {}
    return render_to_response(template,
                              data,
                              context_instance=RequestContext(request))


def new(request):
    if request.session.has_key('simulation_id'):
        try:
            simulation = Simulation.objects.get(id=request.session['simulation_id'])
            simulation.delete()
        except Simulation.DoesNotExist:
            pass

        del request.session['simulation_id']

    return HttpResponseRedirect(reverse('simulation_distributions'))


def distributions(request, id=None):
    simulation = None
    try:
        simulation = Simulation.objects.get(id=id)
    except Simulation.DoesNotExist:
        pass

    if request.method == 'POST':
        form = DistributionsForm(request.POST, instance=simulation)
        if form.is_valid():
            simulation = form.save()
            request.session['simulation_id'] = simulation.id
            return HttpResponseRedirect(reverse('simulation_parameters', kwargs={'id': simulation.id}))
    else:
        form = DistributionsForm(instance=simulation)

    template = 'distributions.xhtml'
    data = {
        'form': form,
    }

    return render_to_response(template,
                              data,
                              context_instance=RequestContext(request))


def parameters(request, id):
    try:
        simulation = Simulation.objects.get(id=id)
    except Simulation.DoesNotExist:
        return HttpResponseRedirect(reverse('simulation_new'))

    if request.method == 'POST':
        form = parameters_form_factory(request.POST, instance=simulation)
        if form.is_valid():
            simulation = form.save()
            simulation.valid = True
            simulation.save()
            return HttpResponseRedirect(reverse('simulation_sampling', kwargs={'id': simulation.id}))
    else:
        form = parameters_form_factory(instance=simulation)

    template = 'parameters.xhtml'
    data = {
        'simulation': simulation,
        'form': form,
    }

    return render_to_response(template,
                              data,
                              context_instance=RequestContext(request))


def sampling(request, id):
    try:
        simulation = Simulation.objects.get(id=id)
        if not simulation.valid:
            return HttpResponseRedirect(reverse('simulation_new'))
    except Simulation.DoesNotExist:
        return HttpResponseRedirect(reverse('simulation_new'))

    if request.method == 'POST':
        form = SamplingForm(request.POST)
        if form.is_valid():
            sample_size = form.cleaned_data['sample_size']
            sample_format = form.cleaned_data['sample_format']
            if sample_format == 'xls':
                return render_xls(simulation.sample(sample_size))
            elif sample_format == 'csv':
                return render_csv(simulation.sample(sample_size))
            else:
                raise Exception(u'Nieobsługiwany format wyjściowy: %s' % sample_format)
    else:
        form = SamplingForm()

    template = 'sampling.xhtml'
    data = {
        'simulation': simulation,
        'form': form,
        }

    return render_to_response(template,
                              data,
                              context_instance=RequestContext(request))


def render_xls(samples):
    samples = list(samples)
    w = Workbook()
    ws = w.add_sheet('simulation')
    columncount = len(samples[0])
    row = 0
    for sample in samples:
        for column in range(columncount):
            ws.write(row, column, sample[column])
        row += 1

    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=simulation.xls'
    w.save(response)

    return response


def render_csv(samples):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=simulation.csv'

    writer = csv.writer(response)
    for sample in samples:
        writer.writerow(sample)

    return response
