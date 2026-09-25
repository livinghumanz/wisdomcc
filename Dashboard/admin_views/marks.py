"""Spec page 2 -- mark entry and the Growth Card bar chart.

Two screens live here:

* ``marks_screen``  -- pick a student, pick how many subjects, enter a row each.
* ``growth_card``   -- the same student's marks drawn as an inline SVG bar chart.

Two things the handwritten spec left open (questions 5 and 6 of
``docs/requests/UI-002-admin-dashboard.md``) are answered the same way here as in
the model: **"Out of 100" and "P/F" are derived, never typed.**  The browser shows
them live as the admin types purely as a convenience; the values that reach the
database come from ``MarkEntry.percent`` / ``MarkEntry.result``, recomputed from
``mark`` and ``out_of`` on every read.  Nothing posted by the form is trusted for
either column -- the form does not even carry an input for them.

No charting library is used: the SVG geometry is computed here and emitted by the
template, so the Growth Card renders with no network access.
"""
from collections import OrderedDict
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.dateparse import parse_date

from ..auth_utils import staff_required
from ..choices import EXAM_TYPE_CHOICES
from ..models import MarkEntry, Staff, Student, Subject

#: Mirrors ``MarkEntry.pass_mark_percent``'s default; used for the live JS preview
#: and the chart's pass line.  The stored value still wins on every row.
PASS_PERCENT = MarkEntry._meta.get_field('pass_mark_percent').default

MAX_SUBJECT_ROWS = 10


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _decimal(raw):
    """Parse a posted number, returning ``None`` for blank or unusable input."""
    if raw is None:
        return None
    raw = raw.strip()
    if not raw:
        return None
    try:
        return Decimal(raw)
    except (InvalidOperation, ValueError):
        return None


def _fmt(value):
    """Trim trailing zeros so 45.00 prints as 45 (marks are usually whole)."""
    if value is None:
        return '-'
    value = Decimal(value)
    quantised = value.quantize(Decimal(1)) if value == value.to_integral_value() else value.normalize()
    return str(quantised)


def _num(value):
    """SVG coordinate as a short string -- never a Python float repr."""
    return '{0:.2f}'.format(float(value)).rstrip('0').rstrip('.') or '0'


def _exam_groups(student):
    """That student's saved entries, newest exam first, grouped per exam."""
    groups = OrderedDict()
    entries = (MarkEntry.objects
               .filter(student=student)
               .select_related('subject', 'faculty')
               .order_by('-examdate', 'exam_type', 'subject__order', 'subject__name'))
    for entry in entries:
        key = (entry.examdate, entry.exam_type, entry.exam_name)
        group = groups.get(key)
        if group is None:
            group = groups[key] = {
                'examdate': entry.examdate,
                'exam_type': entry.get_exam_type_display(),
                'exam_name': entry.exam_name,
                'rows': [],
                'total_mark': Decimal('0'),
                'total_out_of': Decimal('0'),
            }
        group['rows'].append(entry)
        group['total_mark'] += entry.mark
        group['total_out_of'] += entry.out_of or Decimal('0')
    for group in groups.values():
        group['total_mark'] = _fmt(group['total_mark'])
        group['total_out_of'] = _fmt(group['total_out_of'])
    return list(groups.values())


def _save_rows(request, student):
    """Create or update one ``MarkEntry`` per filled-in row.  Returns (saved, skipped)."""
    exam_type = request.POST.get('exam_type') or EXAM_TYPE_CHOICES[0][0]
    if exam_type not in dict(EXAM_TYPE_CHOICES):
        exam_type = EXAM_TYPE_CHOICES[0][0]
    exam_name = (request.POST.get('exam_name') or '').strip()[:60]
    examdate = parse_date((request.POST.get('examdate') or '').strip())
    if examdate is None:
        messages.info(request, 'Pick a valid exam date before saving.')
        return 0, 0

    subjects = {str(s.pk): s for s in Subject.objects.all()}
    faculties = {str(f.pk): f for f in Staff.objects.all()}

    saved = skipped = 0
    for index in range(1, MAX_SUBJECT_ROWS + 1):
        subject = subjects.get((request.POST.get('subject_%d' % index) or '').strip())
        mark = _decimal(request.POST.get('mark_%d' % index))
        if subject is None or mark is None:
            # A row the admin left blank (or never revealed) is not an error.
            if (request.POST.get('subject_%d' % index) or request.POST.get('mark_%d' % index) or '').strip():
                skipped += 1
            continue
        out_of = _decimal(request.POST.get('out_of_%d' % index)) or Decimal('100')
        if out_of <= 0:
            skipped += 1
            continue
        faculty = faculties.get((request.POST.get('faculty_%d' % index) or '').strip())
        # unique_together is (student, subject, exam_type, examdate): a re-entry of
        # the same exam corrects the existing row instead of raising IntegrityError.
        MarkEntry.objects.update_or_create(
            student=student, subject=subject, exam_type=exam_type, examdate=examdate,
            defaults={
                'faculty': faculty,
                'exam_name': exam_name,
                'mark': mark,
                'out_of': out_of,
                # "Out of 100" and P/F are deliberately absent: they are properties.
            },
        )
        saved += 1
    return saved, skipped


