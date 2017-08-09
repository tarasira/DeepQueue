from django.contrib.auth.models import User
if User.objects.filter(username="admin").exists():
	admin=User.objects.get(username="admin")
	print("Found superuser: {}".format(admin))
else:
	admin=User.objects.create_superuser('admin', 'admin@example.com', 'qwer1234')
	print("Created superuser: {}".format(admin))
