# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template.context import RequestContext


def home(request):
    template = 'base.xhtml'
    data = dict()
    return render_to_response(template,
                              data,
                              context_instance=RequestContext(request))