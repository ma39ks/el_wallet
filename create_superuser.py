import os
import django
from django.contrib.auth import get_user_model
from django.core.management import call_command


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wallet_project.settings")
django.setup()

def create_superuser():
    call_command("makemigrations")
    call_command("migrate")

    User = get_user_model()
    username = 'admin'
    email = 'admin@example.com'
    password = 'admin'

    try:
        user = User.objects.get(username=username)
        print(f"User '{username}' already exists.")
    except User.DoesNotExist:
        user = User.objects.create_superuser(username, email, password)
        print(f"Superuser '{username}' created successfully.")

if __name__ == "__main__":
    create_superuser()
