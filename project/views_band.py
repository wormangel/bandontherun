# TODO: change some posts request to put / delete (investigate how to do that with django)
from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.utils import simplejson as json
from django.core.urlresolvers import reverse

from datetime import datetime
from filetransfers.api import prepare_upload, serve_file
from models import Band, User, BandFile, CalendarEntry, Contact
from forms import BandCreateForm, BandEditForm, UploadBandFileForm, ContactBandForm, CalendarEntryForm

import users_manager
import bands_manager

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
# Calendar feature #
####################
@login_required
@require_GET
def show_calendar(request, band_id):
    context = {}
    try:
        band = bands_manager.get_band(band_id)
        if not band.is_member(request.user):
            # 403
            raise Exception("You have no permission to view this band cause you are not a member of it.")
        context['band'] = band
        context['form'] = CalendarEntryForm()
    except Exception as exc:
        # 500
        context['error_msg'] = "Error ocurred: %s" % exc.message
    return render_to_response('band/calendar.html', context, context_instance=RequestContext(request))
    
@login_required
@require_GET
def get_calendar_entries(request, band_id):
    context = {}
    try:
        band = bands_manager.get_band(band_id)
        if not band.is_member(request.user):
            # 403
            raise Exception("You have no permission to view this band cause you are not a member of it.")
        context['entries'] = list(band.calendar_entries)
    except Exception as exc:
        # 500
        context['error_msg'] = "Error ocurred: %s" % exc.message
    return HttpResponse(json.dumps(context), mimetype='application/json')
    
@login_required
@require_POST
def add_calendar_entry(request, band_id):
    context = {}
    band = bands_manager.get_band(band_id)
    form = CalendarEntryForm(request.POST)

    context['band'] = band
    context['form'] = form

    if form.is_valid():
        date = form.cleaned_data['date'] 
        start = form.cleaned_data['start']
        end = form.cleaned_data['end']
        try:
            if not band.is_member(request.user):
                raise Exception("You have no permission to add songs to this band's setlist cause you are not a member of it.")
            bands_manager.add_calendar_entry(band_id, date, start, end)
            return redirect('/band/%s/calendar' % band_id)
        except Exception as exc:
            context['error_msg'] = "Error ocurred: %s" % exc.message
    return render_to_response('band/calendar.html', context, context_instance=RequestContext(request))
