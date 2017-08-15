def is_superuser(user):
    return user.is_superuser
def is_worker(user):
    return user.groups.filter(name__in=['worker']).exists()
def is_student(user):
    return user.groups.filter(name__in=['student']).exists()
