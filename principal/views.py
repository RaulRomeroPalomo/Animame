#encoding:utf-8

from django.db.models import Max, Count
from django.shortcuts import render_to_response
from django.template import RequestContext

from principal.models import *

def inicio(request):
    return render_to_response('inicio.html')