# TODO: separate in two apps (user, band)

from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.shortcuts import render_to_response, redirect

import band_manager, accounts_manager

def index(request):
    if request.user.is_authenticated():
        redirect('/dashboard')
    else:
        return render_to_response('index.html')

# account views
def dashboard(request):
    return render_to_response('accounts/dashboard.html')

def login(request):
    if request.method == 'GET':
        return render_to_response('accounts/login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next = request.GET['next'] if request.GET['next'] else '/dashboard'
        user = authenticate(username=username, password=password)
        if user is not None:
            login_auth(request, user)
            redirect(next)
        else:
            # flag de erro
            redirect('/login?next=%s' % next)
        
def logout(request):
    logout_auth(request)
    redirect('/')

# band views
def show_band(request):
    if request.method == 'GET':
        return render_to_response('band/show.html')
    else:
        # The response MUST include an Allow header containing a list of valid methods for the requested resource. 
        return HttpResponse(status_code=405)

def new_band(request):
    if request.method == 'GET':
        return render_to_response('band/new.html')
    else:
        # The response MUST include an Allow header containing a list of valid methods for the requested resource. 
        return HttpResponse(status_code=405)

def create_band(request):
    if request.method == 'POST':
        return redirect('/band/' + band_name)
    else:
        # The response MUST include an Allow header containing a list of valid methods for the requested resource. 
        return HttpResponse(status_code=405)

def edit_band(request):
    if request.method == 'GET':
        return render_to_response('band/edit.html')
    else:
        # The response MUST include an Allow header containing a list of valid methods for the requested resource. 
        return HttpResponse(status_code=405)

def update_band(request):
    if request.method == 'POST':
        return redirect('/band/' + band_name)
    else:
        # The response MUST include an Allow header containing a list of valid methods for the requested resource. 
        return HttpResponse(status_code=405)
