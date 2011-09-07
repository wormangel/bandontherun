from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'project.views.index', name='index'),
    url(r'^about$', 'project.views.about', name='about'),

    # bands url
    url(r'^band/create$', 'project.views_band.create_band', name='create-band'),
    url(r'^band/(?P<band_id>\d+)$', 'project.views_band.show_band', name='show-band'),
    url(r'^band/(?P<band_id>\d+)/upload$', 'project.views_band.upload_file', name='upload-band-file'),
    url(r'^band/(?P<band_id>\d+)/(?P<username>\w+)/(?P<bandfile_id>\d+)/deletefile$', 'project.views_band.delete_file', name='delete-band-file'),
    url(r'^band/(?P<band_id>\d+)/edit$', 'project.views_band.edit_band', name='edit-band'),
    url(r'^band/(?P<band_id>\d+)/member/add$', 'project.views_band.add_band_member', name='add-band-member'),
    url(r'^band/(?P<band_id>\d+)/member/(?P<username>\w+)/remove$', 'project.views_band.remove_band_member', name='remove-band-member'),

    # users url
    url(r'^user/login$', 'project.views_user.login', name='user-login'),
    url(r'^user/create$', 'project.views_user.create_user', name='create-user'),
    url(r'^user/logout$', 'project.views_user.logout', name='user-logout'),
    url(r'^user/edit$', 'project.views_user.edit_user', name='edit-user'),
    url(r'^user/dashboard$', 'project.views_user.dashboard', name='user-dashboard'),
    url(r'^user/invite$', 'project.views_user.invite_user', name='invite-user'),
    url(r'^user/profile/(?P<username>\w+)$', 'project.views_user.show_user', name='show-user'),
    url(r'^user/create/(?P<email>\w+)/(?P<key>\w+)$', 'project.views_user.create_invited_user', name='create-invited-user'),
    
    # Examples:
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

