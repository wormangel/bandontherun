from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'project.views.home', name='home'),
    url(r'^$', 'project.views.index', name='index'),
    url(r'^band/(?P<band_name>\d+)/$', 'project.views.show_band', name='show-band'),
    url(r'^accounts/(?P<user_login>\d+)/$', 'project.views.show_user', name='show-user'),

    # Examples:
    # url(r'^bandontherun/', include('bandontherun.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
