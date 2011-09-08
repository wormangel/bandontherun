# TODO: change some posts request to put / delete (investigate how to do that with django)

from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

from forms import UserCreateForm, UserEditForm, LoginForm
import users_manager

@login_required
@require_GET
def dashboard(request):
    return render_to_response('user/dashboard.html', context_instance=RequestContext(request))

@login_required
@require_GET
def show_user(request, username):
    context = {}
    context_instance = RequestContext(request)
    
    try:
        user = users_manager.get_user(username)
        context['profile_user'] = user
    except Exception as exc:
        # 500
        context['error_msg'] = "Error ocurred: %s" % exc.message
    return render_to_response('user/show.html', context, context_instance=context_instance)

@require_http_methods(["GET", "POST"])
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
                # 400
                form.errors['__all__'] = form.error_class(["Error: %s" % exc.message])
    else:
        form = UserCreateForm()

    # GET / POST with invalid input
    context['form'] = form
    return render_to_response('user/create.html', context, context_instance=context_instance)

@require_http_methods(["GET", "POST"])
def create_invited_user(request, email, key):
    context = {}
    context_instance = RequestContext(request)

    if request.user.is_authenticated():
        return redirect('/user/dashboard')

    if request.method == 'POST':
        form = InvitedUserCreateForm(request.POST)
        if form.is_valid() and users_manager.invitation_exists(email, key):
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            phone = form.cleaned_data['phone']
            try:
                users_manager.create_user(first_name, last_name, username, password, email, phone)
                # authenticate and login
                user = authenticate(username=username, password=password)
                login_auth(request, user)
                return redirect('/user/dashboard')
            except Exception as exc:
                # 400
                form.errors['__all__'] = form.error_class(["Error: %s" % exc.message])
    elif users_manager.invitation_exists(email, key):
        form = InvitedUserCreateForm({email: email})
    else:
        # 404
        pass

    # GET / POST with invalid input
    context['form'] = form
    return render_to_response('user/create.html', context, context_instance=context_instance)


@login_required
@require_http_methods(["GET", "POST"])
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
                    # 400
                    form.errors['__all__'] = form.error_class(["Error: passwords didn't match."])
                    error = True
            elif (new_password and not new_password_confirm) or (new_password_confirm and not new_password):
                # 400
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

@require_http_methods(["GET", "POST"])
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
                # 400
                form.errors['__all__'] = form.error_class(["Login failure. Verify your user/password combination"])
    else:
        form = LoginForm()

    # GET / POST with invalid input
    context['form'] = form
    return render_to_response('user/login.html', context, context_instance=context_instance)

@login_required
@require_GET
def logout(request):
    logout_auth(request)
    return redirect('/')

# TODO
@login_required
@require_http_methods(["GET", "POST"])
def invite_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        users_manager.invite_user(email)
