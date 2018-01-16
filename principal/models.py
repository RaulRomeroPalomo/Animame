from django.db import models


class Tipo(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    def __unicode__(self):
        return self.nombre


class Genero(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    def __unicode__(self):
        return self.nombre
    
class Estudio(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    def __unicode__(self):
        return self.nombre    

class Anime(models.Model):
    titulo = models.CharField(max_length=100, null=False, blank=False)
    original = models.CharField(max_length=100, null=True, blank=True)
    sinopsis = models.CharField(max_length=500, null=False, blank=True)
    lanzamiento = models.CharField(max_length=500, null=False, blank=True)
    tipo = models.ForeignKey(Tipo)
    estudios = models.ManyToManyField(Estudio)
    generos = models.ManyToManyField(Genero)
    popularidad = models.IntegerField(null=False)
#     clasificacionedad = models.IntegerField()
    def __unicode__(self):
        return self.titulo
    
    
class Usuario(models.Model):
    usuario = models.CharField(max_length=100, null=False, blank=False, unique=True)
    topgeneros = models.ManyToManyField(Genero)
    topestudios = models.ManyToManyField(Estudio)
    image = models.URLField(blank=True)
    def __unicode__(self):
        return self.usuario