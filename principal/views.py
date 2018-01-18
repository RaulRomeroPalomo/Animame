#encoding:utf-8
import operator
import shelve

from django.db.models import Max, Count
from django.shortcuts import render_to_response
from django.template import RequestContext

from principal.models import *
from principal.forms import *
from index import *

import webscrape

   # matriz de artistas y numero de repeticiones de tags 
ItemPrefs={}   # matriz de items y puntuaciones de cada usuario. Inversa de Prefs`

def loadDict(usuario):
#     Caract={}
    Prefs={}
#     shelf = shelve.open("dataRS.dat")
    animes = Anime.objects.all()
    for row in animes:
        for tag in row.generos.all():
            if tag in usuario.topgeneros.all():
                if row not in Prefs:
                    Prefs[row]=1
                else:
                    Prefs[row]+=1
        for studio in row.estudios.all():
            if studio in usuario.topestudios.all():
                if row not in Prefs:
                    Prefs[row]=2
                else:
                    Prefs[row]+=2
    
#     print Prefs  
    animes = []
    for row in Prefs:
        if Prefs[row]>=3:
            animes.append(row)
    return animes
            

def inicio(request):
    return render_to_response('inicio.html')


def populate(request):
    webscrape.principal()
    return render_to_response('inicio.html',{'mensaje':'Ya tiene disponibles los próximos lanzamientos en Anime'})


def buscar_usuario(request):
    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            usuario = formulario.cleaned_data['usuario']
            try:
                user = Usuario.objects.get(usuario=usuario)
                estado = 0
            except:
                user, estado = webscrape.getUsuario(usuario)
                
            print estado
            if estado == 0: #Todo bien
                animes = loadDict(user)
                return render_to_response('lista.html',{'animes':animes,'usuario':user,'rs':True,'titulo':"Recomendados para '"+usuario+"'"})
            if estado == 1: #No existe usuario
                return render_to_response('inicio.html',{'usuario':'No existe usuario'})
            if estado == 2: #No tiene favoritos
                return render_to_response('inicio.html',{'usuario':'Debes tener favoritos para usar el sistema de recomendación'})
    else:
        formulario = SearchForm()
    return render_to_response('search.html',{'formulario':formulario,'titulo':'Busca tu usuario'}, context_instance=RequestContext(request))


def buscar_palabra(request):
    if request.method == 'POST':
        formulario = WordForm(request.POST)
        if formulario.is_valid():
            word = formulario.cleaned_data['word']
            animes = buscar('titulo', word)
            
            return render_to_response('lista.html',{'animes':animes,'titulo':"Animes con '"+word+"' en el Titulo"})
    else:
        formulario = WordForm()
    return render_to_response('search.html',{'formulario':formulario,'titulo':'Busqueda por palabras en el titulo'}, context_instance=RequestContext(request))


def buscar_sinopsis(request):
    if request.method == 'POST':
        formulario = WordForm(request.POST)
        if formulario.is_valid():
            word = formulario.cleaned_data['word']
            animes = buscar('sinopsis', word)
            
            return render_to_response('lista.html',{'animes':animes,'titulo':"La sinospsis contiene '"+word+"'"})
    else:
        formulario = WordForm()
    return render_to_response('search.html',{'formulario':formulario,'titulo':'Busqueda por palabras en la sinopsis'}, context_instance=RequestContext(request))


def animes_populares(request):
    animes = Anime.objects.order_by('popularidad')
    return render_to_response('lista.html',{'animes':animes,'titulo':'Animes por popularidad'})


def generos(request):
    generos = Genero.objects.all().order_by('nombre')
    return render_to_response('generos.html',{'generos':generos,'titulo':'Generos'})


def animes_genero(request, genero):
    animes = Anime.objects.all()
    rg = Genero.objects.get(nombre=genero)
    res = []
    for a in animes:
        if rg in a.generos.all():
            res.append(a)
    return render_to_response('lista.html',{'animes':res,'titulo':'Animes del genero '+genero})


def estudios(request):
    estudios = Estudio.objects.all().order_by('nombre')
    return render_to_response('estudio.html',{'estudios':estudios,'titulo':'Estudio'})


def animes_estudio(request, estudio):
    animes = Anime.objects.all()
    re = Estudio.objects.get(nombre=estudio)
    res = []
    for a in animes:
        if re in a.estudios.all():
            res.append(a)
    return render_to_response('lista.html',{'animes':res,'titulo':'Animes del estudio '+estudio})


def tipos(request):
    tipos = Tipo.objects.all().order_by('nombre')
    return render_to_response('tipo.html',{'tipos':tipos,'titulo':'Tipo'})


def animes_tipo(request, tipo):
    animes = Anime.objects.all()
    re = Tipo.objects.get(nombre=tipo)
    res = []
    for a in animes:
        if re == a.tipo:
            res.append(a)
    return render_to_response('lista.html',{'animes':res,'titulo':'Animes '+tipo})