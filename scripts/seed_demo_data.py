"""Seed realistic demo data into a LOCAL development database.

Run:  ./venv/bin/python scripts/seed_demo_data.py

Refuses to run against anything but a local database, so it cannot be pointed at
production by accident. This is demo data, deliberately NOT a migration -- a
migration would seed these fake students onto the live site.
"""
import os
import random
import sys
from datetime import date, timedelta
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wisdomcc.settings')

import django  # noqa: E402
django.setup()

from django.db import connection  # noqa: E402
from Dashboard.models import (  # noqa: E402
    Attendance, FeeRecord, MarkEntry, Staff, Student, Subject,
)

HOST = connection.settings_dict['HOST']
if HOST not in ('', 'localhost', '127.0.0.1'):
    sys.exit('Refusing to seed demo data into a non-local database (HOST=%r).' % HOST)

random.seed(20260925)

STUDENTS = [
    # regnum, name, std, curriculum, branch, school, team, status, father, mother, fee
    ('WCC001', 'Arjun Kumar',      'X',    'state', 'wcc_r', 'St Marys Hr Sec School',   'ripplers', 'active',       'Kumar S',     'Lakshmi K',   2500),
    ('WCC002', 'Divya Raman',      'IX',   'cbse',  'wcc_r', 'Velammal Vidyalaya',       'planners', 'active',       'Raman V',     'Shanti R',    2400),
    ('WCC003', 'Rahul Menon',      'XII',  'cbse',  'wcc_g', 'DAV Public School',        'ripplers', 'active',       'Menon P',     'Gita M',      3200),
    ('WCC004', 'Sneha Prakash',    'XI',   'state', 'wcc_g', 'Kendriya Vidyalaya',       'planners', 'active',       'Prakash N',   'Uma P',       3000),
    ('WCC005', 'Karthik Vel',      'VIII', 'state', 'wcc_r', 'Govt Hr Sec School',       'ripplers', 'active',       'Vel M',       'Devi V',      2200),
    ('WCC006', 'Priya Nandini',    'X',    'icse',  'wcc_a', 'Holy Angels School',       'planners', 'active',       'Nandan R',    'Kala N',      2600),
    ('WCC007', 'Mohammed Irfan',   'IX',   'cbse',  'wcc_r', 'Crescent Matric School',   'ripplers', 'active',       'Irfan A',     'Fatima I',    2400),
    ('WCC008', 'Anitha Selvam',    'XII',  'state', 'wcc_g', 'Chennai Girls Hr Sec',     'planners', 'active',       'Selvam K',    'Mala S',      3200),
    ('WCC009', 'Vignesh Babu',     'VII',  'state', 'wcc_r', 'Little Flower School',     'ripplers', 'active',       'Babu T',      'Radha B',     2000),
    ('WCC010', 'Lakshmi Sundar',   'XI',   'igcse', 'wcc_a', 'Chettinad Vidyashram',     'planners', 'active',       'Sundar G',    'Meena S',     3400),
    ('WCC011', 'Ganesh Moorthy',   'X',    'state', 'wcc_g', 'Govt Boys Hr Sec School',  'ripplers', 'discontinued', 'Moorthy L',   'Vani M',      2500),
    ('WCC012', 'Fathima Zahra',    'IX',   'cbse',  'wcc_r', 'MCC Matric Hr Sec',        'planners', 'rejoining',    'Zahir H',     'Naseema Z',   2400),
]

SUBJECTS = ['Tamil', 'English', 'Maths', 'Science', 'Social Science']
FACULTY = [('EMP01', 'Priya Raman'), ('EMP02', 'Ravi Shankar'), ('EMP03', 'Anand Krishnan')]


def run():
    staff = [Staff.objects.get_or_create(empid=e, defaults={'name': n})[0] for e, n in FACULTY]
    subjects = [Subject.objects.get_or_create(name=n, defaults={'order': i})[0]
                for i, n in enumerate(SUBJECTS, 1)]

    for i, (reg, name, std, curr, branch, school, team, status, fa, mo, fee) in enumerate(STUDENTS):
        mobile = '90000%05d' % (11000 + i)
        st, _ = Student.objects.update_or_create(regnum=reg, defaults=dict(
            name=name, dob=date(2026 - 15 + i % 5, 1 + i % 12, 1 + i % 28),
            DateofJoin=date(2024, 6, 1), aadhar='%04d %04d %04d' % (1000 + i, 5678, 9012),
            address='%d Gandhi Nagar West, Redhills, Chennai 600052' % (10 + i),
            ystudy=std, std=std, school=school, curriculum=curr, branch=branch,
            team=team, active_status=status, category='regular',
            fname=fa, mname=mo, foccupation='Business', moccupation='Homemaker',
            father_mobile=mobile, father_whatsapp=mobile,
            mother_mobile='90000%05d' % (22000 + i), mother_whatsapp='90000%05d' % (22000 + i),
            contact=int(mobile), WhatsappNo=int(mobile),
            password=name.split()[0].lower() + '123', FeeAmount=fee,
            FeeDue=i % 3 != 0, FeeDate=date(2026, 10, 5),
        ))

        # marks: two exams per student across the subjects
        for exam_i, (etype, ename, edate) in enumerate([
                ('internal', 'Unit Test 1', date(2026, 7, 18)),
                ('external', 'Quarterly', date(2026, 9, 12))]):
            for sub_i, sub in enumerate(subjects):
                base = 35 + ((i * 7 + sub_i * 13 + exam_i * 5) % 58)
                MarkEntry.objects.update_or_create(
                    student=st, subject=sub, exam_type=etype, examdate=edate,
                    defaults=dict(faculty=staff[(sub_i + i) % len(staff)],
                                  exam_name=ename, mark=Decimal(base), out_of=Decimal(100)))

        # attendance: last 20 weekdays
        d, added = date(2026, 9, 25), 0
        while added < 20:
            if d.weekday() < 5:
                roll = (i * 3 + added) % 10
                status_v = 'no_class' if roll == 7 else ('absent' if roll in (2, 5) else 'present')
                Attendance.objects.update_or_create(
                    studentid=st, edate=d,
                    defaults={'status': status_v, 'present': status_v == 'present'})
                added += 1
            d -= timedelta(days=1)

        # fees
        paid = Decimal(fee) if i % 3 == 0 else Decimal(fee) - Decimal(500 + i * 25)
        FeeRecord.objects.update_or_create(
            student=st, academic_year='2026-27',
            defaults=dict(fee_amount=Decimal(fee), paid_amount=paid,
                          admission_amount=Decimal(1500), admission_paid=Decimal(1500 if i % 2 else 750),
                          jersey_amount=Decimal(0 if i % 2 else 450),
                          material_amount=Decimal(325 if i % 4 else 0)))

    print('Students   :', Student.objects.count())
    print('Subjects   :', Subject.objects.count())
    print('Staff      :', Staff.objects.count())
    print('MarkEntry  :', MarkEntry.objects.count())
    print('Attendance :', Attendance.objects.count())
    print('FeeRecord  :', FeeRecord.objects.count())
    print('\nStudent logins are firstname + "123", e.g. WCC002 / divya123')


if __name__ == '__main__':
    run()
