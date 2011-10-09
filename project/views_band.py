# TODO: change some posts request to put / delete (investigate how to do that with django)
from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core import serializers
from django.core.urlresolvers import reverse

from datetime import datetime
from filetransfers.api import prepare_upload, serve_file
from models import Band, User, BandFile
from forms import BandCreateForm, BandEditForm, UploadBandFileForm, ContactBandForm, UnavailabilityEntryForm

import users_manager, bands_manager

json_serializer = serializers.get_serializer("json")()

@login_required
@require_GET
def show_band(request, band_id):
    context = {}
    try:
        band = bands_manager.get_band(band_id)
        context = __prepare_context(request, band)
        if not band.is_member(request.user):
            # 403
            raise Exception("You have no permission to view this band cause you are not a member of it.")
    except Exception as exc:
        # 500
        context['error_msg'] = "Error ocurred: %s" % exc.message
    return render_to_response('band/show.html', context, context_instance=RequestContext(request))

@login_required
@require_http_methods(["GET", "POST"])
def create_band(request):
    context = {}

    if request.method == 'POST':
        form = BandCreateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            bio = form.cleaned_data['bio']
            url = form.cleaned_data['url']
            try:
                band = bands_manager.create_band(name, bio, url, request.user)
                return redirect('/band/%d' % band.id)
            except Exception as exc:
                #400
                form.errors['__all__'] = form.error_class(["Error: %s" % exc.message])
    else: # request.method == GET
        form = BandCreateForm()

    # GET / POST with invalid input
    context['form'] = form
    return render_to_response('band/create.html', context, context_instance=RequestContext(request))

@login_required
@require_http_methods(["GET", "POST"])
def edit_band(request, band_id):
    context = {}

    try:
        band = bands_manager.get_band(band_id)

        if not band.is_member(request.user):
            raise Exception("You have no permission edit this band cause you are not a member of it.")

        if request.method == 'POST':
            form = BandEditForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                bio = form.cleaned_data['bio']
                url = form.cleaned_data['url']
                band = bands_manager.update_band(band_id, name, bio, url) #get the updated band
                context['success'] = True
        else:
            # request.method == 'GET'
            data = {'name': band.name,
                    'bio': band.bio,
                    'url': band.url,}
            form = BandEditForm(data)
            
        context['form'] = form
        context['band'] = band
    except Exception as exc:
        # 404
        context['error_msg'] = "Error ocurred: %s" % exc.message
        
    return render_to_response('band/edit.html', context, context_instance=RequestContext(request))

@login_required
@require_POST
def add_band_member(request, band_id):
    context = {}
    username = request.POST['username']

    try:
        band = bands_manager.get_band(band_id)
        if not band.is_member(request.user):
            raise Exception("You have no permission to add members to this band cause you are not a member of it.")

        bands_manager.add_band_member(band_id, username)
        return redirect('/band/%s' % band_id)
    except Exception as exc:
        context['error_msg'] = "Error ocurred: %s" % exc.message
        return render_to_response('band/show.html', context, context_instance=RequestContext(request))

@login_required
@require_POST
def remove_band_member(request, band_id, username):
    context = {}

    try:
        band = bands_manager.get_band(band_id)
        if not band.is_member(request.user):
            raise Exception("You have no permission to remove members from this band cause you are not a member of it.")

        bands_manager.remove_band_member(band_id, users_manager.get_user(username))
        return redirect('/band/%s' % band_id)
    except Exception as exc:
        context['error_msg'] = "Error ocurred: %s" % exc.message
        return render_to_response('band/show.html', context, context_instance=RequestContext(request))
        
@login_required
@require_POST
def upload_file(request, band_id):
    view_url = reverse('project.views_band.upload_file', args=[band_id])

    try:
        user = User.objects.get(username=request.user.username)
        band = Band.objects.get(id=band_id)

        if not band.is_member(user):
            raise Exception("You have no permission to upload files to this band cause you are not a member of it.")

        context = __prepare_context(request, band)
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
            return render_to_response('band/files.html', context, context_instance=RequestContext(request))

        context['upload_form'] = form
    except Exception as exc:
        context['error_msg'] = "Error: %s" % exc.message
        
    return render_to_response('band/files.html', context, context_instance=RequestContext(request))

@login_required
@require_POST
def delete_file(request, band_id, username, bandfile_id):
    context = __prepare_context(request, Band.objects.get(id=band_id))
    
    band_file = BandFile.objects.get(id=bandfile_id)
    if band_file:
        if Band.objects.get(id=band_id).is_member(User.objects.get(username=username)):
            band_file.file.delete()
            band_file.delete()
        else:
            context['error_msg'] = "You have no permission to delete a file from this band cause you are not a member of it."
            return render_to_response('band/files.html', context, context_instance=RequestContext(request))
    else:
        context['error_msg'] = "Invalid file."
        return render_to_response('band/files.html', context, context_instance=RequestContext(request))
    return render_to_response('band/files.html', context, context_instance=RequestContext(request))

@login_required
@require_GET
def download_file(request, band_id, bandfile_id):
    try:
        band = bands_manager.get_band(band_id)
        if not band.is_member(request.user):
            raise Exception("You have no permission to download this file cause you are not a member of the band.")

        try:
            band_file = BandFile.objects.get(pk=bandfile_id)
        except BandFile.DoesNotExist:
            raise Exception("There is no file associated with id %s" % bandfile_id)

        return serve_file(request, band_file.file, save_as=True)

    except Exception as exc:
        context = {}
        context['error_msg'] = "Error: " + exc.message
        return render_to_response('error.html', context, context_instance=RequestContext(request))

@login_required
@require_GET
def show_files(request, band_id):
    context = {}
    try:
        band = bands_manager.get_band(band_id)
        if not band.is_member(request.user):
            # 403
            raise Exception("You have no permission to view this band cause you are not a member of it.")
        context['band'] = band
        view_url = reverse('project.views_band.upload_file', args=[band.id])
        upload_url, upload_data = prepare_upload(request, view_url)
        context['upload_form'] = UploadBandFileForm()
        context['upload_url'] = upload_url
        context['upload_data'] = upload_data
    except Exception as exc:
        # 500
        context['error_msg'] = "Error ocurred: %s" % exc.message
    return render_to_response('band/files.html', context, context_instance=RequestContext(request))

def __prepare_context(request, band):
    context = {}
    context['band'] = band
    view_url = reverse('project.views_band.upload_file', args=[band.id])
    upload_url, upload_data = prepare_upload(request, view_url)
    context['upload_form'] = UploadBandFileForm()
    context['upload_url'] = upload_url
    context['upload_data'] = upload_data
    return context

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
    
####################
# Events feature #
####################
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
        context['unavailability_form'] = UnavailabilityEntryForm()
        context['gig_form'] = UnavailabilityEntryForm()
        context['rehearsal_form'] = UnavailabilityEntryForm()
    except Exception as exc:
        # 500
        context['error_msg'] = "Error ocurred: %s" % exc.message
    return render_to_response('band/events.html', context, context_instance=RequestContext(request))
    
@login_required
@require_GET
def get_calendar_entries(request, band_id):
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
@require_POST
def add_unavailability(request, band_id):
    context = {}
    band = bands_manager.get_band(band_id)
    form = UnavailabilityEntryForm(request.POST)

    context['band'] = band
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
            context['success'] = "Unavailability added successfully!" # TODO: make this work with redirect or change the flow
            return redirect('/band/%s/events' % band_id)
        except Exception as exc:
            pass
            # 500
    else:
        print form.errors
        return render_to_response('band/events.html', context, context_instance=RequestContext(request))
    
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
        pass
        # 500
