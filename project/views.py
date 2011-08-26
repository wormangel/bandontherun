# TODO: separate in two apps (user, band)

from django.http import HttpResponse
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

import users_manager, bands_manager

def index(request):
    if request.user.is_authenticated():
        return redirect('/user/dashboard')
    else:
        return render_to_response('index.html')

def about(request):
    return render_to_response('about.html')

#################
# account views #
#################
def dashboard(request):
    return render_to_response('user/dashboard.html', context_instance=RequestContext(request))

def show_user(request):
     return render_to_response('user/user.html')

def new_user(request):
    if request.method == 'GET':
        return render_to_response('user/new.html', context_instance=RequestContext(request))
    else:
        # The response MUST include an Allow header containing a list of valid methods for the requested resource. 
        return HttpResponse(status=405)

def create_user(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        phone = request.POST['phone']
        # TODO: validate input / use form
        accounts_manager.create_user(first_name, last_name, username, password, email, phone)
        user = authenticate(username=username, password=password)
        if user is not None:
            login_auth(request, user)
            return redirect('/')
        else:
            # TODO: append validation errors
            return redirect('/user/new')
    else:
        # The response MUST include an Allow header containing a list of valid methods for the requested resource. 
        return HttpResponse(status=405)

def edit_user(request):
    if request.method == 'GET':
        return render_to_response('user/edit.html', context_instance=RequestContext(request))
    else:
        # The response MUST include an Allow header containing a list of valid methods for the requested resource. 
        return HttpResponse(status=405)

def update_user(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        phone = request.POST['phone']
        # TODO: validate input
        user = accounts_manager.update_user(first_name, last_name, username, password, email, phone)
        if user is not None:
            return redirect('/user/dashboard')
        else:
            # TODO: append validation errors
            return redirect('/user/edit')
    else:
        # The response MUST include an Allow header containing a list of valid methods for the requested resource. 
        return HttpResponse(status=405)

def login(request):
    if request.method == 'GET':
        return render_to_response('user/login.html', context_instance=RequestContext(request))
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            next = request.GET['next']
        except:
            next = '/user/dashboard'
        user = authenticate(username=username, password=password)
        if user is not None:
            login_auth(request, user)
            return redirect(next)
        else:
            # error flag for message
            return redirect('/login?next=%s' % next)
    else:
        # The response MUST include an Allow header containing a list of valid methods for the requested resource. 
        return HttpResponse(status_code=405)

def logout(request):
    logout_auth(request)
    return redirect('/')

##############
# band views #
##############
def show_band(request):
    if request.method == 'GET':
        shortcut_name = request.GET['band_name']
        return render_to_response('band/show.html', {band: bands_manager.get_band(shortcut_name)}, context_instance=RequestContext(request))
    else:
        # The response MUST include an Allow header containing a list of valid methods for the requested resource. 
        return HttpResponse(status_code=405)

def new_band(request):
    if request.method == 'GET':
        return render_to_response('band/new.html', context_instance=RequestContext(request))
    else:
        # The response MUST include an Allow header containing a list of valid methods for the requested resource. 
        return HttpResponse(status_code=405)

def create_band(request):
    if request.method == 'POST':
        band_name = request.POST['band_name']
        shortcut_name = request.POST['shortcut_name']
        bio = request.POST['bio']
        url = request.POST['url']
        # TODO: validate input / use form
        bands_manager.create_band(band_name, shortcut_name, bio, url, request.user.profile)
        return redirect('/band/%s' % shortcut_name)
    else:
        # The response MUST include an Allow header containing a list of valid methods for the requested resource. 
        return HttpResponse(status_code=405)

def edit_band(request):
    if request.method == 'GET':
        band_name = request.GET['band_name']
        return render_to_response('band/edit.html', {band: bands_manager.get_band(band_name)}, context_instance=RequestContext(request))
    else:
        # The response MUST include an Allow header containing a list of valid methods for the requested resource. 
        return HttpResponse(status_code=405)

def update_band(request):
    if request.method == 'POST':
        band_name = request.POST['band_name']
        old_shortcut_name = request.POST['old_shortcut_name']
        new_shortcut_name = request.POST['new_shortcut_name']
        bio = request.POST['bio']
        url = request.POST['url']
        # TODO: validate input / use form
        if band is not None:
            bands_manager.update_band(band_name, shortcut_name, bio, url)
        else:
            # echo input vars on output
            return redirect('/band/%s/edit' % old_shortcut_name)
        return redirect('/band/%s' % band_name)
    else:
        # The response MUST include an Allow header containing a list of valid methods for the requested resource. 
        return HttpResponse(status_code=405)
