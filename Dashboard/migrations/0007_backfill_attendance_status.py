"""Backfill Attendance.status from the legacy `present` boolean.

Migration 0006 added `status` with default='present' and no data migration, so
every pre-existing row claimed the student was present regardless of what the
`present` flag actually said -- silently rewriting attendance history.

The legacy schema had no way to record "no class", so rows can only be mapped to
present or absent here. Anything genuinely a holiday must be re-marked by hand.
"""
from django.db import migrations


def backfill(apps, schema_editor):
    Attendance = apps.get_model('Dashboard', 'Attendance')
    Attendance.objects.filter(present=False).exclude(status='absent').update(status='absent')
    Attendance.objects.filter(present=True).exclude(status='present').update(status='present')


def unbackfill(apps, schema_editor):
    # `present` is derivable from `status`, so there is nothing to undo.
    pass


class Migration(migrations.Migration):

    dependencies = [('Dashboard', '0006_subject_alter_attendance_options_and_more')]

    operations = [migrations.RunPython(backfill, unbackfill)]
