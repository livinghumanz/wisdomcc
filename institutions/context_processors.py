"""Make brand and branch data available to every template, including base.html.

This runs on *every* page, including the pre-existing coaching-centre pages, so a
database problem here would take down the whole site rather than one section.
It therefore degrades to empty values instead of raising -- the templates all
guard on these being falsy.
"""
import logging

from django.db import DatabaseError

from .models import Brand

logger = logging.getLogger(__name__)

WCC_SLUG = 'coaching-centre'
PRESCHOOL_SLUG = 'preschool'

GROUP_NAME = 'Wisdom Group of Institutions'

EMPTY = {
    'group_name': GROUP_NAME,
    'wcc_brand': None,
    'preschool_brand': None,
    'wcc_branches': [],
    'wcc_team': [],
}


def wisdom_group(request):
    try:
        brands = {
            b.slug: b
            for b in Brand.objects.filter(is_active=True).prefetch_related('branches', 'team')
        }
    except DatabaseError:
        # Most likely the institutions migrations have not been applied yet on
        # this environment. Serve the pages without brand data rather than 500.
        logger.warning('institutions tables unavailable; serving without brand data', exc_info=True)
        return dict(EMPTY)

    wcc = brands.get(WCC_SLUG)
    return {
        'group_name': GROUP_NAME,
        'wcc_brand': wcc,
        'preschool_brand': brands.get(PRESCHOOL_SLUG),
        'wcc_branches': wcc.branches.filter(is_active=True) if wcc else [],
        'wcc_team': wcc.team.filter(is_published=True) if wcc else [],
    }
