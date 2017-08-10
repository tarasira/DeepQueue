import os
import json
from pprint import pprint
from collections import defaultdict
from django.contrib.auth.models import User, Group

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
    pprint(secret_var)
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
print('Setup Complete')
