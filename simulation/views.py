# -*- coding: utf-8 -*-

import csv
from django.core.urlresolvers import reverse
from csim import copulae
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from xlwt import Workbook
from simulation.forms import DistributionsForm, ParametersForm, parameters_form_factory
from simulation.models import Simulation


def start(request):
    return HttpResponseRedirect(reverse('simulation_distributions'))


def distributions(request):
    if request.method == 'POST':
        form = DistributionsForm(request.POST)
        if form.is_valid():
            simulation = form.save()
            request.session['simulation_id'] = simulation.id
            return HttpResponseRedirect(reverse('simulation_parameters'))
    else:
        form = DistributionsForm()

    template = 'distributions.xhtml'
    data = {
        'form': form,
    }

    return render_to_response(template,
                              data,
                              context_instance=RequestContext(request))


def parameters(request):
    if request.session.has_key('simulation_id'):
        simulation = Simulation.objects.get(id=request.session['simulation_id'])
    else:
        return HttpResponseRedirect(reverse('simulation_distributions'))

    if request.method == 'POST':
        form = parameters_form_factory(request.POST, instance=simulation)
        if form.is_valid():
            form.save()
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


def new(request):
    if request.session.has_key('simulation_id'):
        simulation = Simulation.objects.get(id=request.session['simulation_id'])
        simulation.delete()
        del request.session['simulation_id']

    return HttpResponseRedirect(reverse('simulation_distributions'))


def home(request):
    menu = {
        'algorytm 1': "#",
        'algorytm 2': "#",
    }
    template = 'start.xhtml'
    data = {
        'menu': menu,
    }
    return render_to_response(template,
                              data,
                              context_instance=RequestContext(request))


def sample(request):
    copula = copulae.Clayton(5)
    data = {
        'samples': (copula.sample() for i in range(500))
    }
    return render_to_response('sample.xhtml',
                              data,
                              context_instance=RequestContext(request))


def xls_sample(request):
    copula = copulae.Clayton(5)
    return render_xls((copula.sample() for i in range(500)))


def render_xls(samples):
    w = Workbook()
    ws = w.add_sheet('simulation')
    rowcount = 0
    for sample in samples:
        ws.write(rowcount, 0, sample[0])
        ws.write(rowcount, 1, sample[1])
        rowcount += 1

    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=simulation.xls'
    w.save(response)

    return response


def csv_sample(request):
    copula = copulae.Clayton(5)
    return render_csv((copula.sample() for i in range(500)))


def render_csv(samples):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=simulation.csv'

    writer = csv.writer(response)
    for sample in samples:
        writer.writerow(sample)

    return response
