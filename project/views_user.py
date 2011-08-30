# TODO: create decorators for @get @post @put @delete
# TODO: change some posts request to put (investigate how to do that with django)

from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

from forms import UserCreateForm, UserEditForm, LoginForm
import users_manager
import bands_manager

#################
# account views #
#################
@login_required
def dashboard(request):
    return render_to_response('user/dashboard.html', context_instance=RequestContext(request))

@login_required
def show_user(request, username):
    context = {}
    context_instance = RequestContext(request)
    
    try:
        if users_manager.exists(username):
            context['profile_user'] = users_manager.get_user(username)
            return render_to_response('user/show.html', context, context_instance=context_instance)
        else:
            context['error_msg'] = "There is no user called '" + username + "'."
            return render_to_response('user/show.html', context, context_instance=context_instance)
    except Exception as exc:
        context['error_msg'] = "Error ocurred: " + exc.message
        return render_to_response('user/show.html', context, context_instance=context_instance)

def create_user(request):
    context = {}
    context_instance = RequestContext(request)

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
                return redirect('/user/dashboard')
            except Exception as exc:
                form.errors['__all__'] = form.error_class(["Error: " + exc.message])
    else:
        form = UserCreateForm()

    # GET / POST with invalid input
    context['form'] = form
    return render_to_response('user/create.html', context, context_instance=context_instance)

@login_required
def edit_user(request):
    context = {}
    context_instance = RequestContext(request)

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
                new_password = None

            if not error:
                user = users_manager.update_user(request.user, first_name, last_name, new_password, email, phone)
                context['success'] = not error
    else:
        data = {'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'phone': request.user.profile.phone,}
        form = UserEditForm(data)

    # GET / POST with invalid input
    context['form'] = form
    return render_to_response('user/edit.html', context, context_instance=context_instance)

def login(request):
    context = {}
    context_instance = RequestContext(request)

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
                return redirect(next)
            else:
                form.errors['__all__'] = form.error_class(["Login failure. Verify your user/password combination"])
    else:
        form = LoginForm()

    # GET / POST with invalid input
    context['form'] = form
    return render_to_response('user/login.html', context, context_instance=context_instance)

@login_required
def logout(request):
    logout_auth(request)
    return redirect('/')

# TODO
@login_required
def invite_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        users_manager.invite_user(email)
