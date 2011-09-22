from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_complete, password_reset_confirm

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'project.views.index', name='index'),
    url(r'^about$', 'project.views.about', name='about'),

    # bands url
    url(r'^band/create$', 'project.views_band.create_band', name='create-band'),
    url(r'^band/(?P<band_id>\d+)$', 'project.views_band.show_band', name='show-band'),
    url(r'^band/(?P<band_id>\d+)/edit$', 'project.views_band.edit_band', name='edit-band'),
    url(r'^band/(?P<band_id>\d+)/member/add$', 'project.views_band.add_band_member', name='add-band-member'),
    url(r'^band/(?P<band_id>\d+)/member/(?P<username>\w+)/remove$', 'project.views_band.remove_band_member', name='remove-band-member'),

    # files url
    url(r'^band/(?P<band_id>\d+)/files$', 'project.views_band.show_files', name='show-files'),
    url(r'^band/(?P<band_id>\d+)/upload$', 'project.views_band.upload_file', name='upload-band-file'),
    url(r'^band/(?P<band_id>\d+)/download/(?P<bandfile_id>\d+)$', 'project.views_band.download_file', name='download-band-file'),
    url(r'^band/(?P<band_id>\d+)/(?P<username>\w+)/(?P<bandfile_id>\d+)/deletefile$', 'project.views_band.delete_file', name='delete-band-file'),

    # setlists url
    url(r'^band/(?P<band_id>\d+)/setlist$', 'project.views_band.show_setlist', name='show-setlist'),
    url(r'^band/(?P<band_id>\d+)/setlist/add$', 'project.views_band.add_setlist_song', name='add-setlist-song'),
    url(r'^band/(?P<band_id>\d+)/setlist/(?P<song_id>\w+)/remove$', 'project.views_band.remove_setlist_song', name='remove-setlist-song'),

    # band contacts url
    url(r'^band/(?P<band_id>\d+)/contacts$', 'project.views_band.show_contacts', name='show-contacts'),
    url(r'^band/(?P<band_id>\d+)/contact/(?P<contact_id>\w+)/remove$', 'project.views_band.remove_contact', name='remove-contact'),
    url(r'^band/(?P<band_id>\d+)/contact/add$', 'project.views_band.add_contact', name='add-contact'),

    # band calendar
    url(r'^band/(?P<band_id>\d+)/calendar$', 'project.views_band.show_calendar', name='show-calendar'),
    url(r'^band/(?P<band_id>\d+)/calendar/entries$', 'project.views_band.get_calendar_entries', name='get-calendar-entries'),
    url(r'^band/(?P<band_id>\d+)/calendar/entry/add$', 'project.views_band.add_calendar_entry', name='add-calendar-entry'),

    # users url
    url(r'^user/login$', 'project.views_user.login', name='user-login'),
    url(r'^user/create$', 'project.views_user.create_user', name='create-user'),
    url(r'^user/logout$', 'project.views_user.logout', name='user-logout'),
    url(r'^user/password-reset-done$', password_reset_done, {'template_name': 'user/password-reset-done.html'}, name='password-reset-done'),
    url(r'^user/password-reset-confirm/(?P<uidb36>\w+)/(?P<token>[-\w]+)$', password_reset_confirm, {'template_name': 'user/password-reset-confirm.html'}, name='password-reset-confirm'),
    url(r'^user/password-reset-complete$', password_reset_complete, {'template_name': 'user/password-reset-complete.html'}, name='password-reset-complete.html'),
    url(r'^user/password-reset$', password_reset, {'template_name': 'user/password-reset.html', 'email_template_name': 'user/password-reset-email.html'}, name='password-reset'),
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

