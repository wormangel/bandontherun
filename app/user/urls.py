from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # accounts
    url(r'^login$', 'project.views.login', name='user-login'),
    url(r'^logout$', 'project.views.logout', name='user-logout'),
    url(r'^create$', 'project.views.create_user', name='create-user'),
    url(r'^user/edit$', 'project.views.edit_user', name='edit-user'),
    url(r'^dashboard$', 'project.views.dashboard', name='user-dashboard'),
    url(r'^invite$', 'project.views.invite_user', name='invite-user'),
    url(r'^profile/(?P<username>\w+)$', 'project.views.show_user', name='show-user'),

    # Examples:
    # url(r'^bandontherun/', include('bandontherun.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
