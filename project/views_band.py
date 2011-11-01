# TODO: change some posts request to put / delete (investigate how to do that with django)
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse

from filetransfers.api import prepare_upload
from forms import BandCreateForm, BandEditForm, UploadBandFileForm

import users_manager, bands_manager

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
        context['band'] = band
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
        context['band'] = band
        return render_to_response('band/show.html', context, context_instance=RequestContext(request))
        
def __prepare_context(request, band):
    context = {}
    context['band'] = band
    view_url = reverse('upload-band-file', args=[band.id])
    upload_url, upload_data = prepare_upload(request, view_url)
    context['upload_form'] = UploadBandFileForm()
    context['upload_url'] = upload_url
    context['upload_data'] = upload_data
    return context
