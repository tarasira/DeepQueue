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
    return HttpResponseRedirect('/login/')

@csrf_exempt
def login(request):
    context = {'form': AuthenticationForm(request)}
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usr = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            user = authenticate(request, username=usr, password=pwd)
            if not user is None and user.is_active:
                auth_login(request, user)
                if is_worker(user):
                    res = HttpResponse(content_type='text/plain', status=200)
                    res.content = request.session.session_key
                    return res
                return HttpResponseRedirect('/')
        context['error_message'] = "Incorrect username or password."
    return render(request, 'login.html', context)