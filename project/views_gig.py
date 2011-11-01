# TODO: change some posts request to put / delete (investigate how to do that with django)
from django.http import  HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse

from datetime import datetime
from filetransfers.api import prepare_upload
from models import Band, User
from forms import   UploadBandFileForm, GigEntryForm
from project.models import Gig
from django.utils import simplejson

import  bands_manager

@login_required
@require_http_methods(["GET", "POST"])
def add_gig(request, band_id):
    context = {}
    band = bands_manager.get_band(band_id)
    context['band'] = band

    if request.method == 'POST':
        form = GigEntryForm(request.POST)
        context['form'] = form
        if form.is_valid():
            date_start = form.cleaned_data['date_start']
            date_end = form.cleaned_data['date_end']
            time_start = form.cleaned_data['time_start']
            time_end = form.cleaned_data['time_end']
            place = form.cleaned_data['place']
            costs = form.cleaned_data['costs']
            ticket = form.cleaned_data['ticket']
            try:
                if not band.is_member(request.user):
                    raise Exception("You have no permission to add songs to this band's setlist cause you are not a member of it.")
                bands_manager.add_gig_entry(band_id, date_start, date_end, time_start, time_end, place, costs, ticket, request.user)
                if (bands_manager.has_unavailabilities(band_id, date_start, date_end)):
                    request.flash['warning'] = "There is at least one unavailability of a member on this period."
                request.flash['success'] = "Gig added successfully!"
                return redirect('/band/%d/events' % band.id)
            except Exception as exc:
                context['error_msg'] = "Error ocurred: %s" % exc.message
                # 500
    else:
        context['form'] = GigEntryForm()
    return render_to_response('band/events/gig/create.html', context, context_instance=RequestContext(request))

@login_required
@require_http_methods(["GET", "POST"])
def edit_gig(request, band_id, entry_id):
    context = {}

    try:
        band = bands_manager.get_band(band_id)
        context['band'] = band

        gig = bands_manager.get_gig(entry_id)

        if not band.is_member(request.user):
            raise Exception("You have no permission to edit this band's events cause you are not a member of it.")

        if request.method == 'POST':
            form = GigEntryForm(request.POST)
            context['form'] = form
            if form.is_valid():
                date_start = form.cleaned_data['date_start']
                time_start = form.cleaned_data['time_start']
                time_end = form.cleaned_data['time_end']
                place = form.cleaned_data['place']
                costs = form.cleaned_data['costs']
                ticket = form.cleaned_data['ticket']

                gig = bands_manager.update_gig_entry(entry_id, date_start, time_start, time_end, place, costs, ticket)
                request.flash['success'] = "Gig updated successfully!"
                return redirect('/band/%d/events' % band.id)
        else: # GET
            if gig.band != band:
                raise Exception("There is no gig for this band with the given Id.")

            data = {'date_start' : gig.date_start,
                    'time_start' : gig.time_start,
                    'time_end' : gig.time_end,
                    'place' : gig.place,
                    'costs' : gig.costs,
                    'ticket' : gig.ticket
                    }
            form = GigEntryForm(data)

        context['gig'] = gig
        context['form'] = form
    except Exception as exc:
        # 404
        context['error_msg'] = "Error ocurred: %s" % exc.message

    return render_to_response('band/events/gig/edit.html', context, context_instance=RequestContext(request))

@login_required
@require_http_methods(["GET"])
def show_gig(request, band_id, entry_id):
    context = {}
    try:
        band = bands_manager.get_band(band_id)
        if not band.is_member(request.user):
            raise Exception("You have no permission to view this band's events cause you are not a member of it.")

        gig = bands_manager.get_gig(entry_id)

        # calculates the band diff setlist (band setlist songs minus gig setlist songs)
        diff_setlist = []

        for song in band.setlist.song_list:
            if not gig.setlist.contains(song):
                diff_setlist.append(song)

        context['diff_setlist'] = diff_setlist

        context['band'] = band
        context['gig'] = gig

        if gig.contract is None:
            view_url = reverse('project.views_gig.upload_contract', args=[band.id, gig.id])
            upload_url, upload_data = prepare_upload(request, view_url)
            context["contract_form"] = UploadBandFileForm(request.POST, request.FILES)
            context['contract_url'] = upload_url
            context['contract_data'] = upload_data
            context['form'] = True
        else:
            context["contract"] = gig.contract
            context['form'] = False
    except Exception as exc:
        # 500
        context['error_msg'] = "Error ocurred: %s" % exc.message
    return render_to_response('band/events/gig/show.html', context, context_instance=RequestContext(request))

