# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template.context import RequestContext


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