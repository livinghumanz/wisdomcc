"""Fee sheet (spec page 3, "Fee Update") and faculty result analysis (spec page 2).

Both screens are read-mostly rollups over models owned elsewhere; nothing here
creates schema. Money is handled as `Decimal` end to end -- never float -- and the
derived columns (balances, total due, status) are computed from `FeeRecord`'s own
properties so the browser preview and the saved truth cannot drift apart.
"""
from datetime import date, datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import urlencode

from ..auth_utils import staff_required
from ..choices import BRANCH_CHOICES, EXAM_TYPE_CHOICES, STD_CHOICES
from ..models import FeeRecord, MarkEntry, Student, Subject

TWOPLACES = Decimal('0.01')
ZERO = Decimal('0.00')

# `FeeRecord` money columns the admin may type into. Everything else on the sheet
# is derived and therefore never rendered as an input.
MONEY_FIELDS = (
    'fee_amount',
    'paid_amount',
    'admission_amount',
    'admission_paid',
    'jersey_amount',
    'material_amount',
)

# FeeRecord money columns are max_digits=10, decimal_places=2.
MONEY_CEILING = Decimal('99999999.99')


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def money(value):
    """Round a Decimal to two places, half-up, the way an invoice would."""
    return (value or ZERO).quantize(TWOPLACES, rounding=ROUND_HALF_UP)


def fmt(value):
    """Plain, un-localised 2dp text: safe inside a number input's value."""
    return '{0:.2f}'.format(money(value))


def parse_money(raw):
    """Parse one posted amount. Returns `None` when the text is not usable."""
    if raw is None:
        return None
    raw = raw.strip().replace(',', '').replace('₹', '')
    if raw == '':
        return ZERO
    try:
        value = Decimal(raw)
    except (InvalidOperation, ValueError):
        return None
    if not value.is_finite():
        return None
    value = money(value)
    if value < ZERO or value > MONEY_CEILING:
        return None
    return value


def current_academic_year(today=None):
    """June-to-May academic year, rendered the way the spec writes it: 2026-27."""
    today = today or date.today()
    start = today.year if today.month >= 6 else today.year - 1
    return '{0}-{1:02d}'.format(start, (start + 1) % 100)


def academic_year_options(selected):
    """The current year, two either side, plus whatever the data already holds."""
    base = int(current_academic_year().split('-')[0])
    years = {'{0}-{1:02d}'.format(y, (y + 1) % 100) for y in range(base - 2, base + 3)}
    years.update(FeeRecord.objects.values_list('academic_year', flat=True).distinct())
    if selected:
        years.add(selected)
    return sorted(years, reverse=True)


def _filters_from(source):
    """The filter state, read from either GET or the POSTed hidden inputs."""
    year = (source.get('academic_year') or '').strip() or current_academic_year()
    return {
        'academic_year': year[:9],
        'branch': (source.get('branch') or '').strip(),
        'std': (source.get('std') or '').strip(),
        'status': (source.get('status') or 'all').strip(),
    }


def _active_students(filters):
    qs = Student.objects.filter(active_status='active')
    if filters['branch']:
        qs = qs.filter(branch=filters['branch'])
    if filters['std']:
        qs = qs.filter(std=filters['std'])
    return qs.order_by('name', 'regnum')


# ---------------------------------------------------------------------------
# Screen 1 -- fee sheet
# ---------------------------------------------------------------------------

