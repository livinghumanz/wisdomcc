from django.shortcuts import get_object_or_404, render

from .models import Brand

PRESCHOOL_SLUG = 'preschool'


def preschool_home(request):
    """Public home page for the play school brand under the Wisdom Group umbrella."""
    brand = get_object_or_404(
        Brand.objects.prefetch_related('programs', 'sections', 'branches'),
        slug=PRESCHOOL_SLUG,
        is_active=True,
    )
    context = {
        'brand': brand,
        'programs': brand.programs.all(),
        'sections': brand.sections.filter(is_published=True),
        'branches': brand.branches.filter(is_active=True),
    }
    return render(request, 'institutions/preschool_home.html', context)
