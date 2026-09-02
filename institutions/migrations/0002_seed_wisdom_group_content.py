"""Seed the content the client supplied on 2026-09-02.

Source: docs/requests/UI-001-wisdom-group-london-kids.md

This is a starting point for the admin, not fixed copy -- everything here is
editable at /admin/ without a deploy. Re-running the migration will not
overwrite edits (get_or_create on the natural key).
"""
from django.db import migrations

YOUTUBE = 'https://youtube.com/@wisdomcoachingcentre7947'

PRESCHOOL = {
    'slug': 'preschool',
    'name': 'London Kids International Play School',
    'short_name': 'London Kids',
    'descriptor': 'A Unit of Wisdom Group of Institutions',
    'tagline': 'Where Little Minds Grow, Explore, and Shine.',
    'welcome_heading': 'Welcome to London Kids International Play School',
    'order': 2,
    'intro': (
        'At London Kids International Play School, we believe every child deserves a joyful '
        'beginning to their learning journey. As a proud member of the Wisdom Group of '
        'Institutions, we provide a safe, caring, and stimulating environment where children '
        'learn through play, exploration, and meaningful experiences.\n\n'
        'Our child-centered approach helps build confidence, creativity, communication skills, '
        'and a lifelong love for learning.'
    ),
    'about': (
        'London Kids International Play School is dedicated to providing quality early childhood '
        'education that nurtures every child’s intellectual, emotional, social, and physical '
        'development.\n\n'
        'Our experienced educators create engaging learning experiences using interactive '
        'activities, storytelling, music, art, games, and hands-on exploration. We focus on '
        'developing strong foundations that prepare children for future academic success.'
    ),
    'vision': (
        'To inspire young minds through quality early childhood education while nurturing '
        'confident, compassionate, and lifelong learners.'
    ),
    'mission': (
        'To provide a joyful, safe, and stimulating environment where every child develops '
        'academically, socially, emotionally, and creatively through innovative teaching '
        'methods and personalized care.'
    ),
    'admissions_note': (
        'Give your child the perfect start with an education that builds confidence, creativity, '
        'communication, and character.\n\n'
        'Enroll today and become a part of the London Kids International Play School family.'
    ),
}

WCC = {
    'slug': 'coaching-centre',
    'name': 'Wisdom Coaching Centre',
    'short_name': 'Wisdom Coaching Centre',
    'descriptor': 'A Unit of Wisdom Group of Institutions',
    'order': 1,
    'intro': '',
    'about': '',
}

PROGRAMS = [
    ('Play Group', '2–3 Years',
     'Our Play Group program introduces children to a fun and welcoming learning environment. '
     'Activities focus on:',
     'Social interaction\nSensory play\nFine and gross motor skills\nLanguage development\n'
     'Music and movement\nCreative activities'),
    ('Nursery', '3–4 Years',
     'The Nursery program encourages curiosity and early learning through engaging activities '
     'that develop:',
     'Early literacy\nNumber concepts\nVocabulary building\nCreative thinking\nSocial skills\n'
     'Independence'),
    ('Junior KG (LKG)', '4–5 Years',
     'Our Junior KG curriculum prepares children with strong foundational skills through:',
     'Reading readiness\nWriting practice\nBasic mathematics\nGeneral awareness\n'
     'Art and creativity\nCommunication skills'),
    ('Senior KG (UKG)', '5–6 Years',
     'Senior KG prepares children for primary school by strengthening:',
     'Reading and writing\nMathematics\nScience concepts\nLogical thinking\nProblem-solving\n'
     'Leadership and confidence'),
]

