from django.contrib import admin
from .models import *

class TaskAdmin(admin.ModelAdmin):
	list_display=[f.name for f in Task._meta.fields]
	list_filter=("completed", "user__username")
	search_fields = ('describe', 'user__username')

admin.site.register(Task,TaskAdmin)	