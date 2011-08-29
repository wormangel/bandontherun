# TODO: separate in two apps (user, band)
# TODO: create decorators for @get @post @put @delete
# TODO: change some posts request to put (investigate how to do that with django)

from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

from models import Band
from forms import *

import users_manager, bands_manager

def index(request):
    if request.user.is_authenticated():
        return redirect('/user/dashboard')
    else:
        return render_to_response('index.html', context_instance=RequestContext(request))

def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))

#################
# account views #
#################
@login_required
def dashboard(request):
    return render_to_response('user/dashboard.html', context_instance=RequestContext(request))

@login_required
def show_user(request, username):
    try:
        profile_user = users_manager.get_user(username)
        if profile_user is None:
            return render_to_response('user/show.html', {'error_msg': "There is no user called\'" + username + "\'."}, context_instance=RequestContext(request))
        else:
            return render_to_response('user/show.html', {'profile_user': profile_user}, context_instance=RequestContext(request))
    except Exception as exc:
        return render_to_response('user/show.html', {'error_msg': "Error ocurred: " + exc.message}, context_instance=RequestContext(request))


@login_required
def invite_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        users_manager.invite_user(email)

def create_user(request):
    if request.user.is_authenticated():
        return redirect('/user/dashboard')

    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            try:
                users_manager.create_user(first_name, last_name, username, password, email, phone)
                # authenticate and login
                user = authenticate(username=username, password=password)
                login_auth(request, user)
                return HttpResponseRedirect('/user/dashboard')
            except Exception as exc:
                form.errors['__all__'] = form.error_class(["Error: " + exc.message])
    else:
        form = UserCreateForm()
    return render_to_response('user/create.html', { 'form' : form }, context_instance=RequestContext(request))

@login_required
def edit_user(request):
    context = {}
    if request.method == 'POST':
        form = UserEditForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            new_password =  form.cleaned_data['new_password']
            new_password_confirm = form.cleaned_data['new_password_confirm']

            error = False
            if new_password and new_password_confirm:
                if (new_password != new_password_confirm):
                    form.errors['__all__'] = form.error_class(["Error: passwords didn't match."])
                    error = True
            elif (new_password and not new_password_confirm) or (new_password_confirm and not new_password):
                form.errors['__all__'] = form.error_class(["Error: you must input the desired password twice."])
                error = True
            else:
                print 'NAO MUDOU SENHA'
                new_password = None

            if not error:
                user = users_manager.update_user(request.user, first_name, last_name, new_password, email, phone)

            context['success'] = not error
    else:
        data = {'first_name':request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'phone': request.user.profile.phone,}
        form = UserEditForm(data)

    context['form'] = form
    return render_to_response('user/edit.html', context, context_instance=RequestContext(request))

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                next = request.GET['next']
            except:
                next = '/user/dashboard'

            user = authenticate(username=username, password=password)
            if user is not None:
                login_auth(request, user)
                return HttpResponseRedirect(next)
            else:
                form.errors['__all__'] = form.error_class(["Login failure. Verify your user/password combination"])
    else:
        form = LoginForm()    
    return render_to_response('user/login.html', {'form' : form}, context_instance=RequestContext(request))

@login_required
def logout(request):
    logout_auth(request)
    return redirect('/')

##############
# band views #
##############
@login_required
def show_band(request, shortcut_name):
    if request.method == 'GET':
        return render_to_response('band/show.html', {'band': bands_manager.get_band(shortcut_name)}, context_instance=RequestContext(request))
    else:
        # The response MUST include an Allow header containing a list of valid methods for the requested resource. 
        return HttpResponse(status_code=405)

@login_required
def create_band(request):
    if request.method == 'POST':
        form = BandForm(request.POST)
        if form.is_valid():
            band_name = form.cleaned_data['band_name']
            shortcut_name = form.cleaned_data['shortcut_name']
            bio = form.cleaned_data['bio']
            url = form.cleaned_data['url']
            bands_manager.create_band(band_name, shortcut_name, bio, url, request.user)
            return HttpResponseRedirect('/band/%s' % shortcut_name)
    else:
        form = BandForm()
    return render_to_response('band/create.html', { 'form' : form }, context_instance=RequestContext(request))

@login_required
def edit_band(request, shortcut_name):
    if request.method == 'POST':
        form = BandForm(request.POST)
        if form.is_valid():
            band_name = form.cleaned_data['band_name']
            shortcut_name = form.cleaned_data['shortcut_name']
            bio = form.cleaned_data['bio']
            url = form.cleaned_data['url']
            bands_manager.update_band(band_name, shortcut_name, new_shortcut_name, bio, url)
            return HttpResponseRedirect('/band/%s' % band_name)
    else:
        form = BandForm()
    return render_to_response('band/edit.html', {'band': bands_manager.get_band(shortcut_name), 'form' : form}, context_instance=RequestContext(request))

@login_required
def add_band_member(request, shortcut_name):
    if request.method == 'POST':
        username = request.POST['username']
        # TODO: validate input / use form
        # validate if user updating the info is a member
        band = Band.objects.filter(name=shortcut_name)[0]
        if band is not None:
            bands_manager.add_band_member(shortcut_name, users_manager.get_user(username)[0])
        else:
            # echo input vars on output
            return redirect('/band/%s' % shortcut_name)
        return redirect('/band/%s' % shortcut_name)
    else:
        # The response MUST include an Allow header containing a list of valid methods for the requested resource. 
        return HttpResponse(status_code=405)

@login_required
def remove_band_member(request, shortcut_name):
    if request.method == 'POST':
        member = request.POST['member']
        # TODO: validate input / use form
        # validate if user updating the info is a member
        if band is not None:
            bands_manager.remove_band_member(shortcut_name, users_manager.get_user(member))
        else:
            pass
            # echo input vars on output
        return redirect('/band/%s' % shortcut_name)
    else:
        # The response MUST include an Allow header containing a list of valid methods for the requested resource. 
        return HttpResponse(status_code=405)
