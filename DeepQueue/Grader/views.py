import json
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from Grader.query import *
from Grader.models import *
# Create your views here.
def _issuperuser(user):
    return user.is_superuser
def _isworker(user):    
    return user.groups.filter(name__in=['worker']).exists()
def has_task_permission(user):
    return _isworker(user) or _issuperuser(user)

@csrf_exempt
@user_passes_test(has_task_permission)
def get_task(request):
    # chk failure worker
    print(request.session.session_key)
    prev_task = Task.objects.filter(worker=request.user, status='1')
    if prev_task.exists():
        for task in prev_task:
            task.worker = None
            task.status = '0'
            task.request_time = None
            task.save()

    task = find_next_task()
    if task:
        task.worker = request.user
        task.status = '1'
        task.request_time = timezone.now()
        task.save()
        res = HttpResponse(content_type='text/plain', status=200)
        res['task-id'] = task.id
        res.content = task.input_file.read()
        return res
    return HttpResponse(status=204) 

# @user_passes_test(_issuperuser)
# send with this curl cmd
# curl -H "task-id: 1" -d @hello.txt localhost:8000/writetask/
@csrf_exempt
@user_passes_test(has_task_permission)
def write_task(request):
    tid = request.META['HTTP_TASK_ID']
    if Task.objects.get(id=tid).worker != request.user:
        return HttpResponse(status=301)
    if request.method == 'POST':
        write_response(request)
        return HttpResponse(status=200)

@login_required
def upload(request):
    template = 'upload.html'
    if request.method == 'POST':
    	if upload_task(request):
    		return HttpResponse('C O M P L E T E')
    else:
        form = UploadTaskForm()
    return render(request, 'upload.html', {'form': form})