# ---------------------------------------------------------------------------
# screens
# ---------------------------------------------------------------------------

@staff_required
def marks_screen(request):
    students = Student.objects.filter(active_status='active')
    subjects = list(Subject.objects.filter(is_active=True))
    staff = list(Staff.objects.all())

    if request.method == 'POST':
        regnum = (request.POST.get('student') or '').strip()
        student = Student.objects.filter(pk=regnum).first()
        if student is None:
            messages.info(request, 'Choose a student before saving marks.')
        elif not subjects:
            messages.info(request, 'Add subjects in Django admin before entering marks.')
        else:
            saved, skipped = _save_rows(request, student)
            if saved:
                messages.info(request, '%d subject mark(s) saved for %s.%s' % (
                    saved, student.name,
                    ' %d row(s) skipped as incomplete.' % skipped if skipped else ''))
            elif skipped:
                messages.info(request, 'Nothing saved: %d row(s) were incomplete.' % skipped)
            return redirect('%s?student=%s' % (reverse('admin-marks'), student.pk))
        selected = student
    else:
        selected = Student.objects.filter(pk=(request.GET.get('student') or '').strip()).first()

    row_count = 0
    try:
        row_count = int(request.GET.get('rows') or 0)
    except ValueError:
        row_count = 0
    row_count = max(0, min(row_count, MAX_SUBJECT_ROWS))

    context = {
        'active': 'marks',
        'students': students,
        'subjects': subjects,
        'staff': staff,
        'exam_types': EXAM_TYPE_CHOICES,
        'selected': selected,
        'row_choices': range(1, MAX_SUBJECT_ROWS + 1),
        'rows': range(1, MAX_SUBJECT_ROWS + 1),
        'initial_rows': row_count,
        'pass_percent': PASS_PERCENT,
        'exam_groups': _exam_groups(selected) if selected else [],
    }
    return render(request, 'dashboard/admin/marks.html', context)


@staff_required
def growth_card(request, regnum):
    student = get_object_or_404(Student, pk=regnum)

    exam_type = (request.GET.get('exam_type') or '').strip()
    if exam_type not in dict(EXAM_TYPE_CHOICES):
        exam_type = ''

    entries = (MarkEntry.objects
               .filter(student=student)
               .select_related('subject', 'faculty')
               .order_by('subject__order', 'subject__name', '-examdate'))
    if exam_type:
        entries = entries.filter(exam_type=exam_type)

    # --- average the entries of each subject (a subject can appear in many exams)
    buckets = OrderedDict()
    for entry in entries:
        bucket = buckets.get(entry.subject_id)
        if bucket is None:
            bucket = buckets[entry.subject_id] = {
                'subject': entry.subject.name, 'mark': Decimal('0'), 'out_of': Decimal('0'),
                'percents': [], 'count': 0, 'faculties': [],
            }
        bucket['mark'] += entry.mark
        bucket['out_of'] += entry.out_of or Decimal('0')
        # percent is the model's derived "Out of 100" -- never a posted figure.
        if entry.percent is not None:
            bucket['percents'].append(entry.percent)
        bucket['count'] += 1
        name = entry.faculty.name if entry.faculty else ''
        if name and name not in bucket['faculties']:
            bucket['faculties'].append(name)

    rows, averaged = [], False
    for bucket in buckets.values():
        percents = bucket['percents']
        percent = round(sum(percents) / len(percents), 2) if percents else None
        if bucket['count'] > 1:
            averaged = True
        rows.append({
            'subject': bucket['subject'],
            'mark': _fmt(bucket['mark']),
            'out_of': _fmt(bucket['out_of']),
            'percent': percent,
            'passed': None if percent is None else percent >= PASS_PERCENT,
            'result': '-' if percent is None else ('P' if percent >= PASS_PERCENT else 'F'),
            'faculty': ', '.join(bucket['faculties']) or '-',
            'count': bucket['count'],
        })

    scored = [r for r in rows if r['percent'] is not None]
    passed = sum(1 for r in scored if r['passed'])
    stats = {
        'subjects': len(rows),
        'average': round(sum(r['percent'] for r in scored) / len(scored), 1) if scored else None,
        'passed': passed,
        'failed': len(scored) - passed,
    }

    context = {
        'active': 'marks',
        'student': student,
        'rows': rows,
        'averaged': averaged,
        'stats': stats,
        'exam_types': EXAM_TYPE_CHOICES,
        'exam_type': exam_type,
        'pass_percent': PASS_PERCENT,
        'chart': _build_chart(rows) if rows else None,
    }
    return render(request, 'dashboard/admin/growth_card.html', context)


