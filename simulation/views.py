# -*- coding: utf-8 -*-

import csv

from csim import alg2
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from xlwt import Workbook


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
    alg = alg2.AlgII(alg2.Clayton(5))
    data = {
        'samples': (alg.sample() for i in range(500))
    }
    return render_to_response('sample.xhtml',
                              data,
                              context_instance=RequestContext(request))


def xls_sample(request):
    alg = alg2.AlgII(alg2.Clayton(5))
    return render_xls((alg.sample() for i in range(500)))


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
    alg = alg2.AlgII(alg2.Clayton(5))
    return render_csv((alg.sample() for i in range(500)))


def render_csv(samples):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=simulation.csv'

    writer = csv.writer(response)
    for sample in samples:
        writer.writerow(sample)

    return response
