"""Daily attendance register (spec page 3).

One row per *active* student for a chosen date, with three mutually exclusive
states -- Present / Absent / No Class (Holiday) -- and footer totals.

Two notes on the data model, because they shape this module:

1. `Attendance` has `unique_together = ('studentid', 'edate')`, so a save is an
   upsert (`update_or_create`) rather than an insert. The register is therefore
   editable: re-opening a date shows what was recorded and lets it be corrected.
2. `Attendance.present` is a legacy boolean that the student-facing dashboard
   still reads. `Attendance.save()` derives it from `status`, but since Django
   4.2 `update_or_create()` passes `update_fields` to `save()` on the update
   branch -- and a field that `save()` assigns but that is not in
   `update_fields` is silently not written. So `present` is passed explicitly
   in `defaults` below to keep it inside `update_fields`. `save()` still has
   the last word on its value; naming it here only guarantees it is persisted.
"""
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.utils.http import urlencode

from ..auth_utils import feature_required, portal_required
from ..choices import ATTENDANCE_STATUS_CHOICES, BRANCH_CHOICES, STD_CHOICES
from ..models import Attendance, Student

ACTIVE = 'active'
VALID_STATUSES = {value for value, _label in ATTENDANCE_STATUS_CHOICES}


def _selected_date(raw):
    """The date being registered: the `date` parameter, else today."""
    if raw:
        try:
            parsed = parse_date(raw.strip())
        except ValueError:      # well-formed but impossible, e.g. 2026-02-31
            parsed = None
        if parsed:
            return parsed
    return timezone.localdate()


def _filters(data):
    branch = (data.get('branch') or '').strip()
    std = (data.get('std') or '').strip()
    # Ignore anything that is not an offered option, so a hand-edited query
    # string cannot quietly empty the register.
    if branch not in {value for value, _ in BRANCH_CHOICES}:
        branch = ''
    if std not in {value for value, _ in STD_CHOICES}:
        std = ''
    return branch, std


def _student_qs(branch, std, active=True):
    qs = Student.objects.filter(active_status=ACTIVE) if active \
        else Student.objects.exclude(active_status=ACTIVE)
    if branch:
        qs = qs.filter(branch=branch)
    if std:
        qs = qs.filter(std=std)
    return qs.order_by('name', 'regnum')


def _register_url(edate, branch, std):
    params = {'date': edate.isoformat()}
    if branch:
        params['branch'] = branch
    if std:
        params['std'] = std
    return '{0}?{1}'.format(reverse('admin-attendance'), urlencode(params))


@portal_required
@feature_required('attendance')
def attendance_register(request):
    if request.method == 'POST':
        return _save_register(request)

    edate = _selected_date(request.GET.get('date'))
    branch, std = _filters(request.GET)

    students = list(_student_qs(branch, std))
    recorded = dict(
        Attendance.objects
        .filter(edate=edate, studentid__in=students)
        .values_list('studentid_id', 'status')
    )

    totals = {'present': 0, 'absent': 0, 'no_class': 0, 'unmarked': 0}
    rows = []
    for number, student in enumerate(students, start=1):
        status = recorded.get(student.regnum)
        totals[status if status in totals else 'unmarked'] += 1
        rows.append({
            'sl': number,
            'student': student,
            'status': status,
            # Pre-built so the template stays a plain loop over three radios.
            'options': [
                {'value': value, 'label': label, 'checked': status == value}
                for value, label in ATTENDANCE_STATUS_CHOICES
            ],
        })

    return render(request, 'dashboard/admin/attendance.html', {
        'active': 'attendance',
        'edate': edate,
        'date_value': edate.isoformat(),
        'today_value': timezone.localdate().isoformat(),
        'branch': branch,
        'std': std,
        'branch_choices': BRANCH_CHOICES,
        'std_choices': STD_CHOICES,
        'status_choices': ATTENDANCE_STATUS_CHOICES,
        'rows': rows,
        'totals': totals,
        'active_count': len(rows),
        'excluded_count': _student_qs(branch, std, active=False).count(),
    })


def _save_register(request):
    """Upsert one Attendance row per marked student, then POST-redirect-GET."""
    edate = _selected_date(request.POST.get('date'))
    branch, std = _filters(request.POST)
    students = _student_qs(branch, std)

    saved = 0
    with transaction.atomic():
        for student in students:
            status = (request.POST.get('status_{0}'.format(student.regnum)) or '').strip()
            if status not in VALID_STATUSES:
                # Nothing chosen for this student: leave the date unrecorded
                # for them rather than inventing an attendance state.
                continue
            Attendance.objects.update_or_create(
                studentid=student,
                edate=edate,
                # `present` is listed so it survives update_or_create's
                # update_fields; see the module docstring.
                defaults={'status': status, 'present': status == 'present'},
            )
            saved += 1

    if saved:
        messages.success(request, 'Attendance saved for {0} student{1} on {2}.'.format(
            saved, '' if saved == 1 else 's', edate.strftime('%d %b %Y')))
    else:
        messages.info(request, 'Nothing was marked, so no attendance was saved for {0}.'.format(
            edate.strftime('%d %b %Y')))

    return redirect(_register_url(edate, branch, std))
