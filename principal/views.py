#encoding:utf-8

from django.db.models import Max, Count
from django.shortcuts import render_to_response
from django.template import RequestContext

from principal.models import *
from principal.forms import *

def inicio(request):
    return render_to_response('inicio.html')


def buscar_usuario(request):
    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            #metodo en cuestion para sacar la infor del usuario
            return render_to_response('inicio.html')
    else:
        formulario = SearchForm()
    return render_to_response('search.html',{'formulario':formulario}, context_instance=RequestContext(request))