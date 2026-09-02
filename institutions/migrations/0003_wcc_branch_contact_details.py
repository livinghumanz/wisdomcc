"""Carry the Wisdom Coaching Centre addresses across from the old hardcoded footer.

The client's UI-001 brief gave social links for the two WCC branches but no
addresses, so these come from templates/base.html as it stood before the
redesign. The old footer's "Wisdom @ Redhills" address is on Gandhi Nagar west,
which is why it is mapped to the Gandhi Nagar branch.

Kamaraj Nagar has no address on record anywhere -- it stays blank until the
client supplies one. See docs/requests/UI-001-wisdom-group-london-kids.md.
"""
from django.db import migrations

UPDATES = {
    'Wisdom Coaching Centre — Gandhi Nagar': {
        'address': 'No 2/1825, Gandhi Nagar West, Redhills, Chennai 600052',
        'phone': '044-26323939, 9791148553',
    },
}


def fill_contacts(apps, schema_editor):
    Branch = apps.get_model('institutions', 'Branch')
    for name, fields in UPDATES.items():
        Branch.objects.filter(name=name).update(**fields)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [('institutions', '0002_seed_wisdom_group_content')]

    operations = [migrations.RunPython(fill_contacts, noop)]
