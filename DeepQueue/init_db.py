import os
import json
from collections import defaultdict
from django.contrib.auth.models import User, Group

print()
print('='*40)
_secret_path = os.path.join('secret','setup.json')
print("Read secret variable")
try:
    with open(_secret_path, 'r') as fp:
        secret_var = json.load(fp)
except FileNotFoundError as err:
    secret_var = {
        'admin_email': '',
        'admin_username': 'admin',
        'admin_password': 'qwer1234'
    }
    print('********************************************')
    print('!!! Secret File Not Found, use default value')
    print('********************************************')
    for k, v in secret_var.items():
        print('\t{}: {}'.format(k, v))
secret_var = defaultdict(str, secret_var)

print()
print("- Create Admin user")
User.objects.create_superuser(
    username=secret_var['admin_username'], 
    password=secret_var['admin_password'],
    email=secret_var['admin_email']
)
print("- Create worker Group")
Group.objects.create(name='worker')
print()
print('Setup Complete')
print('='*40)
