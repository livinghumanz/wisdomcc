from datetime import datetime

from django.db import models

from .choices import (
    ACTIVE_STATUS_CHOICES, ATTENDANCE_STATUS_CHOICES, BRANCH_CHOICES, CATEGORY_CHOICES,
    CURRICULUM_CHOICES, EXAM_TYPE_CHOICES, STD_CHOICES, TEAM_CHOICES,
)

# Create your models here.
class Student(models.Model):
    regnum = models.CharField(primary_key=True,max_length=20)
    #up_path="/images/profilepic/"+str(reg_num)+str(name).split()[0]
    image = models.ImageField(upload_to='images/profilepic/%y/%m/%d/')
    name = models.CharField(max_length=40)
    dob = models.DateField()
    DateofJoin = models.DateField(null=True)
    aadhar = models.CharField(max_length=20)
    address = models.TextField()
    ystudy = models.CharField(max_length=10)
    school = models.TextField()
    fname = models.CharField(max_length=40)
    mname = models.CharField(max_length=40)
    foccupation = models.CharField(max_length=100)
    moccupation = models.CharField(max_length=100)
    contact = models.BigIntegerField()
    WhatsappNo = models.BigIntegerField(null=True)
    password = models.CharField(max_length= 40)
    timetable = models.ImageField(upload_to='images/timetable/',null=True)
    FeeDue = models.BooleanField(default=True)
    FeeDate = models.DateField(null=True)
    FeeAmount = models.BigIntegerField(null=True)

    # ---- added for the admin portal (spec page 1) ----
    std = models.CharField('Class / STD', max_length=5, choices=STD_CHOICES, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True)
    curriculum = models.CharField(max_length=10, choices=CURRICULUM_CHOICES, blank=True)
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES, blank=True)
    active_status = models.CharField(max_length=15, choices=ACTIVE_STATUS_CHOICES, default='active')
    team = models.CharField(max_length=15, choices=TEAM_CHOICES, blank=True)
    # Phone numbers are text, not integers: they can carry leading zeros and separators.
    father_mobile = models.CharField(max_length=20, blank=True)
    father_whatsapp = models.CharField(max_length=20, blank=True)
    mother_mobile = models.CharField(max_length=20, blank=True)
    mother_whatsapp = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ['name']

    @property
    def is_active_student(self):
        return self.active_status == 'active'

    @property
    def display_class(self):
        return self.get_std_display() if self.std else (self.ystudy or '-')

    def __str__(self):
        return '{0} : {1}'.format(self.regnum,self.name.split()[0])

# --------- Staff model -----------
class Staff(models.Model):
    empid = models.CharField(primary_key=True,max_length=20)
    name = models.CharField(max_length=40)

    def __str__(self):
        return '{0} : {1}'.format(self.empid,self.name.split()[0])

# ------ Course model -----
class Course(models.Model):
    staffid = models.ForeignKey(Staff,on_delete=models.DO_NOTHING)
    cname = models.CharField(max_length=20)

    def __str__(self):
        return '{0}'.format(self.cname)

# -------- Attendance model -------
class Attendance(models.Model):
    studentid = models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    edate = models.DateField()
    present = models.BooleanField(default=False)
    late = models.BooleanField(default=False)
    # `present` alone cannot express the spec's third state, "No Class (Holiday)".
    # It is kept in sync below so the existing student dashboard keeps working.
    status = models.CharField(max_length=10, choices=ATTENDANCE_STATUS_CHOICES, default='present')

    class Meta:
        unique_together = ('studentid', 'edate')
        ordering = ['-edate']

    def save(self, *args, **kwargs):
        self.present = self.status == 'present'
        return super().save(*args, **kwargs)

    def __str__(self):
        if self.present==True:
            return '{1} |{0} -> present'.format(self.studentid,self.edate)
        return '{1} |{0}  -> absent'.format(self.studentid,self.edate)

# ------ Marks model -----
class Mark(models.Model):
    studentid = models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    courseid = models.ForeignKey(Course,on_delete=models.DO_NOTHING)
    score = models.IntegerField()
    examdate = models.DateField()

    def __str__(self):
        return '{0} : {1} -> {2}'.format(self.studentid,self.courseid,self.score)


