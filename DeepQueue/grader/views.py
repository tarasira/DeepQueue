import json
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.middleware import csrf
from auth.util import *
from grader.query import *
from grader.models import *
# Create your views here.
has_task_permission = lambda x: is_superuser(x) or is_worker(x)

class HomeView(LoginRequiredMixin, generic.CreateView):
    template_name = 'home.html'
    model = Task
    form_class = UploadTaskForm
    def form_valid(self, form):
        print('awf')
        upload_task(self.request)

    def post(self, request):
        upload_task(request)
        return redirect('/home/')

    def get_context_data(self, **kwargs):
        objs = None
        if is_student(self.request.user):
            objs = Task.objects.filter(user=self.request.user)
        if is_superuser(self.request.user):
            objs = Task.objects.all()
        print(super().get_context_data())
        return dict(
            super().get_context_data(**kwargs),
            task_list = objs,
            csrftoken = csrf.get_token(self.request)
        )

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
