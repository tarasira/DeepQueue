from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
# Create your models here.

def user_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.user.username, filename)

class Task(models.Model):
	user = models.ForeignKey(User)
	input_file = models.FileField(upload_to=user_directory_path)
	output_file = models.FileField(upload_to=user_directory_path, blank=True, null=True)
	describe = models.CharField(max_length=100, blank=True)
	completed = models.BooleanField(default=False)
	start_time = models.DateTimeField(auto_now_add=True)
	complete_time = models.DateTimeField(null=True, blank=True)
	complete_time2 = models.DateTimeField(null=True, blank=True)

class UploadTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['input_file', 'describe']