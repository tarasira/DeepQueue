from __future__ import unicode_literals
import os

from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, PasswordInput
# Create your models here.
_STATUS_CHOICE = (('0', 'To do'), ('1', 'Doing'), ('2', 'Done'))
def user_input_path(instance, filename):
    return os.path.join(instance.user.username, 'input', filename)

def user_output_path(instance, filename):
    return os.path.join(instance.user.username, 'output', filename)

class Task(models.Model):
    user = models.ForeignKey(User, related_name='task_user')
    worker = models.ForeignKey(User, related_name='task_worker', null=True, blank=True)
    status = models.CharField(max_length=10, choices=_STATUS_CHOICE, default='0')
    describe = models.CharField(max_length=100, blank=True, default='')
    input_file = models.FileField(upload_to=user_input_path)
    output_file = models.FileField(upload_to=user_output_path, blank=True, null=True)
    input_time = models.DateTimeField(auto_now_add=True)
    output_time = models.DateTimeField(null=True, blank=True)
    request_time = models.DateTimeField(null=True, blank=True)


class WorkerForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': TextInput(),
            'password': PasswordInput(),
        }

class UploadTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['input_file', 'describe']