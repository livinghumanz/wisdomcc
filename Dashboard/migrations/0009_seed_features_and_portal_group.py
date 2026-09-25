"""Create the portal group and the switchable features.

The group is what grants portal access. It deliberately carries no Django
permissions: portal users have `is_staff=False`, so /admin/ is closed to them
and the feature switches stay with the superuser.
"""
from django.db import migrations

PORTAL_GROUP = 'Portal Admin'

FEATURES = [
    ('students',  'Students',          'Student records, photos, add and edit.',              False, 1),
    ('marks',     'Marks',             'Internal and external mark entry per subject.',       True,  2),
    ('growth',    'Growth Card',       'Per-student bar chart of subject performance.',       True,  3),
    ('attendance','Attendance',        'Daily Present / Absent / No Class register.',         False, 4),
    ('fees',      'Fees',              'Fee sheet with balances and payment status.',         True,  5),
    ('faculty',   'Faculty Analysis',  'Results rolled up per faculty member.',               True,  6),
]


def seed(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Feature = apps.get_model('Dashboard', 'Feature')
    Group.objects.get_or_create(name=PORTAL_GROUP)
    for key, name, description, billable, order in FEATURES:
        Feature.objects.get_or_create(key=key, defaults={
            'name': name, 'description': description,
            'is_enabled': True, 'show_when_disabled': billable,
            'is_billable': billable, 'order': order,
        })


def unseed(apps, schema_editor):
    apps.get_model('Dashboard', 'Feature').objects.filter(
        key__in=[f[0] for f in FEATURES]).delete()
    apps.get_model('auth', 'Group').objects.filter(name=PORTAL_GROUP).delete()


class Migration(migrations.Migration):

    dependencies = [('Dashboard', '0008_feature'), ('auth', '0012_alter_user_first_name_max_length')]

    operations = [migrations.RunPython(seed, unseed)]
