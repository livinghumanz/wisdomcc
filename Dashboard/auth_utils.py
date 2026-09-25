"""Access control for the admin portal.

Two separate tiers, deliberately not the same thing:

* **Superuser** -- the owner. Reaches Django admin at /admin/, and is the only
  one who can switch features on and off.
* **Portal user** -- the client's staff. Reaches the admin portal only. These
  accounts are created with ``is_staff=False`` on purpose: ``is_staff`` is
  precisely what Django uses to allow entry to /admin/, so granting it would
  hand the client the feature switches and every raw table.

Portal access is therefore keyed on membership of the PORTAL_GROUP group, never
on ``is_staff``.
"""
import logging
from functools import wraps

from django.contrib import messages
from django.db import DatabaseError
from django.shortcuts import redirect, render

logger = logging.getLogger(__name__)

PORTAL_GROUP = 'Portal Admin'


def can_use_portal(user):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name=PORTAL_GROUP).exists()


def feature_is_enabled(key):
    """True unless a Feature row exists and says otherwise.

    Defaults to enabled so a missing row can never lock the client out of a
    screen that was working.
    """
    from .models import Feature
    try:
        feature = Feature.objects.filter(key=key).first()
    except DatabaseError:
        logger.warning('feature table unavailable; allowing %s', key, exc_info=True)
        return True
    return True if feature is None else feature.is_enabled


def portal_required(view):
    """Allow the superuser, or a member of the portal group. Nobody else."""

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, 'Please log in to continue.')
            return redirect('/')
        if not can_use_portal(request.user):
            messages.info(request, 'That account does not have admin access.')
            return redirect('/')
        return view(request, *args, **kwargs)

    return wrapper


def feature_required(key):
    """Block a screen whose feature is switched off.

    Applied under `portal_required`, so the caller is already known to be staff.
    The superuser is exempt: the owner must be able to check a feature before
    enabling it for the client.
    """

    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser or feature_is_enabled(key):
                return view(request, *args, **kwargs)
            from .models import Feature
            feature = Feature.objects.filter(key=key).first()
            return render(request, 'dashboard/admin/feature_off.html',
                          {'active': key, 'feature_key': key,
                           'feature_name': feature.name if feature else None}, status=403)
        return wrapper

    return decorator


# Kept so older imports do not break; portal access is no longer is_staff-based.
staff_required = portal_required


def student_required(view):
    """Allow only a logged-in student, identified by the regnum held in the session."""

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('student_regnum'):
            messages.info(request, 'Please log in to continue.')
            return redirect('/')
        return view(request, *args, **kwargs)

    return wrapper
