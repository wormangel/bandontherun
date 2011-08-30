from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

def index(request):
    if request.user.is_authenticated():
        return redirect('/user/dashboard')
    else:
        return render_to_response('index.html', context_instance=RequestContext(request))

def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))
