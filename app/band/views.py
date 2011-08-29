from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

from models import Band
from forms import BandCreateForm, BandEditForm
from user import users_manager
import bands_manager

@login_required
def show_band(request, band_id):
    context = {}
    context_instance = RequestContext(request)

    try:
        band = bands_manager.get_band(band_id)
        if band is not None:
            context['band'] = band
            return render_to_response('show.html', context, context_instance=context_instance)
        else:
            context['error_msg'] = "There is no band associated with id '" + id + "'."
            return render_to_response('show.html', context, context_instance=context_instance)
    except Exception as exc:
        context['error_msg'] = "Error ocurred: " + exc.message
        return render_to_response('show.html', context, context_instance=context_instance)

@login_required
def create_band(request):
    context = {}
    context_instance = RequestContext(request)

    if request.method == 'POST':
        form = BandCreateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['band']
            bio = form.cleaned_data['bio']
            url = form.cleaned_data['url']
            try:
                bands_manager.create_band(band_name, bio, url, request.user)
                return redirect('/band/%d' % band_id)
            except Exception as exc:
                form.errors['__all__'] = form.error_class(["Error: " + exc.message])
    else: # request.method == GET
        form = BandCreateForm()

    # GET / POST with invalid input
    context['form'] = form
    return render_to_response('create.html', context, context_instance=context_instance)

@login_required
def edit_band(request, band_id):
    context = {}
    context_instance = RequestContext(request)

    if band_manager.exists(band_id):
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
            data = {'band_name': band.name,
                    'bio': band.bio,
                    'url': band.url,}
            context['form'] = BandEditForm(data)
    else:
        context['error_msg'] = "There is no band with the specified shortcut name."

    return render_to_response('edit.html', context, context_instance=context_instance)

@login_required
def add_band_member(request, band_id):
    context = {}
    context_instance = RequestContext(request)
    
    # TODO: validate input / use form
    # validate if user updating the info is a member
    if request.method == 'POST':
        username = request.POST['username']
        if bands_manager.exists(band_id):
            if users_manager.exists(username):
                bands_manager.add_band_member(band_id, username)
                return redirect('/band/%d' % band_id)
            else:
                context['error_msg'] = "There is no user called '" + username + "'."
                return render_to_response('show.html', context, context_instance=context_instance)
        else:
            context['error_msg'] = "There is no band associated with id '" + band_id + "'."
            return render_to_response('show.html', context, context_instance=context_instance)
    else:
        # The response MUST include an Allow header containing a list of valid methods for the requested resource. 
        return HttpResponse(status_code=405)

@login_required
def remove_band_member(request, band_id, username):
    if request.method == 'POST':
        # TODO: validate input / use form
        # validate if user updating the info is a member
        if bands_manager.exists(band_id):
            if bands_manager.is_member(username):
                bands_manager.remove_band_member(band_id, users_manager.get_user(username))
                return redirect('/band/%d' % band_name)
            else:
                # TODO: see how to handle this better
                return HttpResponse(status_code=404)
        else:
            # TODO: see how to handle this better
            return HttpResponse(status_code=404)
    else:
        # The response MUST include an Allow header containing a list of valid methods for the requested resource. 
        return HttpResponse(status_code=405)
