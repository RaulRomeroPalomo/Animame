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
    url(r'^popularity/', 'principal.views.animes_populares'),
    url(r'^genres/', 'principal.views.generos'),
    url(r'^lista/(?P<genero>([0-9a-zA-Z]{1,}[- ]?)*)/','principal.views.animes_genero'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