@login_required
@require_http_methods(["POST"])
def upload_contract(request, band_id, entry_id):
    try:
        user = User.objects.get(username=request.user.username)
        band = Band.objects.get(id=band_id)
        gig = Gig.objects.get(id=entry_id)

        if not band.is_member(user):
            raise Exception("You have no permission to upload files to this band cause you are not a member of it.")

        context = __prepare_context(request, band)
        context['band'] = band
        context['gig'] = gig
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
            gig.contract = band_file
            gig.save()
            context["contract"] = band_file
            return render_to_response('band/events/gig/show.html', context, context_instance=RequestContext(request))
        context['contract_form'] = form
    except Exception as exc:
        context['error_msg'] = "Error: %s" % exc.message
    return render_to_response('band/events/gig/show.html', context, context_instance=RequestContext(request))

@login_required
@require_POST
def remove_gig(request, band_id, entry_id):
    context = {}
    band = bands_manager.get_band(band_id)
    try:
        if not band.is_member(request.user):
            raise Exception("You have no permission to remove this band's event cause you are not a member of it.")
        bands_manager.remove_gig(band_id, entry_id, request.user)
        return HttpResponse()
    except Exception as exc:
        print exc
        # 500

@login_required
@require_http_methods(["GET", "POST"])
def gig_setlist(request, band_id, entry_id):
    context = {}

    try:
        band = bands_manager.get_band(band_id)

        if not band.is_member(request.user):
            raise Exception("You have no permission to view this band's event cause you are not a member of it.")

        context['band'] = band

        gig = bands_manager.get_gig(entry_id)
        context['gig'] = gig

        # calculates the band diff setlist (band setlist songs minus gig setlist songs)
        diff_setlist = []

        for song in band.setlist.song_list:
            if not gig.setlist.contains(song):
                diff_setlist.append(song)

        context['diff_setlist'] = diff_setlist

    except Exception as exc:
        context['error_msg'] = "Error ocurred: %s" % exc.message
    return render_to_response('band/events/gig/setlist.html', context, context_instance=RequestContext(request))

@login_required
@require_POST
def add_gig_song(request, band_id, entry_id, song_id):
    try:
        band = bands_manager.get_band(band_id)
        if not band.is_member(request.user):
            raise Exception("You have no permission to view this band cause you are not a member of it.")

        response_data = {}

        bands_manager.add_gig_song(entry_id, song_id, request.POST['position'])

        response_data = { 'success' : "ok" }
    except Exception as exc:
        response_data= { 'success' : "fail: " + exc.message }

    return HttpResponse(simplejson.dumps(response_data), mimetype='application/json')

@login_required
@require_POST
def remove_gig_song(request, band_id, entry_id, song_id):
    try:
        band = bands_manager.get_band(band_id)
        if not band.is_member(request.user):
            raise Exception("You have no permission to view this band cause you are not a member of it.")
        response_data = {}
        bands_manager.remove_gig_song(entry_id, song_id)
        response_data = { 'success' : "ok" }
    except Exception as exc:
        response_data= { 'success' : "fail: " + exc.message }

    return HttpResponse(simplejson.dumps(response_data), mimetype='application/json')

@login_required
@require_POST
def sort_gig_setlist(request, band_id, entry_id, song_id):
    try:
        band = bands_manager.get_band(band_id)
        if not band.is_member(request.user):
            raise Exception("You have no permission to view this band cause you are not a member of it.")
        response_data = {}
        bands_manager.sort_gig_setlist(entry_id, song_id, request.POST['position'])
        response_data = { 'success' : "ok" }
    except Exception as exc:
        response_data= { 'success' : "fail: " + exc.message }

    return HttpResponse(simplejson.dumps(response_data), mimetype='application/json')

def __prepare_context(request, band):
    context = {}
    context['band'] = band
    view_url = reverse('upload-band-file', args=[band.id])
    upload_url, upload_data = prepare_upload(request, view_url)
    context['upload_form'] = UploadBandFileForm()
    context['upload_url'] = upload_url
    context['upload_data'] = upload_data
    return context
