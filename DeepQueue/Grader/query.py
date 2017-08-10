import os 
from Grader.models import *
from django.utils import timezone
from django.core.files.base import ContentFile

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

def write_response(request):
	tid = request.META['HTTP_TASK_ID']
	fname =tid +'.txt'
	content = ContentFile(request.body)
	task = Task.objects.get(id=tid)
	task.output_file.delete()
	task.output_file.save(fname, content)
	task.output_time = timezone.now()
	task.status = True
	task.save()
