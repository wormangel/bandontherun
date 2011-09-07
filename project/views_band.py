# TODO: change some posts request to put / delete (investigate how to do that with django)

from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse

from filetransfers.api import prepare_upload
from models import Band, User, BandFile
from forms import BandCreateForm, BandEditForm, UploadBandFileForm, UploadBandFileForm
import users_manager
import bands_manager

from datetime import datetime

@login_required
@require_GET
def show_band(request, band_id):
    band = bands_manager.get_band(band_id)
    context, context_instance = __prepare_context(request, band)
    try:
        user = request.user
        if band is not None:
            if band.is_member(user):
                return render_to_response('band/show.html', context, context_instance=context_instance)
            else:
                # 403
                context['error_msg'] = "You have no permission to view this band cause you are not a member of it."
                return render_to_response('band/show.html', context, context_instance=context_instance)
        else:
            # 404
            context['error_msg'] = "There is no band associated with id '%d'." % band_id
            return render_to_response('band/show.html', context, context_instance=context_instance)
    except Exception as exc:
        # 500
        context['error_msg'] = "Error ocurred: %s" % exc.message
        return render_to_response('band/show.html', context, context_instance=context_instance)

@login_required
@require_http_methods(["GET", "POST"])
def create_band(request):
    context = {}
    context_instance = RequestContext(request)

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
    return render_to_response('band/create.html', context, context_instance=context_instance)

@login_required
@require_http_methods(["GET", "POST"])
def edit_band(request, band_id):
    context = {}
    context_instance = RequestContext(request)

    if bands_manager.exists(band_id):
        if request.method == 'POST':
            form = BandEditForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                bio = form.cleaned_data['bio']
                url = form.cleaned_data['url']
                bands_manager.update_band(band_id, name, bio, url)
                context['success'] = True
        else: # request.method == GET
            band = bands_manager.get_band(band_id)
            data = {'name': band.name,
                    'bio': band.bio,
                    'url': band.url,}
        context['form'] = BandEditForm(data)
        context['band_id'] = band_id
    else:
        # 404
        context['error_msg'] = "There is no band associated with id %d." % band_id

    return render_to_response('band/edit.html', context, context_instance=context_instance)

@login_required
@require_POST
def add_band_member(request, band_id):
    context = {}
    context_instance = RequestContext(request)
    
    # TODO: validate input / use form
    # validate if user updating the info is a member
    username = request.POST['username']
    if bands_manager.exists(band_id):
        if users_manager.exists(username):
            bands_manager.add_band_member(band_id, users_manager.get_user(username))
            return redirect('/band/%d' % band_id)
        else:
            # 404
            context['error_msg'] = "There is no user called '%s'." % username
            return render_to_response('band/show.html', context, context_instance=context_instance)
    else:
        # 404
        context['error_msg'] = "There is no band associated with id '%d'." % band_id
        return render_to_response('band/show.html', context, context_instance=context_instance)

@login_required
@require_POST
def remove_band_member(request, band_id, username):
    # TODO: validate input / use form
    # validate if user updating the info is a member
    if bands_manager.exists(band_id):
        bands_manager.remove_band_member(band_id, username)
        return redirect('/band/%s' % band_id)
    else:
        # TODO: see how to handle this better
        return HttpResponse(status=404)
        
@login_required
@require_POST
def upload_file(request, band_id):
    view_url = reverse('project.views_band.upload_file', args=[band_id])
    
    user = User.objects.get(username=request.user.username)
    band = Band.objects.get(id=band_id)
    context, context_instance = __prepare_context(request, band)
    form = UploadBandFileForm(request.POST, request.FILES)
    
    if form.is_valid():
        if band.is_member(user):
            file = request.FILES['file']    
            band_file = form.save(commit=False)
            band_file.filename= file.name
            band_file.size = file.size
            band_file.uploader = user.username
            band_file.band = band
            band_file.created = datetime.now()
            band_file.save()
            return render_to_response('band/show.html', context, context_instance=context_instance)
        else:
            context['error_msg'] = "You have no permission to upload a file to this band cause you are not a member of it."
            return render_to_response('band/show.html', context, context_instance=context_instance) 
    context['upload_form'] = form 
    return render_to_response('band/show.html', context, context_instance=context_instance)

@login_required
@require_POST
def delete_file(request, band_id, username, bandfile_id):
    context, context_instance = __prepare_context(request, Band.objects.get(id=band_id))
    
    band_file = BandFile.objects.get(id=bandfile_id)
    if band_file:
        if Band.objects.get(id=band_id).is_member(User.objects.get(username=username)):
            band_file.file.delete()
            band_file.delete()
        else:
            context['error_msg'] = "You have no permission to delete a file to this band cause you are not a member of it."
            return render_to_response('band/show.html', context, context_instance=context_instance)   
    else:
        context['error_msg'] = "Invalid file."
        return render_to_response('band/show.html', context, context_instance=context_instance)   
    return render_to_response('band/show.html', context, context_instance=context_instance)


def __prepare_context(request, band):
    context = {}
    context['band'] = band
    view_url = reverse('project.views_band.upload_file', args=[band.id])
    upload_url, upload_data = prepare_upload(request, view_url)
    context['upload_form'] = UploadBandFileForm()
    context['upload_url'] = upload_url
    context['upload_data'] = upload_data
    return context, RequestContext(request)