# ---------------------------------------------------------------------------
# the chart -- plain geometry, no library, no CDN
# ---------------------------------------------------------------------------

PAD_L, PAD_R, PAD_T, PAD_B = 48, 20, 22, 64
PLOT_H = 260
SLOT, BAR_W = 92, 48
PASS_COLOUR, FAIL_COLOUR = '#0ec7a7', '#e5484d'


def _bar_path(x, y, width, height):
    """A bar with 4px rounded data-end, square on the baseline."""
    baseline = y + height
    radius = min(4.0, width / 2.0, height)
    if radius <= 0:
        return ''
    return ('M{0} {1} V{2} Q{0} {3} {4} {3} H{5} Q{6} {3} {6} {2} V{1} Z'.format(
        _num(x), _num(baseline), _num(y + radius), _num(y),
        _num(x + radius), _num(x + width - radius), _num(x + width)))


def _build_chart(rows):
    """Everything the template needs to emit the SVG; all numbers pre-formatted."""
    count = len(rows)
    width = PAD_L + SLOT * count + PAD_R
    height = PAD_T + PLOT_H + PAD_B
    baseline = PAD_T + PLOT_H

    def y_for(percent):
        return baseline - PLOT_H * (max(0.0, min(100.0, float(percent))) / 100.0)

    gridlines = [{'value': v, 'y': _num(y_for(v))} for v in (0, 20, 40, 60, 80, 100)]

    bars = []
    for index, row in enumerate(rows):
        percent = row['percent'] or 0
        centre = PAD_L + SLOT * index + SLOT / 2.0
        x = centre - BAR_W / 2.0
        top = y_for(percent)
        bar_h = baseline - top
        # The value sits above the bar, or inside it when the bar reaches the top.
        if top - 8 < PAD_T + 10:
            label_y, label_fill = top + 16, '#ffffff'
        else:
            label_y, label_fill = top - 8, '#23293d'
        name = row['subject']
        bars.append({
            'subject': name,
            'short': name if len(name) <= 11 else name[:10] + '…',
            'percent': row['percent'],
            'mark': row['mark'],
            'out_of': row['out_of'],
            'count': row['count'],
            'colour': FAIL_COLOUR if row['passed'] is False else PASS_COLOUR,
            'path': _bar_path(x, top, BAR_W, bar_h),
            'x': _num(x),
            'centre': _num(centre),
            'slot_x': _num(PAD_L + SLOT * index),
            'label_y': _num(label_y),
            'label_fill': label_fill,
        })

    return {
        'width': width,
        'height': height,
        'view_box': '0 0 {0} {1}'.format(width, height),
        'baseline': _num(baseline),
        'plot_left': _num(PAD_L),
        'plot_right': _num(width - PAD_R),
        'plot_top': _num(PAD_T),
        'axis_label_x': _num(PAD_L - 10),
        'subject_label_y': _num(baseline + 22),
        'detail_label_y': _num(baseline + 38),
        'gridlines': gridlines,
        'pass_y': _num(y_for(PASS_PERCENT)),
        'pass_label_y': _num(y_for(PASS_PERCENT) - 5),
        'slot_w': _num(SLOT),
        'bars': bars,
    }
