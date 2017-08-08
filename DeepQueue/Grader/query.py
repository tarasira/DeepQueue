from Grader.models import *

def upload_task():
    form = UploadTaskForm(request.POST, request.FILES)
    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        return True
    return False

def _query_task():
	q = Task.objects.exclude(completed=True).order_by('-start_time')
	print q