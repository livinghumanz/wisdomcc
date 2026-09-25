"""Students screen for the admin portal (spec page 1, UI-002).

Holds the list/filter screen, the add/edit form and the delete action. The form
is a ModelForm -- the first in this project -- but it is rendered field by field
through the admin portal's own CSS classes, never `{{ form.as_p }}`.
"""
from django import forms
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from ..auth_utils import staff_required
from ..choices import (
    ACTIVE_STATUS_CHOICES, BRANCH_CHOICES, CURRICULUM_CHOICES, STD_CHOICES, TEAM_CHOICES,
)
from ..models import Student

# The pill colour for each active status (spec: Active / Discontinued / Re-Joining).
PILL_CLASSES = {
    'active': 'pill pill--green',
    'discontinued': 'pill pill--red',
    'rejoining': 'pill pill--amber',
}

# Section headings on the form, in the order the spec lists the fields.
FIELD_GROUPS = [
    ('Student', [
        'image', 'regnum', 'name', 'dob', 'DateofJoin', 'aadhar',
        'std', 'category', 'curriculum', 'school', 'address',
    ]),
    ('Parents', [
        'fname', 'father_mobile', 'father_whatsapp',
        'mname', 'mother_mobile', 'mother_whatsapp',
    ]),
    ('Administration', ['branch', 'team', 'active_status', 'FeeAmount', 'password']),
]

# Fields that span the whole grid row.
WIDE_FIELDS = {'address'}


def _digits(value):
    """The digits in a typed phone number, e.g. '+91 97911-48553' -> 9791148553."""
    only = ''.join(ch for ch in (value or '') if ch.isdigit())
    return int(only[:18]) if only else None


