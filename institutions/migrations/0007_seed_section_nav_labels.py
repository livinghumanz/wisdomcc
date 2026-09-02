"""Give the seeded preschool sections short menu labels.

Full section titles ("Why Choose London Kids?", "Our Learning Approach") wrapped
onto three lines in the navbar. These are the short forms shown in the menu.
"""
from django.db import migrations

LABELS = {
    'speech-curriculum': 'Speech',
    'why-choose': 'Why Us',
    'learning-approach': 'Approach',
    'facilities': 'Facilities',
}


def set_labels(apps, schema_editor):
    BrandSection = apps.get_model('institutions', 'BrandSection')
    for key, label in LABELS.items():
        BrandSection.objects.filter(key=key, nav_label='').update(nav_label=label)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [('institutions', '0006_brandsection_nav_label')]

    operations = [migrations.RunPython(set_labels, noop)]