@staff_required
def fee_sheet(request):
    if request.method == 'POST':
        return _save_fee_sheet(request)

    filters = _filters_from(request.GET)
    students = list(_active_students(filters))
    records = {
        r.student_id: r
        for r in FeeRecord.objects.filter(
            academic_year=filters['academic_year'],
            student__in=students,
        )
    }

    rows = []
    total_billed = total_collected = total_outstanding = ZERO
    unpaid_count = 0

    for student in students:
        record = records.get(student.regnum)
        # A student with no record for this year still belongs on the sheet, at
        # zero, so the admin can see who has not been set up yet.
        preview = record or FeeRecord(student=student, academic_year=filters['academic_year'])

        fee_balance = money(preview.fee_balance)
        admission_balance = money(preview.admission_balance)
        total_due = money(preview.total_due)
        settled = preview.is_settled

        billed = money(
            preview.fee_amount + preview.admission_amount
            + preview.jersey_amount + preview.material_amount
        )
        collected = money(preview.paid_amount + preview.admission_paid)

        total_billed += billed
        total_collected += collected
        if total_due > ZERO:
            total_outstanding += total_due
        if not settled:
            unpaid_count += 1

        if filters['status'] == 'paid' and not settled:
            continue
        if filters['status'] == 'unpaid' and settled:
            continue

        rows.append({
            'student': student,
            'has_record': record is not None,
            'values': {f: fmt(getattr(preview, f)) for f in MONEY_FIELDS},
            'fee_balance': fmt(fee_balance),
            'admission_balance': fmt(admission_balance),
            'total_due': fmt(total_due),
            'status': preview.status,
            'settled': settled,
        })

    for index, row in enumerate(rows, start=1):
        row['sl'] = index

    context = {
        'active': 'fees',
        'filters': filters,
        'rows': rows,
        'money_fields': MONEY_FIELDS,
        'year_options': academic_year_options(filters['academic_year']),
        'branch_choices': BRANCH_CHOICES,
        'std_choices': STD_CHOICES,
        'status_choices': [('all', 'All'), ('paid', 'Paid'), ('unpaid', 'Yet to pay')],
        'active_total': len(students),
        'tiles': {
            'billed': fmt(total_billed),
            'collected': fmt(total_collected),
            'outstanding': fmt(total_outstanding),
            'unpaid_count': unpaid_count,
        },
        'querystring': urlencode(filters),
    }
    return render(request, 'dashboard/admin/fees.html', context)


def _save_fee_sheet(request):
    """Upsert one `FeeRecord` per edited student for the selected academic year."""
    filters = _filters_from(request.POST)
    year = filters['academic_year']
    students = _active_students(filters)
    existing = {
        r.student_id: r
        for r in FeeRecord.objects.filter(academic_year=year, student__in=students)
    }

    saved = 0
    rejected = []

    for student in students:
        posted = {}
        touched = False
        for field in MONEY_FIELDS:
            raw = request.POST.get('{0}_{1}'.format(field, student.regnum))
            if raw is None:
                continue          # column not on screen; leave the stored value alone
            touched = True
            value = parse_money(raw)
            if value is None:
                rejected.append('{0} ({1})'.format(student.name, field.replace('_', ' ')))
                posted = None
                break
            posted[field] = value
        if not touched or posted is None:
            continue

        record = existing.get(student.regnum)
        if record is None and not any(v for v in posted.values()):
            # Nothing typed and nothing stored: do not litter the table with zero rows.
            continue
        if record is not None and all(getattr(record, f) == posted[f] for f in posted):
            continue

        FeeRecord.objects.update_or_create(
            student=student, academic_year=year, defaults=posted,
        )
        saved += 1

    if rejected:
        messages.info(
            request,
            'Ignored {0} amount(s) that were not a valid figure between 0 and {1}: {2}.'.format(
                len(rejected), MONEY_CEILING, ', '.join(rejected[:6]),
            ),
        )
    if saved:
        messages.info(request, 'Saved fees for {0} student(s) for {1}.'.format(saved, year))
    elif not rejected:
        messages.info(request, 'Nothing to save for {0} -- no amounts had changed.'.format(year))

    # POST-redirect-GET, keeping the year and filters the admin was looking at.
    return redirect('{0}?{1}'.format(reverse('admin-fees'), urlencode(filters)))


# ---------------------------------------------------------------------------
# Screen 2 -- faculty result analysis
# ---------------------------------------------------------------------------

CHART_WIDTH = 560          # viewBox units; the SVG itself is width:100%
CHART_TRACK = 430          # bar track length inside that viewBox
CHART_ROW_H = 46


def _parse_date(raw):
    raw = (raw or '').strip()
    if not raw:
        return None
    try:
        return datetime.strptime(raw, '%Y-%m-%d').date()
    except ValueError:
        return None


def _avg(values):
    return round(sum(values) / len(values), 1) if values else 0.0


