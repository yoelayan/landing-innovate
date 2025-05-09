import os
import sys
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser from environment variables'

    def handle(self, *args, **options):
        try:
            admin_username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
            admin_email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
            admin_password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

            if not (admin_username and admin_email and admin_password):
                self.stdout.write(self.style.WARNING(
                    'Skipping superuser creation. Environment variables '
                    'DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, and '
                    'DJANGO_SUPERUSER_PASSWORD must be set.'
                ))
                return

            if not User.objects.filter(username=admin_username).exists():
                self.stdout.write(self.style.NOTICE(f'Creating superuser {admin_username}'))
                User.objects.create_superuser(
                    username=admin_username,
                    email=admin_email,
                    password=admin_password
                )
                self.stdout.write(self.style.SUCCESS(f'Superuser {admin_username} created successfully'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Superuser {admin_username} already exists'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating superuser: {str(e)}'))
            # Don't fail the entire deployment if superuser creation fails
            self.stdout.write(self.style.WARNING('Continuing with deployment despite superuser creation error')) 