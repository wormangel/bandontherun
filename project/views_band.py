# TODO: change some posts request to put / delete (investigate how to do that with django)

from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.shortcuts import render_to_response, redirect

from models import Band, User, BandFile
from forms import BandCreateForm, BandEditForm, UploadBandFileForm, UploadBandFileForm
import users_manager
import bands_manager

@login_required
@require_GET
def show_band(request, band_id):
    context = {}
    context_instance = RequestContext(request)
    try:
        band = bands_manager.get_band(band_id)
        user = request.user
        if band is not None:
            if band.is_member(user):
                context['band'] = band
                context['upload_form'] = UploadBandFileForm()
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
def upload_file(request, band_id, username):
    context_instance = RequestContext(request)
    form = UploadBandFileForm(request.POST, request.FILES)
    if form.is_valid():
        if Band.objects.get(id=band_id).is_member(User.objects.get(username=username)):
            name = form.cleaned_data['name']
            bands_manager.add_file(band_id, name, username, request.FILES['bandfile'])
            return redirect('/band/%s' % band_id)
        else:
            context['error_msg'] = "You have no permission to upload a file to this band cause you are not a member of it."
            return render_to_response('band/show.html', context, context_instance=context_instance)            
    return render_to_response('band/show.html', {'form': form}, context_instance=context_instance)

@login_required
@require_POST
def delete_file(request, band_id, username, bandfile_id):
    context_instance = RequestContext(request)
    
    context = {}
    context['band'] = bands_manager.get_band(band_id)
    context['form'] = UploadBandFileForm()
    
    if BandFile.objects.get(id=bandfile_id):
        if Band.objects.get(id=band_id).is_member(User.objects.get(username=username)):
            bands_manager.delete_file(bandfile_id)
        else:
            context['error_msg'] = "You have no permission to delete a file to this band cause you are not a member of it."
            return render_to_response('band/show.html', context, context_instance=context_instance)   
    else:
        context['error_msg'] = "Invalid file."
        return render_to_response('band/show.html', context, context_instance=context_instance)   
    return render_to_response('band/show.html', context, context_instance=context_instance)


