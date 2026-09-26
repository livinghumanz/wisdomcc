"""Create or reset the owner account -- full access to everything.

    ./venv/bin/python manage.py create_owner ramesh --password '<password>'

The owner is a Django superuser, so they get the admin portal, Django admin and
the feature switches. Keep this password to yourself: anyone holding it can turn
features on, read every table and change any account.
"""
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create or reset the owner (full-access superuser) account.'

    def add_arguments(self, parser):
        parser.add_argument('username')
        parser.add_argument('--password', required=True)
        parser.add_argument('--email', default='')

    def handle(self, *args, **options):
        username = options['username'].strip().lower()
        user, created = User.objects.get_or_create(
            username=username, defaults={'email': options['email']})
        user.set_password(options['password'])
        user.is_staff = True
        user.is_superuser = True
        if options['email']:
            user.email = options['email']
        user.save()
        self.stdout.write(self.style.SUCCESS(
            '%s owner account "%s"' % ('Created' if created else 'Reset', username)))
        self.stdout.write('  admin portal    : yes')
        self.stdout.write('  Django admin    : yes')
        self.stdout.write('  feature switches: yes')
