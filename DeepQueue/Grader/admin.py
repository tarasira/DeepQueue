from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import *

# class TaskInline(admin.TabularInline):
# 	model = Task
# class TestInlineAdmin(admin.ModelAdmin):
# 	inlines = [TaskInline]
# admin.site.register(Task,TestInlineAdmin)	

# class UserProfileInline(admin.StackedInline):
#     model = User
#     max_num = 1
#     can_delete = False
# class AccountsUserAdmin(admin.ModelAdmin):
#     inlines = [UserProfileInline]
# admin.site.unregister(User)
# admin.site.register(User, AccountsUserAdmin)
class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
admin.site.register(Session, SessionAdmin)

class TaskAdmin(admin.ModelAdmin):
	list_display=[f.name for f in Task._meta.fields]
	list_filter=("status", "user__username")
	search_fields = ('describe', 'user__username')
admin.site.register(Task,TaskAdmin)	