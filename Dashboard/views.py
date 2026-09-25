import csv
from django.shortcuts import redirect, render
from django.http import HttpResponse, request, HttpResponseRedirect
from home.models import Admision,Fupload
from .models import *
from django.contrib import messages,auth
from .auth_utils import can_use_portal, portal_required, student_required
# Create your views here.


def _login_admin(request):
    """Authenticate a staff user and actually establish a session.

    The previous version called `auth.authenticate()` and discarded the result
    without `auth.login()`, so nothing was ever logged in and no page could be
    revisited or bookmarked. It also never checked `is_staff` (defect S7).
    """
    user = auth.authenticate(
        request,
        username=request.POST.get('loginid', '').strip().lower(),
        password=request.POST.get('lpassword', ''),
    )
    if user is None:
        messages.info(request, 'Incorrect admin login details.')
        return redirect('/')
    if not can_use_portal(user):
        messages.info(request, 'That account does not have admin access.')
        return redirect('/')
    auth.login(request, user)
    return redirect('admin-students')


def _login_student(request):
    """Look the student up and remember them in the session.

    Passwords here are still compared in plain text (defect S3) -- unchanged by
    this pass, but now at least the login produces a session, so the dashboard
    survives a refresh instead of being reachable only as a POST response.
    """
    regnum = request.POST.get('loginid', '').strip()
    password = request.POST.get('lpassword', '')
    student = Student.objects.filter(regnum=regnum, password=password).first()
    if student is None:
        messages.info(request, 'Incorrect login details.')
        return redirect('/')
    request.session['student_regnum'] = student.regnum
    return redirect('Dashboard')


def _student_dashboard(request, regnum):
    student = Student.objects.filter(regnum=regnum).first()
    if student is None:
        request.session.pop('student_regnum', None)
        return redirect('/')

    score = []
    for i, entry in enumerate(Mark.objects.filter(studentid__regnum=regnum).values_list(), start=1):
        row = list(entry)
        row[0] = i
        course = Course.objects.filter(id=row[2]).first()
        row[2] = course.cname if course else '-'
        score.append(row)

    return render(request, 'dashboard/dashboard_user.html', {
        'marks': score,
        # These were `.url` accesses that raised ValueError when no file was set (defect F6).
        'image': student.image.url if student.image else '',
        'timetable': student.timetable.url if student.timetable else '',
        'name': student.name.split()[0],
        'sdata': [student],
        'student': student,
        'notes': Fupload.objects.filter(mtype='notes'),
    })


def logout_view(request):
    request.session.pop('student_regnum', None)
    auth.logout(request)
    return redirect('/')


def dashboard(request):
    """Login dispatcher, and the landing page for whoever is already logged in."""
    if request.method == 'POST':
        if request.POST.get('ltype') == 'admin':
            return _login_admin(request)
        return _login_student(request)

    # GET: send whoever is already signed in to the right place.
    if can_use_portal(request.user):
        return redirect('admin-students')
    regnum = request.session.get('student_regnum')
    if regnum:
        return _student_dashboard(request, regnum)
    messages.info(request, 'Please log in to continue.')
    return redirect('/')

@portal_required
def export(request):
    response= HttpResponse(content_type = 'text/csv')
    writer = csv.writer(response)
    writer.writerow(['#','Name','School','Contact No','Location opted','Class','Mail id'])
    
    for entry in Admision.objects.all().values_list('id','sname','school','contact','slocation','ystudy','mailid'):
        '''entry1= list(entry)
        entry1[3]='hello'
        entry=tuple(entry1)
        print(entry)'''
        writer.writerow(entry)
    
    response['Content-Disposition'] = 'attachment; filename="applications.csv"'
    return response

@student_required
def reportdown(request, stid):
    """Download the signed-in student's own report.

    The regno now comes from the session, not the POST body: previously any
    caller could pass another student's number and get their records (S5).
    """
    if request.method == 'POST':
        regno = request.session['student_regnum']
        if stid == "attendance":
            response= HttpResponse(content_type = 'text/csv')
            writer = csv.writer(response)
            writer.writerow(['S.No','ID','Date','Present/Absent','Late'])
            i=1
            for entry in Attendance.objects.all().filter(studentid__regnum=regno).values_list():
                entry1 = list(entry)
                entry1[0]=i
                i+=1
                if entry1[3] == True:
                    entry1[3]='present'
                else:
                    entry1[3]='absent'
                entry=tuple(entry1)
                writer.writerow(entry)
            response['Content-Disposition'] = 'attachment; filename="Attendance_report.csv"'
            return response

        elif stid == "mark":
            i=1
            marks=[]
            for entry in Mark.objects.all().filter(studentid__regnum=regno).values_list():
                entry1=list(entry)
                entry1[0]=i
                i+=1
                entry1[2]=Course.objects.all().filter(id=entry1[2])[0].cname
                print(type(entry1))
                marks.append(tuple(entry1))
            print(marks[0][1])
            '''response= HttpResponse(content_type = 'text/csv')
            writer = csv.writer(response)
            writer.writerow(['S.No','ID','Course','Score','Exam-Date'])
            i=1
            for entry in Mark.objects.all().filter(studentid__regnum=regno).values_list():
                entry1 = list(entry)
                entry1[0]=i
                i+=1
                entry1[2]=Course.objects.all().filter(id=entry1[2])[0].cname
                entry=tuple(entry1)
                writer.writerow(entry)
            response['Content-Disposition'] = 'attachment; filename="Mark-sheet.csv"'
            return response'''

    messages.info(request,"Please login with proper Details")
    return redirect('/')