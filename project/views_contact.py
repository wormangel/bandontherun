from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import   require_POST, require_GET
from django.shortcuts import render_to_response, redirect

from datetime import datetime
from forms import    ContactBandForm

import  bands_manager

@login_required
@require_POST
def remove_contact(request, band_id, contact_id):
    context = {}
    try:
        band = bands_manager.get_band(band_id)
        if not band.is_member(request.user):
            raise Exception("You have no permission to remove songs from this band's setlist cause you are not a member of it.")
        bands_manager.remove_contact(band_id, contact_id)
        return redirect('/band/%s/contacts' % band_id)
    except Exception as exc:
        context['error_msg'] = "Error ocurred: %s" % exc.message
        context['contact_form'] = ContactBandForm()
        return render_to_response('band/contacts.html', context, context_instance=RequestContext(request))

@login_required
@require_POST
def add_contact(request, band_id):
    context = {}

    band = bands_manager.get_band(band_id)
    form = ContactBandForm(request.POST)

    context['band'] = band
    context['form'] = form

    if form.is_valid():
        name = form.cleaned_data['name']
        phone = form.cleaned_data['phone']
        service = form.cleaned_data['service']
        cost = form.cleaned_data['cost']
        added = datetime.now()
        try:
            if not band.is_member(request.user):
                raise Exception("You have no permission to add songs to this band's setlist cause you are not a member of it.")
            bands_manager.add_contact(band_id, name, phone, service, cost, added, added_by=request.user)
            return redirect('/band/%s/contacts' % band_id)
        except Exception as exc:
            context['error_msg'] = "Error ocurred: %s" % exc.message
    return render_to_response('band/contacts.html', context, context_instance=RequestContext(request))


@login_required
@require_GET
def show_contacts(request, band_id):
    context = {}
    context['form'] = ContactBandForm()
    try:
        band = bands_manager.get_band(band_id)
        if not band.is_member(request.user):
            # 403
            raise Exception("You have no permission to view this band cause you are not a member of it.")
        context['band'] = band
    except Exception as exc:
        # 500
        context['error_msg'] = "Error ocurred: %s" % exc.message
    return render_to_response('band/contacts.html', context, context_instance=RequestContext(request))