@staff_required
def faculty_analysis(request):
    exam_type = (request.GET.get('exam_type') or 'all').strip()
    subject_id = (request.GET.get('subject') or '').strip()
    date_from = _parse_date(request.GET.get('date_from'))
    date_to = _parse_date(request.GET.get('date_to'))

    entries = MarkEntry.objects.select_related('faculty', 'subject', 'student')
    if exam_type in dict(EXAM_TYPE_CHOICES):
        entries = entries.filter(exam_type=exam_type)
    if subject_id.isdigit():
        entries = entries.filter(subject_id=int(subject_id))
    if date_from:
        entries = entries.filter(examdate__gte=date_from)
    if date_to:
        entries = entries.filter(examdate__lte=date_to)

    # Bucket by faculty, then by subject inside each faculty.
    buckets = {}
    for entry in entries:
        percent = entry.percent
        if percent is None:
            continue           # out_of is zero/blank: the row cannot be scored
        key = entry.faculty_id or ''
        bucket = buckets.setdefault(key, {
            'faculty': entry.faculty,
            'name': entry.faculty.name if entry.faculty else 'No faculty assigned',
            'empid': entry.faculty_id or '',
            'students': set(),
            'percents': [],
            'passed': 0,
            'failed': 0,
            'subjects': {},
        })
        bucket['students'].add(entry.student_id)
        bucket['percents'].append(percent)
        subject = bucket['subjects'].setdefault(entry.subject_id, {
            'name': entry.subject.name, 'percents': [], 'passed': 0, 'failed': 0,
        })
        subject['percents'].append(percent)
        if entry.passed:
            bucket['passed'] += 1
            subject['passed'] += 1
        else:
            bucket['failed'] += 1
            subject['failed'] += 1

    faculties = []
    for bucket in buckets.values():
        count = len(bucket['percents'])
        pass_rate = round(bucket['passed'] * 100.0 / count, 1) if count else 0.0
        faculties.append({
            'name': bucket['name'],
            'empid': bucket['empid'],
            'unassigned': bucket['faculty'] is None,
            'students': len(bucket['students']),
            'entries': count,
            'average': _avg(bucket['percents']),
            'passed': bucket['passed'],
            'failed': bucket['failed'],
            'pass_rate': pass_rate,
            'subjects': sorted(
                (
                    {
                        'name': s['name'],
                        'entries': len(s['percents']),
                        'average': _avg(s['percents']),
                        'passed': s['passed'],
                        'failed': s['failed'],
                    }
                    for s in bucket['subjects'].values()
                ),
                key=lambda s: s['name'],
            ),
        })

    faculties.sort(key=lambda f: (-f['pass_rate'], f['name']))

    # Pre-compute the inline SVG bar geometry: templates should not do arithmetic.
    chart_rows = []
    for index, faculty in enumerate(faculties):
        top = index * CHART_ROW_H
        chart_rows.append({
            'name': faculty['name'],
            'pass_rate': faculty['pass_rate'],
            'entries': faculty['entries'],
            'bar_width': round(CHART_TRACK * faculty['pass_rate'] / 100.0, 2) or 0.0,
            'y_label': top + 13,
            'y_bar': top + 20,
            'y_value': top + 31,
        })

    all_percents = [p for b in buckets.values() for p in b['percents']]
    total_passed = sum(b['passed'] for b in buckets.values())
    total_entries = len(all_percents)

    context = {
        'active': 'faculty',
        'has_any_data': MarkEntry.objects.exists(),
        'faculties': faculties,
        'chart_rows': chart_rows,
        'chart_width': CHART_WIDTH,
        'chart_track': CHART_TRACK,
        'chart_height': max(len(chart_rows) * CHART_ROW_H, CHART_ROW_H),
        'exam_type': exam_type,
        'exam_type_choices': EXAM_TYPE_CHOICES,
        'subject_id': subject_id,
        'subjects': Subject.objects.all(),
        'date_from': request.GET.get('date_from', ''),
        'date_to': request.GET.get('date_to', ''),
        'tiles': {
            'faculty_count': sum(1 for f in faculties if not f['unassigned']),
            'entries': total_entries,
            'average': _avg(all_percents),
            'pass_rate': round(total_passed * 100.0 / total_entries, 1) if total_entries else 0.0,
        },
    }
    return render(request, 'dashboard/admin/faculty_analysis.html', context)
