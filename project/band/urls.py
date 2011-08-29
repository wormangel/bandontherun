from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # band
    url(r'^create$', 'band.views.create_band', name='create-band'),
    url(r'^(?P<band_id>\d+)$', 'band.views.show_band', name='show-band'),
    url(r'^(?P<band_id>\d+)/edit$', 'band.views.edit_band', name='edit-band'),
    url(r'^(?P<band_id>\d+)/member/add$', 'band.views.add_band_member', name='add-band-member'),
    url(r'^(?P<band_id>\d+)/member/(?P<username>\d+)/remove$', 'band.views.remove_band_member', name='remove-band-member'),

    # Examples:
    # url(r'^bandontherun/', include('bandontherun.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
