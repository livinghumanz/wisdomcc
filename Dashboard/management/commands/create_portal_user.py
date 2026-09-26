"""Create a client staff account for the admin portal.

    ./venv/bin/python manage.py create_portal_user priya --password 'secret'

The account gets `is_staff=False` and `is_superuser=False` deliberately: those
flags are what Django uses to allow entry to /admin/, and the client must not
reach the feature switches or the raw tables. Portal access comes from group
membership instead.
"""
from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand, CommandError

from Dashboard.auth_utils import PORTAL_GROUP


class Command(BaseCommand):
    help = 'Create or update a portal (client staff) account with no Django admin access.'

    def add_arguments(self, parser):
        parser.add_argument('username')
        parser.add_argument('--password', default='')
        parser.add_argument('--email', default='')
        parser.add_argument('--revoke', action='store_true',
                            help='Remove portal access from this account instead.')
        parser.add_argument('--demote', action='store_true',
                            help='Strip superuser/staff from an existing account and leave it '
                                 'with portal access only. Use on an account the client already '
                                 'has the password for.')

    def handle(self, *args, **options):
        username = options['username'].strip().lower()
        group, _ = Group.objects.get_or_create(name=PORTAL_GROUP)

        if not options['revoke'] and not options['demote'] and not options['password']:
            raise CommandError('--password is required when creating an account.')

        if options['revoke']:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise CommandError('No such user: %s' % username)
            user.groups.remove(group)
            self.stdout.write(self.style.WARNING('Portal access revoked for %s' % username))
            return

        if options['demote']:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise CommandError('No such user: %s' % username)
            created = False
            if options['password']:
                user.set_password(options['password'])
        else:
            user, created = User.objects.get_or_create(username=username,
                                                       defaults={'email': options['email']})
            user.set_password(options['password'])
        # Never grant these: they are what open /admin/ and the feature switches.
        user.is_staff = False
        user.is_superuser = False
        user.save()
        user.groups.add(group)

        self.stdout.write(self.style.SUCCESS(
            '%s portal user "%s"' % ('Created' if created else 'Updated', username)))
        self.stdout.write('  portal access : yes (group "%s")' % PORTAL_GROUP)
        self.stdout.write('  Django admin  : no  (is_staff=False)')
