import json
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, FileResponse
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.views import generic
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.middleware import csrf
from myauth.util import *
from grader.query import *
from grader.models import *
# Create your views here.
has_task_permission = lambda x: is_superuser(x) or is_worker(x)
file_mode = {'inpt': 'input_file', 'oupt': 'output_file'}
class HomeView(LoginRequiredMixin, FormMixin, ListView ):
    template_name = 'home.html'
    model = Task
    paginate_by = 10
    context_object_name = 'task_list'
    form_class = UploadTaskForm

    def post(self, request, *args, **kwargs):
        upload_task(request)
        return HttpResponseRedirect('/')

    def get_queryset(self):
        if is_superuser(self.request.user):
            return Task.objects.all()
        else:
            return Task.objects.filter(user=self.request.user)


@user_passes_test(is_superuser)
def create_worker(request):
    template = 'create_worker.html'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user, sess = new_worker(username=username, password=password, email=email)
        return JsonResponse({'username':username, 'password':password, \
            'session_key':sess.session_key})
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

@login_required
def view(request, task_id, mode):
    task = Task.objects.get(id=task_id)
    if (task and task.user == request.user) or is_superuser(request.user):
        return render(request, 'view.html', {'content':getattr(task, file_mode[mode]).read().decode()} )

@login_required
def upload(request):
    template = 'upload.html'
    if request.method == 'POST':
        if upload_task(request):
            return HttpResponse('C O M P L E T E')
    else:
        form = UploadTaskForm()
    return render(request, template, {'form': form})

@csrf_exempt
@user_passes_test(has_task_permission)
def write_task(request):
    if request.method == 'POST':
        write_response(request)
        return HttpResponse(status=200)
    return HttpResponse(status=400)

