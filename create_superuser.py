import os
import django
from django.contrib.auth import get_user_model


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj_zum.settings')
django.setup(set_prefix=False)

User = get_user_model()
if User.objects.all().count() == 0:
    superuser = User.objects.create_superuser(
        username='admin',
        password='admin',
    )
    print(f'Success crated user:')
    print(f'username: {superuser.username}')
    print(f'password: admin')
#
