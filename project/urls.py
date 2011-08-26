from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'project.views.index', name='index'),
    url(r'^about$', 'project.views.about', name='about'),

    # band
    url(r'^band/new$', 'project.views.new_band', name='new-band'),
    url(r'^band/create$', 'project.views.create_band', name='create-band'),
    url(r'^band/(?P<shortcut_name>\d+)$', 'project.views.show_band', name='show-band'),
    url(r'^band/(?P<shortcut_name>\d+)/edit$', 'project.views.edit_band', name='edit-band'),
    url(r'^band/(?P<shortcut_name>\d+)/update$', 'project.views.update_band', name='update-band'),

    # accounts
    url(r'^user/login$', 'project.views.login', name='user-login'),
    url(r'^user/logout$', 'project.views.logout', name='user-logout'),
    url(r'^user/new$', 'project.views.new_user', name='new-user'),
    url(r'^user/create$', 'project.views.create_user', name='create-user'),
    url(r'^user/edit$', 'project.views.edit_user', name='edit-user'),
    url(r'^user/update$', 'project.views.update_user', name='update-user'),
    url(r'^user/dashboard$', 'project.views.dashboard', name='user-dashboard'),
    url(r'^user/profile/(?P<username>\d+)$', 'project.views.show_user', name='show-user'),

    # Examples:
    # url(r'^bandontherun/', include('bandontherun.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
