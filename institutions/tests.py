from django.test import TestCase
from django.urls import reverse

from .models import Brand, BrandSection, Branch, Program


class PreschoolHomeTests(TestCase):
    def setUp(self):
        # The 0002 data migration seeds a brand on this slug; replace it so these
        # tests assert against their own fixture rather than the seeded copy.
        Brand.objects.filter(slug='preschool').delete()
        self.brand = Brand.objects.create(
            slug='preschool', name='Test Play School', short_name='Test Kids',
            tagline='Grow and shine', intro='Hello.\n\nSecond para.',
        )

    def test_home_renders_brand_content(self):
        Program.objects.create(brand=self.brand, name='Play Group', age_range='2-3 Years',
                               focus_areas='Sensory play\nMusic and movement')
        BrandSection.objects.create(brand=self.brand, key='facilities', title='Facilities',
                                    bullets='Activity room\nOutdoor play zone')
        Branch.objects.create(brand=self.brand, name='Redhills', phone='9791148553')

        response = self.client.get(reverse('preschool-home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Play School')
        self.assertContains(response, 'Play Group')
        self.assertContains(response, 'Sensory play')
        self.assertContains(response, 'Activity room')
        self.assertContains(response, '9791148553')

    def test_inactive_brand_is_404(self):
        self.brand.is_active = False
        self.brand.save()
        self.assertEqual(self.client.get(reverse('preschool-home')).status_code, 404)

    def test_unpublished_section_is_hidden(self):
        BrandSection.objects.create(brand=self.brand, key='draft', title='Draft Section',
                                    bullets='Secret', is_published=False)
        self.assertNotContains(self.client.get(reverse('preschool-home')), 'Draft Section')

    def test_blank_lines_are_not_bullets(self):
        section = BrandSection.objects.create(brand=self.brand, key='f', title='F',
                                              bullets='One\n\n  \nTwo\n')
        self.assertEqual(section.bullet_list, ['One', 'Two'])
