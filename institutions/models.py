"""Content models for the Wisdom Group of Institutions.

Everything the client asked to be able to change twice a month (requirement R1)
lives here rather than in a template, so it is editable from Django admin without
a deploy. See docs/requests/UI-001-wisdom-group-london-kids.md.
"""
from django.db import models


def as_lines(text):
    """Split an admin-entered block into a list, one item per non-empty line."""
    return [line.strip() for line in (text or '').splitlines() if line.strip()]


class Brand(models.Model):
    """One institution under the Wisdom Group umbrella.

    The public-facing name is a field, not hardcoded copy, because it is still
    unsettled ("London Kids" vs "Wisdom Kids") -- see open question 1 in the brief.
    """

    slug = models.SlugField(unique=True, help_text='Used in URLs. Changing this changes the page address.')
    name = models.CharField(max_length=120, help_text='Full public name, e.g. "London Kids International Play School".')
    short_name = models.CharField(max_length=60, help_text='Used in the navbar and page titles, e.g. "London Kids".')
    descriptor = models.CharField(max_length=150, blank=True, help_text='e.g. "A Unit of Wisdom Group of Institutions".')
    tagline = models.CharField(max_length=200, blank=True)
    welcome_heading = models.CharField(max_length=200, blank=True)
    intro = models.TextField(blank=True, help_text='Hero paragraph(s). Blank line separates paragraphs.')
    about = models.TextField(blank=True, help_text='"About Us" body. Blank line separates paragraphs.')
    vision = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    admissions_note = models.TextField(blank=True, help_text='Shown in the admissions call-to-action.')
    logo = models.ImageField(upload_to='brand/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    @property
    def intro_paragraphs(self):
        return [p.strip() for p in self.intro.split('\n\n') if p.strip()]

    @property
    def about_paragraphs(self):
        return [p.strip() for p in self.about.split('\n\n') if p.strip()]


class Program(models.Model):
    """A course or programme offered by a brand (Play Group, NEET, Abacus, ...)."""

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='programs')
    name = models.CharField(max_length=120)
    age_range = models.CharField(max_length=60, blank=True, help_text='e.g. "2-3 Years". Leave blank if not age-based.')
    intro = models.TextField(blank=True)
    focus_areas = models.TextField(blank=True, help_text='One focus area per line.')
    image = models.ImageField(upload_to='programs/', blank=True, null=True)
    admissions_open = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return '{0} - {1}'.format(self.brand.short_name, self.name)

    @property
    def focus_list(self):
        return as_lines(self.focus_areas)


class BrandSection(models.Model):
    """A titled block of bullets on a brand page.

    Generic on purpose: "Why Choose Us", "Our Learning Approach", "Facilities" and
    "Our Speech Curriculum" are all the same shape, and the client can add more
    without anyone touching a template.
    """

    LAYOUT_CHOICES = [
        ('pills', 'Pills - short items, wrapped chips'),
        ('cards', 'Cards - one card per item'),
        ('feature', 'Feature - highlighted panel with intro'),
    ]

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='sections')
    key = models.SlugField(help_text='Anchor id used in the page URL, e.g. "facilities".')
    title = models.CharField(max_length=150)
    nav_label = models.CharField(
        max_length=30, blank=True,
        help_text='Short label for the top menu, e.g. "Why Us". Leave blank to keep this '
                  'section out of the menu -- full section titles are too long for a navbar.',
    )
    intro = models.TextField(blank=True)
    bullets = models.TextField(blank=True, help_text='One item per line.')
    outro = models.TextField(blank=True)
    layout = models.CharField(max_length=10, choices=LAYOUT_CHOICES, default='pills')
    is_published = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']
        unique_together = [('brand', 'key')]

    def __str__(self):
        return '{0} - {1}'.format(self.brand.short_name, self.title)

    @property
    def bullet_list(self):
        return as_lines(self.bullets)


class Branch(models.Model):
    """A physical location, with its own contact details and social handles.

    Replaces the hardcoded "redhills"/"kanathur" strings scattered through the
    old templates (requirement R3).
    """

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=120, help_text='e.g. "Wisdom Coaching Centre - Gandhi Nagar".')
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=60, blank=True, help_text='Comma-separate multiple numbers.')
    email = models.EmailField(blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, help_text='Digits only, with country code if known.')
    maps_url = models.URLField(blank=True, max_length=300)
    facebook_url = models.URLField(blank=True, max_length=300)
    instagram_url = models.URLField(blank=True, max_length=300)
    youtube_url = models.URLField(blank=True, max_length=300)
    whatsapp_channel_url = models.URLField(blank=True, max_length=300)
    payment_qr = models.ImageField(upload_to='branch/qr/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'branches'

    def __str__(self):
        return self.name

    @property
    def phone_list(self):
        return [p.strip() for p in self.phone.split(',') if p.strip()]

    @property
    def whatsapp_link(self):
        return 'https://wa.me/{0}'.format(self.whatsapp_number) if self.whatsapp_number else ''


class TeamMember(models.Model):
    """A management or faculty profile shown on a brand's About page.

    Who appears here changes often, so it is data rather than template markup.

    Photos: `photo` is for admin uploads, but uploaded media does not serve in
    production yet (deferred defect F2), so `photo_static` lets a profile point at
    a file already shipped in static/. Drop `photo_static` once F2 is fixed.
    """

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='team')
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    photo_static = models.CharField(
        max_length=200, blank=True,
        help_text='Path under static/, e.g. "img/About_us/ebi.jpg". Used when no photo is uploaded.',
    )
    is_published = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return '{0} - {1}'.format(self.name, self.role or 'team')