class StudentForm(forms.ModelForm):
    """Add / edit a student.

    Only `regnum` and `name` are mandatory, per the spec's validation rules; the
    model's older CharFields are relaxed to optional here so a record can be
    started from a phone call and completed later. `dob` stays mandatory because
    the column is NOT NULL and a date has no empty-string equivalent.
    """

    class Meta:
        model = Student
        fields = [
            'image', 'regnum', 'name', 'dob', 'DateofJoin', 'aadhar',
            'std', 'category', 'curriculum', 'school', 'address',
            'fname', 'father_mobile', 'father_whatsapp',
            'mname', 'mother_mobile', 'mother_whatsapp',
            'branch', 'team', 'active_status', 'FeeAmount', 'password',
        ]
        labels = {
            'image': 'Photo',
            'regnum': 'Reg No',
            'name': 'Student name',
            'dob': 'Date of birth',
            'DateofJoin': 'Date of join',
            'aadhar': 'Aadhaar no',
            'std': 'Class / STD',
            'category': 'Category',
            'curriculum': 'Curriculum',
            'school': 'School',
            'address': 'Address',
            'fname': 'Father name',
            'father_mobile': 'Father mobile no',
            'father_whatsapp': 'Father WhatsApp no',
            'mname': 'Mother name',
            'mother_mobile': 'Mother mobile no',
            'mother_whatsapp': 'Mother WhatsApp no',
            'branch': 'Branch',
            'team': 'Team',
            'active_status': 'Active status',
            'FeeAmount': 'Fee amount',
            'password': 'Login password',
        }
        help_texts = {
            'image': 'Optional. JPG or PNG.',
            'FeeAmount': 'Annual fee in rupees.',
        }
        widgets = {
            'regnum': forms.TextInput(attrs={'placeholder': 'e.g. WCC001'}),
            'name': forms.TextInput(attrs={'placeholder': 'Full name'}),
            'dob': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'DateofJoin': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'aadhar': forms.TextInput(attrs={'placeholder': '12 digits', 'inputmode': 'numeric'}),
            'school': forms.TextInput(attrs={'placeholder': 'School name'}),
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Door no, street, area, pin'}),
            'father_mobile': forms.TextInput(attrs={'inputmode': 'tel', 'placeholder': '10 digits'}),
            'father_whatsapp': forms.TextInput(attrs={'inputmode': 'tel', 'placeholder': '10 digits'}),
            'mother_mobile': forms.TextInput(attrs={'inputmode': 'tel', 'placeholder': '10 digits'}),
            'mother_whatsapp': forms.TextInput(attrs={'inputmode': 'tel', 'placeholder': '10 digits'}),
            'FeeAmount': forms.NumberInput(attrs={'min': 0, 'step': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # `regnum` is a CharField primary key, so a brand-new instance has pk ''
        # rather than None -- `is not None` would wrongly report an edit.
        self.is_edit = bool(self.instance.pk)
        self._original_password = self.instance.password if self.is_edit else ''

        # The photo is genuinely optional -- the list screen falls back to initials.
        self.fields['image'].required = False
        # Spec mandates only Reg No and Name. `DateofJoin` and `FeeAmount` are
        # nullable in the model but lack blank=True, so Django would demand them.
        for name in ('aadhar', 'address', 'school', 'fname', 'mname', 'password',
                     'DateofJoin', 'FeeAmount'):
            self.fields[name].required = False
        self.fields['regnum'].error_messages['required'] = 'Reg No is required.'
        self.fields['name'].error_messages['required'] = 'Student name is required.'
        self.fields['password'].help_text = (
            'Leave blank to keep the current password.' if self.is_edit
            else 'Password the student uses to log in.')

        if self.is_edit:
            # Reg No is the primary key; changing it would orphan marks and fees.
            self.fields['regnum'].disabled = True
            self.fields['regnum'].help_text = 'Reg No cannot be changed after creation.'

    def clean_regnum(self):
        regnum = (self.cleaned_data.get('regnum') or '').strip()
        if not regnum:
            raise forms.ValidationError('Reg No is required.')
        if not self.is_edit and Student.objects.filter(regnum=regnum).exists():
            raise forms.ValidationError('A student with Reg No "%s" already exists.' % regnum)
        return regnum

    def clean_name(self):
        name = (self.cleaned_data.get('name') or '').strip()
        if not name:
            raise forms.ValidationError('Student name is required.')
        return name

    def save(self, commit=True):
        student = super().save(commit=False)

        # Keep the existing password when the field is left blank on an edit.
        if not student.password and self.is_edit:
            student.password = self._original_password

        # `contact` / `WhatsappNo` are the legacy columns the student dashboard
        # still reads, and `contact` is NOT NULL. Mirror the father's numbers
        # into them so both dashboards agree; never blank an existing value.
        father = _digits(student.father_mobile)
        if father is not None:
            student.contact = father
        elif student.contact is None:
            student.contact = 0

        whatsapp = _digits(student.father_whatsapp)
        if whatsapp is not None:
            student.WhatsappNo = whatsapp

        if commit:
            student.save()
        return student


def _decorate(students):
    """Attach the presentation-only bits the templates need (no custom filters here)."""
    for student in students:
        student.pill_class = PILL_CLASSES.get(student.active_status, 'pill pill--grey')
        parts = [p for p in (student.name or '').split() if p]
        student.initials = ''.join(p[0] for p in parts[:2]).upper() or '?'
    return students


@staff_required
def student_list(request):
    """Searchable, filterable list of students (spec page 1)."""
    filters = {
        'q': request.GET.get('q', '').strip(),
        'branch': request.GET.get('branch', '').strip(),
        'std': request.GET.get('std', '').strip(),
        'active_status': request.GET.get('active_status', '').strip(),
        'team': request.GET.get('team', '').strip(),
    }

    queryset = Student.objects.all()
    if filters['q']:
        queryset = queryset.filter(
            Q(name__icontains=filters['q'])
            | Q(regnum__icontains=filters['q'])
            | Q(school__icontains=filters['q'])
        )
    for field in ('branch', 'std', 'active_status', 'team'):
        if filters[field]:
            queryset = queryset.filter(**{field: filters[field]})

    students = _decorate(list(queryset))

    # Tiles describe what is currently on screen, so they respond to the filters.
    counts = {'active': 0, 'discontinued': 0, 'rejoining': 0}
    for student in students:
        if student.active_status in counts:
            counts[student.active_status] += 1

    context = {
        'active': 'students',
        'students': students,
        'filters': filters,
        'has_filters': any(filters.values()),
        'shown_count': len(students),
        'total_count': Student.objects.count(),
        'count_active': counts['active'],
        'count_discontinued': counts['discontinued'],
        'count_rejoining': counts['rejoining'],
        'std_choices': STD_CHOICES,
        'branch_choices': BRANCH_CHOICES,
        'active_status_choices': ACTIVE_STATUS_CHOICES,
        'team_choices': TEAM_CHOICES,
        'curriculum_choices': CURRICULUM_CHOICES,
    }
    return render(request, 'dashboard/admin/students.html', context)


@staff_required
def student_form(request, regnum=None):
    """Add a student (regnum is None) or edit an existing one."""
    student = get_object_or_404(Student, pk=regnum) if regnum else None

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            saved = form.save()
            messages.success(
                request,
                'Student %s (%s) was %s.' % (
                    saved.name, saved.regnum, 'updated' if student else 'added'),
            )
            return redirect('admin-students')
        messages.info(request, 'Please correct the highlighted fields.')
    else:
        form = StudentForm(instance=student)

    groups = [
        (title, [form[name] for name in names if name in form.fields])
        for title, names in FIELD_GROUPS
    ]

    context = {
        'active': 'students',
        'form': form,
        'groups': groups,
        'wide_fields': WIDE_FIELDS,
        'student': student,
        'is_edit': student is not None,
    }
    return render(request, 'dashboard/admin/student_form.html', context)


@staff_required
def student_delete(request, regnum):
    """Delete a student. POST only -- a GET just bounces back to the list."""
    if request.method != 'POST':
        return redirect('admin-students')

    student = get_object_or_404(Student, pk=regnum)
    label = '%s (%s)' % (student.name, student.regnum)
    student.delete()
    messages.success(request, 'Student %s was deleted.' % label)
    return redirect('admin-students')
