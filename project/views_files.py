from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import  require_GET, require_POST
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from datetime import datetime
from filetransfers.api import prepare_upload, serve_file
from models import Band, User, BandFile
from forms import   UploadBandFileForm

import  bands_manager

@login_required
@require_POST
def upload_file(request, band_id):
    view_url = reverse('upload-band-file', args=[band_id])

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
            return render_to_response("band/files.html", context, context_instance=RequestContext(request))
    else:
        context['error_msg'] = "Invalid file."
        return render_to_response("band/files.html", context, context_instance=RequestContext(request))
    return render_to_response("band/files.html", context, context_instance=RequestContext(request))

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
        view_url = reverse('upload-band-file', args=[band.id])
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
    view_url = reverse('upload-band-file', args=[band.id])
    upload_url, upload_data = prepare_upload(request, view_url)
    context['upload_form'] = UploadBandFileForm()
    context['upload_url'] = upload_url
    context['upload_data'] = upload_data
    return context