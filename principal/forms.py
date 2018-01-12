#encoding:utf-8
from django.forms import ModelForm
from django import forms
from principal.models import *

class SearchForm(forms.Form):
    usuarioId = forms.CharField(label='Nombre de usuario', widget=forms.TextInput, required=True)