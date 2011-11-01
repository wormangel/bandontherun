# TODO: change some posts request to put / delete (investigate how to do that with django)
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import  require_GET, require_POST
from django.shortcuts import render_to_response, redirect
from django.db.models import Q

from project.errors import SongAlreadyOnSetlistError, BatchParseError

import  bands_manager

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
@require_GET
def filter_setlist(request, band_id):
    context = {}
    try:
        band = bands_manager.get_band(band_id)
        if not band.is_member(request.user):
            # 403
            raise Exception("You have no permission to view this band cause you are not a member of it.")
        context['band'] = band
        query = request.GET["query"]
        song_list = band.setlist.song_list.filter(Q(artist__icontains=query) | Q(title__icontains=query))
        context['song_list'] = song_list
        context['song_list_size'] = len(song_list) 
        context['query_string'] = query
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

        context['active_voting'] = False
        context['older_votings'] = False

        if not band.is_member(request.user):
            raise Exception("You have no permission to view this band's votings cause you are not a member of it.")

        
    except Exception as exc:
        context['error_msg'] = "Error ocurred: %s" % exc.message


    return render_to_response('band/voting/dashboard.html', context, context_instance=RequestContext(request))

def create_voting(request, band_id):
    pass

def vote_setlist(request, band_id, song_id, voting_id):
    pass

def show_voting(request, band_id, voting_id):
    pass
