import csv
from django.shortcuts import redirect, render
from django.http import HttpResponse, request, HttpResponseRedirect
from home.models import Admision,Fupload
from .models import *
from django.contrib import messages,auth
# Create your views here.
auser:object
class authencateuser:
    def __init__(self,request):
        self.user=False
        self.request = request

    def userdashboard(self):
        if self.user is not None:
            admision_list = Admision.objects.all()
            context = {
                'admision_list':admision_list
            }
            return render(self.request,'dashboard/dashboard.html',context)
        else:
            messages.info(self.request,"Please login with proper Details")
            return redirect('/')

    def authuser(self):
        if self.request.method == 'POST':
            if(self.request.POST['ltype'] == 'admin'):
                self.lid = self.request.POST['loginid']
                self.passwd = self.request.POST['lpassword']
                self.user = auth.authenticate(username=self.lid.lower(),password=self.passwd)
                #data = "loginid: {0} <br> Password: {1}".format(lid,passwd)
                #return HttpResponse(data)
                return self.userdashboard()
            elif self.request.POST['ltype'] == 'student':
                self.lid = self.request.POST['loginid']
                self.passwd = self.request.POST['lpassword']
                sob = Student.objects.all().filter(regnum=self.lid,password=self.passwd)
                #if(self.lid == )
                #print(type(Mark.objects.all().filter(studentid__regnum = self.lid)))
                if len(sob) == 1:
                    notes = Fupload.objects.all().filter(mtype='notes')
                    return render(self.request,"dashboard/dashboard_user.html",{'image':sob[0].image.url,'timetable':sob[0].timetable.url,'name':sob[0].name.split()[0],'sdata':sob,'notes':notes})
                self.user = None
                return self.userdashboard()

        
        else:
            messages.info(self.request,"please login to access.")
            return redirect('/')
            #return HttpResponse("hello")
            

def dashboard(request):
    #return HttpResponse("Hello world!")
    auser = authencateuser(request)
    return auser.authuser()

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

def reportdown(request, stid):
    if request.method == 'POST':
        regno = request.POST['regno']
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
            response= HttpResponse(content_type = 'text/csv')
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
            return response

    messages.info(request,"Please login with proper Details")
    return redirect('/')