# ---------------------------------------------------------------------------
# Admin portal models (spec pages 2 and 3)
# ---------------------------------------------------------------------------

class Subject(models.Model):
    """A subject that marks are recorded against, e.g. Tamil or Maths."""

    name = models.CharField(max_length=60, unique=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class MarkEntry(models.Model):
    """One subject's result for one student in one exam.

    Separate from the older `Mark` model, which the student dashboard still
    reads and which carries no faculty, exam type or maximum.
    """

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='mark_entries')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name='mark_entries')
    faculty = models.ForeignKey(
        Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='mark_entries',
        help_text='Drives the faculty result analysis.',
    )
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPE_CHOICES, default='internal')
    exam_name = models.CharField(max_length=60, blank=True)
    examdate = models.DateField()
    mark = models.DecimalField(max_digits=6, decimal_places=2)
    out_of = models.DecimalField(max_digits=6, decimal_places=2, default=100)
    pass_mark_percent = models.PositiveSmallIntegerField(
        default=35, help_text='Percentage at or above which the result counts as a pass.')

    class Meta:
        ordering = ['-examdate', 'subject__order']
        unique_together = ('student', 'subject', 'exam_type', 'examdate')
        verbose_name_plural = 'mark entries'

    @property
    def percent(self):
        """The spec's "Out of 100" column, derived rather than typed (open question 5)."""
        if not self.out_of:
            return None
        return round((float(self.mark) / float(self.out_of)) * 100, 2)

    @property
    def passed(self):
        pct = self.percent
        return None if pct is None else pct >= self.pass_mark_percent

    @property
    def result(self):
        passed = self.passed
        return '-' if passed is None else ('P' if passed else 'F')

    def __str__(self):
        return '{0} - {1}: {2}/{3}'.format(self.student_id, self.subject, self.mark, self.out_of)


class FeeRecord(models.Model):
    """Fee position for one student in one academic year (spec page 3)."""

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fee_records')
    academic_year = models.CharField(max_length=9, help_text='e.g. 2026-27')
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    admission_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    admission_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    jersey_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    material_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    updated_on = models.DateField(auto_now=True)
    remarks = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-academic_year', 'student__name']
        unique_together = ('student', 'academic_year')

    @property
    def fee_balance(self):
        return self.fee_amount - self.paid_amount

    @property
    def admission_balance(self):
        return self.admission_amount - self.admission_paid

    @property
    def total_due(self):
        """Everything still owed across fees, admission, jersey and materials."""
        return self.fee_balance + self.admission_balance + self.jersey_amount + self.material_amount

    @property
    def is_settled(self):
        return self.total_due <= 0

    @property
    def status(self):
        return 'Paid' if self.is_settled else 'Yet to pay'

    def __str__(self):
        return '{0} {1}: {2}'.format(self.student_id, self.academic_year, self.status)


class Feature(models.Model):
    """A portal capability the superuser can switch on or off.

    Lets the owner demo a screen to the client and bill for it before leaving it
    enabled. Only a superuser can see or change these -- portal users have
    `is_staff=False`, so they cannot reach Django admin at all.
    """

    key = models.SlugField(
        unique=True,
        help_text='Internal id used in code. Do not change once set.',
    )
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=250, blank=True)
    is_enabled = models.BooleanField(
        default=True,
        help_text='Off hides the screen and blocks its URL, even if someone types it directly.',
    )
    show_when_disabled = models.BooleanField(
        'Show as locked when disabled',
        default=False,
        help_text='Leave the item visible in the menu with a padlock, so the client can see the '
                  'feature exists. Off hides it completely.',
    )
    is_billable = models.BooleanField(
        'Chargeable add-on',
        default=False,
        help_text='Marker for your own billing. Has no effect on access.',
    )
    notes = models.CharField(max_length=250, blank=True, help_text='Private note. Never shown to the client.')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return '{0} ({1})'.format(self.name, 'on' if self.is_enabled else 'off')
