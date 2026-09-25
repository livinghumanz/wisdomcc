"""Access control for the admin portal.

The portal holds student PII -- Aadhaar numbers, parent mobiles, addresses and
fee balances -- so every view is gated. The previous code called
`auth.authenticate()` and then never called `auth.login()`, never checked
`is_staff`, and left `/Dashboard/export/` open entirely (defects S7 and S4).
"""
from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def staff_required(view):
    """Allow only authenticated staff users. Anyone else is bounced to the home page."""

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            messages.info(request, 'Please log in to continue.')
            return redirect('/')
        if not user.is_staff:
            messages.info(request, 'That account does not have admin access.')
            return redirect('/')
        return view(request, *args, **kwargs)

    return wrapper


def student_required(view):
    """Allow only a logged-in student, identified by the regnum held in the session."""

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('student_regnum'):
            messages.info(request, 'Please log in to continue.')
            return redirect('/')
        return view(request, *args, **kwargs)

    return wrapper
