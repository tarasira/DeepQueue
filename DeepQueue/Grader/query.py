import os 
from datetime import timedelta
from Grader.models import *
from django.utils import timezone
from django.core.files.base import ContentFile
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.models import User, Group

def new_worker(**kwargs):
    user = User.objects.create_user(**kwargs)
    user.groups.add(Group.objects.get(name='worker'))
    sess = SessionStore()
    sess['_auth_user_id'] = user.id
    sess['_auth_user_hash'] = user.get_session_auth_hash()
    # sess.set_expiry(timedelta(days=365))
    sess.save()
    return user, sess


def upload_task(request):
    form = UploadTaskForm(request.POST, request.FILES)
    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        return True
    return False

def find_next_task():
    q = Task.objects.filter(status='0').order_by('input_time')
    return q[0] if len(q) != 0 else None

def release_prev_task(user):
    prev_task = Task.objects.filter(worker=user, status='1')
    if prev_task.exists():
        for task in prev_task:
            task.worker = None
            task.status = '0'
            task.request_time = None
            task.save()

def write_response(request):
    task = Task.objects.get(worker=request.user, status='1')
    tid = task.id
    fname = str(tid) +'.txt'
    content = ContentFile(request.POST.get('content'))
    task = Task.objects.get(id=tid)
    task.output_file.delete()
    task.output_file.save(fname, content)
    task.output_time = timezone.now()
    task.status = '2'
    task.save()
    print(task)

    # tid = request.META['HTTP_TASK_ID']
    # fname =tid +'.txt'
    # content = ContentFile(request.body)
    # task = Task.objects.get(id=tid)
    # task.output_file.delete()
    # task.output_file.save(fname, content)
    # task.output_time = timezone.now()
    # task.status = True
    # task.save()

