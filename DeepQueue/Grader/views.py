from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from Grader.query import *
from Grader.models import *
# Create your views here.

def get_task(request):
	# _query_task()
	q = Task.objects.exclude(completed=True).order_by('start_time')
	if len(q) != 0:
		print q[0].start_time
	else:
		print None

@login_required
def upload(request):
    template = 'upload.html'
    if request.method == 'POST':
    	if upload_task(request):
    		return HttpResponse('C O M P L E T E')
    else:
        form = UploadTaskForm()
    return render(request, 'upload.html', {'form': form})