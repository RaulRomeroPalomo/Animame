from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'principal.views.inicio'),
    # url(r'^$', 'Animame.views.home', name='home'),
    # url(r'^Animame/', include('Animame.foo.urls')),
    
    url(r'^searchusuario/', 'principal.views.buscar_usuario'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
