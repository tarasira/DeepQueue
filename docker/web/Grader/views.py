import json
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

from Grader.query import *
from Grader.models import *
# Create your views here.
def _issuperuser(user):
    return user.is_superuser
def _isworker(user):    
    return user.groups.filter(name__in=['worker']).exists()
def has_task_permission(user):
    return _isworker(user) or _issuperuser(user)

@user_passes_test(_issuperuser)
def create_worker(request):
    template = 'create_worker.html'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user, sess = new_worker(username=username, password=password, email=email)
        return JsonResponse({'username':username, 'password':password, 'session_key':sess.session_key})
    else:
        form = WorkerForm()
    return render(request, template, {'form': form})

@csrf_exempt
@user_passes_test(has_task_permission)
def get_task(request):
    release_prev_task(request.user)
    task = find_next_task()
    if not task:
        return HttpResponse(status=204)
    else: 
        task.worker = request.user
        task.status = '1'
        task.request_time = timezone.now()
        task.save()
        res = HttpResponse(content_type='text/plain', status=200)
        res['task-id'] = task.id
        res.content = task.input_file.read()
        return res


@csrf_exempt
def user_login(request):
    template = 'login.html'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            login(request, user)
            if _isworker(user):
                print(request.session)
                res = HttpResponse(content_type='text/plain', status=200)
                res.content = request.session.session_key
                return res
            elif user.is_superuser:
                return redirect('/admin')

            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def upload(request):
    template = 'upload.html'
    if request.method == 'POST':
        if upload_task(request):
            return HttpResponse('C O M P L E T E')
    else:
        form = UploadTaskForm()
    return render(request, 'upload.html', {'form': form})

# @user_passes_test(_issuperuser)
# send with this curl cmd
# curl -H "task-id: 1" -d @hello.txt localhost:8000/writetask/
@csrf_exempt
@user_passes_test(has_task_permission)
def write_task(request):
    if request.method == 'POST':
        write_response(request)
        return HttpResponse(status=200)
    return HttpResponse(status=400)
    # tid = request.META['HTTP_TASK_ID']
    # if Task.objects.get(id=tid).worker != request.user:
    #     return HttpResponse(status=301)
    # if request.method == 'POST':
    #     write_response(request)
    #     return HttpResponse(status=200)
