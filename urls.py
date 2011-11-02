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
    url(r'^band/(?P<band_id>\d+)/files$', 'project.views_files.show_files', name='show-files'),
    url(r'^band/(?P<band_id>\d+)/upload$', 'project.views_files.upload_file', name='upload-band-file'),
    url(r'^band/(?P<band_id>\d+)/download/(?P<bandfile_id>\d+)$', 'project.views_files.download_file', name='download-band-file'),
    url(r'^band/(?P<band_id>\d+)/(?P<username>\w+)/(?P<bandfile_id>\d+)/deletefile$', 'project.views_files.delete_file', name='delete-band-file'),

    # setlists url
    url(r'^band/(?P<band_id>\d+)/setlist$', 'project.views_setlist.show_setlist', name='show-setlist'),
    url(r'^band/(?P<band_id>\d+)/setlist/add$', 'project.views_setlist.add_setlist_song', name='add-setlist-song'),
    url(r'^band/(?P<band_id>\d+)/setlist/add_batch$', 'project.views_setlist.add_setlist_batch', name='add-setlist-batch'),
    url(r'^band/(?P<band_id>\d+)/setlist/(?P<song_id>\w+)/remove$', 'project.views_setlist.remove_setlist_song', name='remove-setlist-song'),
    url(r'^band/(?P<band_id>\d+)/setlist/voting$', 'project.views_setlist.voting_dashboard', name='voting-dashboard'),
    url(r'^band/(?P<band_id>\d+)/setlist/voting/(?P<voting_id>\d+)/show$', 'project.views_setlist.show_voting', name='show-voting'),
    url(r'^band/(?P<band_id>\d+)/setlist/voting/create$', 'project.views_setlist.create_voting', name='create-voting'),
    url(r'^band/(?P<band_id>\d+)/setlist/(?P<song_id>\w+)/song_details$', 'project.views_setlist.show_song_details', name='show-song-details'),
    url(r'^band/(?P<band_id>\d+)/setlist/(?P<song_id>\w+)/upload_file$', 'project.views_setlist.upload_song_file', name='upload-song-file'),

    # band contacts url
    url(r'^band/(?P<band_id>\d+)/contacts$', 'project.views_contact.show_contacts', name='show-contacts'),
    url(r'^band/(?P<band_id>\d+)/contacts/(?P<contact_id>\w+)/remove$', 'project.views_contact.remove_contact', name='remove-contact'),
    url(r'^band/(?P<band_id>\d+)/contacts/add$', 'project.views_contact.add_contact', name='add-contact'),

    # band events
    url(r'^band/(?P<band_id>\d+)/events$', 'project.views_event.show_events', name='show-events'),
    url(r'^band/(?P<band_id>\d+)/events/entries$', 'project.views_event.get_calendar_entries', name='get-calendar-entries'),

    url(r'^band/(?P<band_id>\d+)/events/unavailabilities/search$', 'project.views_event.search_unavailabilities', name='search-unavailabilities'),
    url(r'^band/(?P<band_id>\d+)/events/unavailability/add$', 'project.views_event.add_unavailability', name='add-unavailability'),
    url(r'^band/(?P<band_id>\d+)/events/unavailability/(?P<entry_id>\d+)/remove$', 'project.views_event.remove_unavailability', name='remove-unavailability'),

    url(r'^band/(?P<band_id>\d+)/events/gig/add$', 'project.views_gig.add_gig', name='add-gig'),
    url(r'^band/(?P<band_id>\d+)/events/gig/(?P<entry_id>\d+)/edit$', 'project.views_gig.edit_gig', name='edit-gig'),
    url(r'^band/(?P<band_id>\d+)/events/gig/(?P<entry_id>\d+)/show$', 'project.views_gig.show_gig', name='show-gig'),
    url(r'^band/(?P<band_id>\d+)/events/gig/(?P<entry_id>\d+)/upload_contract$', 'project.views_gig.upload_contract', name='upload-contract'),
    url(r'^band/(?P<band_id>\d+)/events/gig/(?P<entry_id>\d+)/remove$', 'project.views_gig.remove_gig', name='remove-gig'),
    url(r'^band/(?P<band_id>\d+)/events/gig/(?P<entry_id>\d+)/setlist$', 'project.views_gig.gig_setlist', name='gig-setlist'),
    url(r'^band/(?P<band_id>\d+)/events/gig/(?P<entry_id>\d+)/setlist/add/(?P<song_id>\d+)$', 'project.views_gig.add_gig_song', name='add-gig-song'),
    url(r'^band/(?P<band_id>\d+)/events/gig/(?P<entry_id>\d+)/setlist/remove/(?P<song_id>\d+)$', 'project.views_gig.remove_gig_song', name='remove-gig-song'),
    url(r'^band/(?P<band_id>\d+)/events/gig/(?P<entry_id>\d+)/setlist/sort/(?P<song_id>\d+)$', 'project.views_gig.sort_gig_setlist', name='sort-gig-setlist'),

    url(r'^band/(?P<band_id>\d+)/events/rehearsal/add$', 'project.views_rehearsal.add_rehearsal', name='add-rehearsal'),
    url(r'^band/(?P<band_id>\d+)/events/rehearsal/(?P<entry_id>\d+)/edit$', 'project.views_rehearsal.edit_rehearsal', name='edit-rehearsal'),
    url(r'^band/(?P<band_id>\d+)/events/rehearsal/(?P<entry_id>\d+)/show', 'project.views_rehearsal.show_rehearsal', name='show-rehearsal'),
    url(r'^band/(?P<band_id>\d+)/events/rehearsal/(?P<entry_id>\d+)/remove$', 'project.views_rehearsal.remove_rehearsal', name='remove-rehearsal'),
    url(r'^band/(?P<band_id>\d+)/events/rehearsal/(?P<entry_id>\d+)/setlist$', 'project.views_rehearsal.rehearsal_setlist', name='rehearsal-setlist'),
    url(r'^band/(?P<band_id>\d+)/events/rehearsal/(?P<entry_id>\d+)/setlist/add/(?P<song_id>\d+)$', 'project.views_rehearsal.add_rehearsal_song', name='remove-rehearsal-song'),
    url(r'^band/(?P<band_id>\d+)/events/rehearsal/(?P<entry_id>\d+)/setlist/remove/(?P<song_id>\d+)$', 'project.views_rehearsal.remove_rehearsal_song', name='remove-rehearsal-song'),
    url(r'^band/(?P<band_id>\d+)/events/rehearsal/(?P<entry_id>\d+)/setlist/sort/(?P<song_id>\d+)$', 'project.views_rehearsal.sort_rehearsal_setlist', name='sort-rehearsal-setlist'),

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

