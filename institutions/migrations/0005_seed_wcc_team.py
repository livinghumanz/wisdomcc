"""Seed the Wisdom Coaching Centre management profiles.

Per the client (2026-09-02): only Ebinezer and Dency are to be listed. The other
four profiles that were hardcoded in templates/home/Wabout.html -- Aaron
Thanasingh, Jansi D Aaron, G. J. Bain and Dr. A. Rosy -- are intentionally not
seeded. Bios are carried across from that template.
"""
from django.db import migrations

MEMBERS = [
    {
        'name': 'Prof. D. Ebinezer',
        'role': 'Founder — Wisdom Coaching Centre',
        'photo_static': 'img/About_us/ebi.jpg',
        'order': 1,
        'bio': (
            'With over 5 years of experience in academics as a teacher and language trainer, '
            'Ebinezer believes in practical and activity based classes. He holds a Master of '
            'Philosophy from University of Madras and a Master of English from one of the '
            'esteemed colleges in Madras, Pachaiyappa’s College for Men.'
        ),
    },
    {
        'name': 'Mrs. C. Dency Ebinezer',
        'role': 'Director — Wisdom Coaching Centre',
        'photo_static': 'img/About_us/dency.jpg',
        'order': 2,
        'bio': (
            'Dency holds a Master’s Degree in Computer Science and is also a Montessori '
            'Diplomat. She is a Kindergarten expert who trains children in an activity based '
            'classroom at the Redhills wing. In addition, she tracks and manages students’ '
            'academic performance and ensures a healthy relationship with parents regarding '
            'their ward’s progress.'
        ),
    },
]


def seed(apps, schema_editor):
    Brand = apps.get_model('institutions', 'Brand')
    TeamMember = apps.get_model('institutions', 'TeamMember')
    try:
        wcc = Brand.objects.get(slug='coaching-centre')
    except Brand.DoesNotExist:
        return
    for member in MEMBERS:
        data = dict(member)
        TeamMember.objects.get_or_create(brand=wcc, name=data.pop('name'), defaults=data)


def unseed(apps, schema_editor):
    TeamMember = apps.get_model('institutions', 'TeamMember')
    TeamMember.objects.filter(name__in=[m['name'] for m in MEMBERS]).delete()


class Migration(migrations.Migration):

    dependencies = [('institutions', '0004_teammember')]

    operations = [migrations.RunPython(seed, unseed)]
