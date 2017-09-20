from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm

from myauth.util import *

@csrf_exempt
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        print('post', request.POST)
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usr = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            user = authenticate(request, username=usr, password=pwd)
            print(user)
            if not user is None:
                auth_login(request, user)
                if is_worker(user):
                    print(request.session)
                    res = HttpResponse(content_type='text/plain', status=200)
                    res.content = request.session.session_key
                    return res
                return HttpResponseRedirect(requestrequest.POST.get('next', '/'))
            else:
                return HttpResponse(status=400)
    else:
        context = {'form': AuthenticationForm(request)}
        return render(request, 'login.html', context)