from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

class Command(BaseCommand):
    help = 'Create a superuser with username admin and password admin'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(username=settings.SUPERUSER_USERNAME).exists():
            User.objects.create_superuser(
                username=settings.SUPERUSER_USERNAME,
                email=settings.SUPERUSER_EMAIL,
                password=settings.SUPERUSER_PASSWORD
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists.'))
