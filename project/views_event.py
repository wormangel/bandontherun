from django.http import  HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.shortcuts import render_to_response, redirect
from django.core import serializers
from forms import UnavailabilityEntryForm

import  bands_manager

json_serializer = serializers.get_serializer("json")()

@login_required
@require_GET
def show_events(request, band_id):
    context = {}
    try:
        band = bands_manager.get_band(band_id)
        if not band.is_member(request.user):
            # 403
            raise Exception("You have no permission to view this band cause you are not a member of it.")
        context['band'] = band
    except Exception as exc:
        # 500
        context['error_msg'] = "Error ocurred: %s" % exc.message
    return render_to_response('band/events.html', context, context_instance=RequestContext(request))

@login_required
@require_GET
def get_calendar_entries(request, band_id):
    context = {}
    try:
        band = bands_manager.get_band(band_id)
        if not band.is_member(request.user):
            # 403
            raise Exception("You have no permission to view this band cause you are not a member of it.")
    except Exception as exc:
        # 500
        context['error_msg'] = "Error ocurred: %s" % exc.message
    response = HttpResponse(mimetype='application/json')
    json_serializer.serialize(band.calendar_entries, ensure_ascii=False, stream=response)
    return response

@login_required
@require_http_methods(["GET", "POST"])
def add_unavailability(request, band_id):
    context = {}
    band = bands_manager.get_band(band_id)
    context['band'] = band

    if request.method == 'POST':
        form = UnavailabilityEntryForm(request.POST)
        context['form'] = form

        if form.is_valid():
            date_start = form.cleaned_data['date_start']
            date_end = form.cleaned_data['date_end']
            time_start = form.cleaned_data['time_start']
            time_end = form.cleaned_data['time_end']
            all_day = form.cleaned_data['all_day']
            try:
                if not band.is_member(request.user):
                    raise Exception("You have no permission to add songs to this band's setlist cause you are not a member of it.")

                bands_manager.add_unavailability_entry(band_id, date_start, date_end, time_start, time_end, all_day, request.user)

                request.flash['success'] = "Unavailability added successfully!"
                return redirect('/band/%d/events' % band.id)
            except Exception as exc:
                context['error_msg'] = "Error ocurred: %s" % exc.message
                # 500
    else:
        context['form'] = UnavailabilityEntryForm()
    return render_to_response('band/events/unavailability/create.html', context, context_instance=RequestContext(request))

@login_required
@require_POST
def remove_unavailability(request, band_id, entry_id):
    context = {}
    band = bands_manager.get_band(band_id)
    try:
        if not band.is_member(request.user):
            raise Exception("You have no permission to remove this band's event cause you are not a member of it.")
        bands_manager.remove_unavailability(band_id, entry_id, request.user)
        return HttpResponse()
    except Exception as exc:
        print exc
        # 500