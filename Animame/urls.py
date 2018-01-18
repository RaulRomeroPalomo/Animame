from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'principal.views.inicio'),
    # url(r'^$', 'Animame.views.home', name='home'),
    # url(r'^Animame/', include('Animame.foo.urls')),
    
    url(r'^populate/', 'principal.views.populate'),
    url(r'^searchusuario/', 'principal.views.buscar_usuario'),
    url(r'^searchword/', 'principal.views.buscar_palabra'),
    url(r'^searchsynopsis/', 'principal.views.buscar_sinopsis'),
    url(r'^genres/', 'principal.views.generos'),
    url(r'^listagenres/(?P<genero>([0-9a-zA-Z]{1,}[- ]{0,})*)/','principal.views.animes_genero'),
    url(r'^studio/', 'principal.views.estudios'),
    url(r'^listastudios/(?P<estudio>([0-9a-zA-Z]{1,}[.]{0,}[- ]{0,}[.]{0,})*)/','principal.views.animes_estudio'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
