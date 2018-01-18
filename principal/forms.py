#encoding:utf-8
from django.forms import ModelForm
from django import forms
from principal.models import *

class SearchForm(forms.Form):
    usuarioId = forms.CharField(label='Nombre de usuario', widget=forms.TextInput, required=True)
    
class WordForm(forms.Form):
    word = forms.CharField(label='Palabra de busqueda', widget=forms.TextInput, required=True)