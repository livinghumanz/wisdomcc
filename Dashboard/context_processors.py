"""Expose the feature switches and the viewer's tier to every portal template."""
import logging

from django.db import DatabaseError

from .auth_utils import PORTAL_GROUP, can_use_portal

logger = logging.getLogger(__name__)


def portal(request):
    user = getattr(request, 'user', None)
    if user is None or not can_use_portal(user):
        return {}

    from .models import Feature
    try:
        features = {f.key: f for f in Feature.objects.all()}
    except DatabaseError:
        logger.warning('feature table unavailable', exc_info=True)
        features = {}

    is_owner = user.is_superuser

    def visible(key):
        """Show it when on, when the owner is looking, or when it is a locked teaser."""
        f = features.get(key)
        if f is None:
            return True
        return f.is_enabled or is_owner or f.show_when_disabled

    def locked(key):
        f = features.get(key)
        return bool(f and not f.is_enabled)

    keys = ['students', 'marks', 'growth', 'attendance', 'fees', 'faculty']
    return {
        'portal_is_owner': is_owner,
        'portal_group': PORTAL_GROUP,
        'feature_visible': {k: visible(k) for k in keys},
        'feature_locked': {k: locked(k) for k in keys},
        'features': features,
    }
