# TODO: change some posts request to put / delete (investigate how to do that with django)
from django.http import  HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.shortcuts import render_to_response, redirect

from forms import      RehearsalEntryForm
from django.utils import simplejson

import bands_manager

@login_required
@require_http_methods(["GET"])
def show_rehearsal(request, band_id, entry_id):
    context = {}
    try:
        band = bands_manager.get_band(band_id)
        if not band.is_member(request.user):
            raise Exception("You have no permission to view this band's events cause you are not a member of it.")

        rehearsal = bands_manager.get_rehearsal(entry_id)

        # calculates the band diff setlist (band setlist songs minus rehearsal setlist songs)
        diff_setlist = []
        for song in band.setlist.song_list:
            if not rehearsal.setlist.contains(song):
                diff_setlist.append(song)

        context['diff_setlist'] = diff_setlist
        context['band'] = band
        context['rehearsal'] = rehearsal
    except Exception as exc:
        # 500
        context['error_msg'] = "Error ocurred: %s" % exc.message
    return render_to_response('band/events/rehearsal/show.html', context, context_instance=RequestContext(request))

@login_required
@require_http_methods(["GET", "POST"])
def edit_rehearsal(request, band_id, entry_id):
    context = {}

    try:
        band = bands_manager.get_band(band_id)
        context['band'] = band
        rehearsal = bands_manager.get_rehearsal(entry_id)

        if not band.is_member(request.user):
            raise Exception("You have no permission to edit this band's events cause you are not a member of it.")

        if request.method == 'POST':
            form = RehearsalEntryForm(request.POST)
            context['form'] = form
            if form.is_valid():
                date_start = form.cleaned_data['date_start']
                time_start = form.cleaned_data['time_start']
                time_end = form.cleaned_data['time_end']
                place = form.cleaned_data['place']
                costs = form.cleaned_data['costs']

                rehearsal = bands_manager.update_rehearsal_entry(entry_id, date_start, time_start, time_end, place, costs)
                request.flash['success'] = "Rehearsal updated successfully!"
                return redirect('/band/%d/events' % band.id)
        else: # GET
            if rehearsal.band != band:
                raise Exception("There is no rehearsal for this band with the given Id.")

            data = {'date_start' : rehearsal.date_start,
                    'time_start' : rehearsal.time_start,
                    'time_end' : rehearsal.time_end,
                    'place' : rehearsal.place,
                    'costs' : rehearsal.costs,
                    }
            form = RehearsalEntryForm(data)

        context['rehearsal'] = rehearsal
        context['form'] = form
    except Exception as exc:
        # 404
        context['error_msg'] = "Error ocurred: %s" % exc.message

    return render_to_response('band/events/rehearsal/edit.html', context, context_instance=RequestContext(request))

@login_required
@require_http_methods(["GET", "POST"])
def rehearsal_setlist(request, band_id, entry_id):
    context = {}

    try:
        band = bands_manager.get_band(band_id)
        if not band.is_member(request.user):
            raise Exception("You have no permission to view this band's event cause you are not a member of it.")
        context['band'] = band
        rehearsal = bands_manager.get_rehearsal(entry_id)
        context['rehearsal'] = rehearsal

        # calculates the band diff setlist (band setlist songs minus rehearsal setlist songs)
        diff_setlist = []
        for song in band.setlist.song_list:
            if not rehearsal.setlist.contains(song):
                diff_setlist.append(song)

        context['diff_setlist'] = diff_setlist
    except Exception as exc:
        context['error_msg'] = "Error ocurred: %s" % exc.message
    return render_to_response('band/events/rehearsal/setlist.html', context, context_instance=RequestContext(request))

@login_required
@require_http_methods(["GET", "POST"])
def add_rehearsal(request, band_id):
    context = {}
    band = bands_manager.get_band(band_id)
    context['band'] = band

    if request.method == 'POST':
        form = RehearsalEntryForm(request.POST)
        context['form'] = form

        if form.is_valid():
            date_start = form.cleaned_data['date_start']
            time_start = form.cleaned_data['time_start']
            time_end = form.cleaned_data['time_end']
            place = form.cleaned_data['place']
            costs = form.cleaned_data['costs']
            try:
                if not band.is_member(request.user):
                    raise Exception("You have no permission to add songs to this band's setlist cause you are not a member of it.")
                bands_manager.add_rehearsal_entry(band_id, date_start, time_start, time_end, place, costs, request.user)
                request.flash['success'] = "Rehearsal added successfully!"
                return redirect('/band/%d/events' % band.id)
            except Exception as exc:
                context['error_msg'] = "Error ocurred: %s" % exc.message
                # 500
    else:
        context['form'] = RehearsalEntryForm()
    return render_to_response('band/events/rehearsal/create.html', context, context_instance=RequestContext(request))

@login_required
@require_POST
def add_rehearsal_song(request, band_id, entry_id, song_id):
    try:
        band = bands_manager.get_band(band_id)
        if not band.is_member(request.user):
            raise Exception("You have no permission to view this band cause you are not a member of it.")
        response_data = {}
        bands_manager.add_rehearsal_song(entry_id, song_id, request.POST['position'])
        response_data = { 'success' : "ok" }
    except Exception as exc:
        response_data= { 'success' : "fail: " + exc.message }

    return HttpResponse(simplejson.dumps(response_data), mimetype='application/json')

@login_required
@require_POST
def remove_rehearsal_song(request, band_id, entry_id, song_id):
    try:
        band = bands_manager.get_band(band_id)
        if not band.is_member(request.user):
            raise Exception("You have no permission to view this band cause you are not a member of it.")
        response_data = {}
        bands_manager.remove_rehearsal_song(entry_id, song_id)
        response_data = { 'success' : "ok" }
    except Exception as exc:
        response_data= { 'success' : "fail: " + exc.message }

    return HttpResponse(simplejson.dumps(response_data), mimetype='application/json')

@login_required
@require_POST
def remove_rehearsal(request, band_id, entry_id):
    context = {}
    band = bands_manager.get_band(band_id)
    try:
        if not band.is_member(request.user):
            raise Exception("You have no permission to remove this band's event cause you are not a member of it.")
        bands_manager.remove_rehearsal(band_id, entry_id, request.user)
        return HttpResponse()
    except Exception as exc:
        print exc
        # 500

@login_required
@require_POST
def sort_rehearsal_setlist(request, band_id, entry_id, song_id):
    try:
        band = bands_manager.get_band(band_id)
        if not band.is_member(request.user):
            raise Exception("You have no permission to view this band cause you are not a member of it.")
        response_data = {}
        bands_manager.sort_rehearsal_setlist(entry_id, song_id, request.POST['position'])
        response_data = { 'success' : "ok" }
    except Exception as exc:
        response_data= { 'success' : "fail: " + exc.message }

    return HttpResponse(simplejson.dumps(response_data), mimetype='application/json')
