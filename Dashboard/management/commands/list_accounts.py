"""Show who has which tier of access.

    ./venv/bin/python manage.py list_accounts
"""
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from Dashboard.auth_utils import PORTAL_GROUP


class Command(BaseCommand):
    help = 'List every account and the access it holds.'

    def handle(self, *args, **options):
        rows = []
        for u in User.objects.order_by('username'):
            in_portal = u.groups.filter(name=PORTAL_GROUP).exists()
            if u.is_superuser:
                tier = 'OWNER  (portal + django admin + feature switches)'
            elif in_portal:
                tier = 'client (portal only)'
            elif u.is_staff:
                tier = 'STAFF WITHOUT PORTAL GROUP -- can reach /admin/, review this'
            else:
                tier = 'no access'
            rows.append((u.username, u.is_staff, u.is_superuser, in_portal, u.last_login, tier))

        self.stdout.write('%-18s %-8s %-10s %-8s %s' % ('USERNAME', 'STAFF', 'SUPERUSER', 'PORTAL', 'TIER'))
        for username, staff, superuser, portal, last, tier in rows:
            self.stdout.write('%-18s %-8s %-10s %-8s %s' % (username, staff, superuser, portal, tier))

        owners = [r[0] for r in rows if r[2]]
        self.stdout.write('')
        self.stdout.write('Owners: %s' % (', '.join(owners) or 'NONE'))
        if len(owners) > 1:
            self.stdout.write(self.style.WARNING(
                'More than one account has full access. Anyone listed above can change '
                'feature switches and read every record.'))