SECTIONS = [
    ('speech-curriculum', 'Our Speech Curriculum', 'feature',
     'One of the highlights of our educational program is our specially designed Speech '
     'Curriculum, which helps children become confident communicators from an early age.',
     'Daily conversation practice\nVocabulary enrichment\nStorytelling\nRhymes and songs\n'
     'Public speaking activities\nShow and Tell\nRole play\nPhonics-based pronunciation\n'
     'Listening skills\nConfidence-building exercises',
     'Our goal is to help every child communicate clearly, confidently, and effectively.'),
    ('why-choose', 'Why Choose London Kids?', 'pills', '',
     'Safe and child-friendly campus\nExperienced and caring teachers\n'
     'Play-based learning approach\nSmart classrooms\nActivity-based curriculum\n'
     'Speech Development Program\nIndividual attention\nCreative learning environment\n'
     'Regular parent interaction\nCelebration of festivals and special days\n'
     'Indoor and outdoor activities\nFocus on holistic child development', ''),
    ('learning-approach', 'Our Learning Approach', 'cards',
     'We believe children learn best when they are happy, engaged, and encouraged to explore.',
     'Learning through play\nActivity-based education\nHands-on experiences\n'
     'Interactive storytelling\nMusic and movement\nCreative arts and crafts\n'
     'Practical life activities\nExperiential learning', ''),
    ('facilities', 'Facilities', 'pills', '',
     'Bright and colorful classrooms\nSafe indoor play area\nOutdoor play zone\n'
     'Learning resource center\nCCTV surveillance\nHygienic campus\nChild-friendly furniture\n'
     'Activity room\nCelebration area\nParent interaction sessions', ''),
]

BRANCHES = [
    ('preschool', {
        'name': 'London Kids International Play School — Redhills',
        'address': 'Vetrivel Street, Kamarajar Nagar, Redhills, Chennai 600052',
        'phone': '9791148553',
        'email': 'info.londonkidsredhills@gmail.com',
        'whatsapp_number': '919791148553',
        'maps_url': 'https://maps.app.goo.gl/Y6XWJrQBJrTf9UxF9',
        'facebook_url': 'https://www.facebook.com/share/1ELhBVdH7B/',
        'instagram_url': 'https://www.instagram.com/londonkidsredhills',
        'youtube_url': YOUTUBE,
        'whatsapp_channel_url': 'https://whatsapp.com/channel/0029VaULsccLSmbbiZnrTR15',
        'order': 1,
    }),
    ('coaching-centre', {
        'name': 'Wisdom Coaching Centre — Gandhi Nagar',
        'phone': '9791148553',
        'whatsapp_number': '919791148553',
        'maps_url': 'https://maps.app.goo.gl/WQfgRTnc82DhU7uG8',
        'facebook_url': 'https://www.facebook.com/wisdomcoachingcentre20/',
        'instagram_url': 'https://www.instagram.com/wisdom_coaching_centre20/',
        'youtube_url': YOUTUBE,
        'order': 1,
    }),
    ('coaching-centre', {
        'name': 'Wisdom Coaching Centre — Kamaraj Nagar',
        'phone': '9791148553',
        'whatsapp_number': '919791148553',
        'maps_url': 'https://maps.app.goo.gl/QBc5XRexhtTXc3xX6',
        'facebook_url': 'https://www.facebook.com/profile.php?id=100091439325900',
        'instagram_url': 'https://www.instagram.com/wisdomcoachingcentre_redhills/',
        'youtube_url': YOUTUBE,
        'order': 2,
    }),
]


def seed(apps, schema_editor):
    Brand = apps.get_model('institutions', 'Brand')
    Program = apps.get_model('institutions', 'Program')
    BrandSection = apps.get_model('institutions', 'BrandSection')
    Branch = apps.get_model('institutions', 'Branch')

    for payload in (WCC, PRESCHOOL):
        data = dict(payload)
        Brand.objects.get_or_create(slug=data.pop('slug'), defaults=data)

    preschool = Brand.objects.get(slug='preschool')

    for order, (name, age_range, intro, focus) in enumerate(PROGRAMS, start=1):
        Program.objects.get_or_create(
            brand=preschool, name=name,
            defaults={'age_range': age_range, 'intro': intro,
                      'focus_areas': focus, 'order': order},
        )

    for order, (key, title, layout, intro, bullets, outro) in enumerate(SECTIONS, start=1):
        BrandSection.objects.get_or_create(
            brand=preschool, key=key,
            defaults={'title': title, 'layout': layout, 'intro': intro,
                      'bullets': bullets, 'outro': outro, 'order': order},
        )

    for brand_slug, data in BRANCHES:
        brand = Brand.objects.get(slug=brand_slug)
        Branch.objects.get_or_create(brand=brand, name=data['name'], defaults=data)


def unseed(apps, schema_editor):
    Brand = apps.get_model('institutions', 'Brand')
    Brand.objects.filter(slug__in=['preschool', 'coaching-centre']).delete()


class Migration(migrations.Migration):

    dependencies = [('institutions', '0001_initial')]

    operations = [migrations.RunPython(seed, unseed)]
