# TODO: change some posts request to put / delete (investigate how to do that with django)
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import  require_GET, require_POST
from django.shortcuts import render_to_response, redirect
from django.db.models import Q
from django.core.urlresolvers import reverse
from filetransfers.api import prepare_upload, serve_file

from project.errors import SongAlreadyOnSetlistError, BatchParseError

from datetime import datetime
import  bands_manager
from forms import UploadBandFileForm
from models import User, Band, BandFile, Song
from project.forms import SetlistVotingForm

@login_required
@require_GET
def show_setlist(request, band_id):
    context = {}
    try:
        band = bands_manager.get_band(band_id)
        if not band.is_member(request.user):
            # 403
            raise Exception("You have no permission to view this band cause you are not a member of it.")
        context['band'] = band
        context['song_list'] = band.setlist.song_list
        context['song_list_size'] = len(band.setlist.song_list) 
        context['query_string'] = ''
    except Exception as exc:
        # 500
        context['error_msg'] = "Error ocurred: %s" % exc.message
    return render_to_response('band/setlist.html', context, context_instance=RequestContext(request))

@login_required
@require_POST
def remove_setlist_song(request, band_id, song_id):
    context = {}

    try:
        band = bands_manager.get_band(band_id)
        if not band.is_member(request.user):
            raise Exception("You have no permission to remove songs from this band's setlist cause you are not a member of it.")
        bands_manager.remove_setlist_song(band_id, song_id)
        return redirect('/band/%s/setlist' % band_id)
    except Exception as exc:
        context['error_msg'] = "Error ocurred: %s" % exc.message
        return render_to_response('band/setlist.html', context, context_instance=RequestContext(request))

@login_required
@require_POST
def add_setlist_song(request, band_id):
    context = {}
    artist = request.POST['artist']
    title = request.POST['title']

    try:
        band = bands_manager.get_band(band_id)
        if not band.is_member(request.user):
            raise Exception("You have no permission to add songs to this band's setlist cause you are not a member of it.")
        bands_manager.add_setlist_song(band_id, artist, title)
        return redirect('/band/%s/setlist' % band_id)
    except Exception as exc:
        context['error_msg'] = "Error ocurred: %s" % exc.message
        return render_to_response('band/setlist.html', context, context_instance=RequestContext(request))

@login_required
@require_POST
def add_setlist_batch(request, band_id):
    context = {}
    batch = request.POST['batch']

    try:
        band = bands_manager.get_band(band_id)
        context['band'] = band

        if not band.is_member(request.user):
            raise Exception("You have no permission to add songs to this band's setlist cause you are not a member of it.")

        for line in batch.splitlines():
            try:
                artist, title = line.split(' - ')
            except:
                raise BatchParseError(line)

            if artist is None or title is None:
                raise BatchParseError(line)
            try:
                bands_manager.add_setlist_song(band_id, artist, title)
            except SongAlreadyOnSetlistError:
                continue

        return redirect('/band/%s/setlist' % band_id)

    except BatchParseError as exc:
        context['error_msg'] = "Parsing error. The following line is in a unknow format: %s" % exc.line
    except Exception as exc:
        context['error_msg'] = "Error ocurred: %s" % exc.message
    return render_to_response('band/setlist.html', context, context_instance=RequestContext(request))

@login_required
def voting_dashboard(request, band_id):
    context = {}
    try:
        band = bands_manager.get_band(band_id)
        context['band'] = band

        context['active_voting'] = band.has_active_voting
        context['older_votings'] = False

        if not band.is_member(request.user):
            raise Exception("You have no permission to view this band's votings cause you are not a member of it.")

        
    except Exception as exc:
        context['error_msg'] = "Error ocurred: %s" % exc.message


    return render_to_response('band/voting/dashboard.html', context, context_instance=RequestContext(request))

def create_voting(request, band_id):
    context = {}

    band = bands_manager.get_band(band_id)
    context['band'] = band
    form = SetlistVotingForm(request.POST or None)
    context['form'] = form

    if request.method == 'POST' and form.is_valid():
        n_suggestions = form.cleaned_data['n_suggestions']
        n_votes_per_user = form.cleaned_data['n_votes_per_user']
        n_winning_songs = form.cleaned_data['n_winning_songs']

        date_suggestion_start = form.cleaned_data['date_suggestion_start']
        time_suggestion_start = form.cleaned_data['time_suggestion_start']
        date_suggestion_end = form.cleaned_data['date_suggestion_end']
        time_suggestion_end = form.cleaned_data['time_suggestion_end']

        date_voting_start = form.cleaned_data['date_voting_start']
        time_voting_start = form.cleaned_data['time_voting_start']
        date_voting_end = form.cleaned_data['date_voting_end']
        time_voting_end = form.cleaned_data['time_voting_end']
        try:
            if not band.is_member(request.user):
                raise Exception("You have no permission to start a voting cause you are not a member of this band.")
            voting = bands_manager.add_voting(band_id, n_suggestions, n_votes_per_user, n_winning_songs, date_suggestion_start,
                                     time_suggestion_start, date_suggestion_end, time_suggestion_end, date_voting_start,
                                     time_voting_start, date_voting_end, time_voting_end)
            request.flash['success'] = "Voting added successfully!"
            return redirect('/band/%d/setlist/voting/%d/show' % (band.id, voting.id))
        except Exception as exc:
            # 500
            print exc.message
            context['error_msg'] = "Error ocurred: %s" % exc.message
    return render_to_response('band/voting/create.html', context, context_instance=RequestContext(request))

def vote_setlist(request, band_id, song_id, voting_id):
    pass

def show_voting(request, band_id, voting_id):
    pass
    
@login_required
@require_GET
def show_song_details(request, band_id, song_id):
    context = {}
    try:
        band = bands_manager.get_band(band_id)
        if not band.is_member(request.user):
            raise Exception("You have no permission to view this band's events cause you are not a member of it.")

        song = bands_manager.get_song(song_id)
        context = __prepare_context(request, band, song)
    except Exception as exc:
        # 500
        print exc.message
        context['error_msg'] = "Error ocurred: %s" % exc.message
    return render_to_response('band/song.html', context, context_instance=RequestContext(request))

@login_required
@require_POST
def upload_song_file(request, band_id, song_id):
    try:
        user = User.objects.get(username=request.user.username)
        band = Band.objects.get(id=band_id)
        song = Song.objects.get(id=song_id)

        if not band.is_member(user):
            raise Exception("You have no permission to upload files to this band cause you are not a member of it.")

        context = __prepare_context(request, band, song)
        form = UploadBandFileForm(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES['file']
            band_file = form.save(commit=False)
            band_file.filename= file.name
            band_file.size = file.size
            band_file.uploader = user.username
            band_file.band = band
            band_file.created = datetime.now()
            band_file.save()
            song.attachments.add(band_file)
            song.save()
            return render_to_response('band/song.html', context, context_instance=RequestContext(request))
        context['song_form'] = form
    except Exception as exc:
        print exc.message
        context['error_msg'] = "Error: %s" % exc.message
    return render_to_response('band/song.html', context, context_instance=RequestContext(request))
    
def __prepare_context(request, band, song):
    context = {}
    context['band'] = band
    context['song'] = song
    view_url = reverse('upload-song-file', args=[band.id, song.id])
    upload_url, upload_data = prepare_upload(request, view_url)
    context['song_form'] = UploadBandFileForm()
    context['song_url'] = upload_url
    context['song_data'] = upload_data
    return context
