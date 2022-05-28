from django.shortcuts import redirect, render
from django.http import HttpResponse, request, HttpResponseRedirect
from Dashboard.models import Staff
from home.models import Admision,Fupload
from django.template.defaulttags import register
from datetime import date
from django.contrib import messages
def HomeIndex(request):
    #return HttpResponse("Hello world!")
    return render(request,'home/index.html')

def about(request):
    return render(request,'home/Wabout.html')

def course_service(request):
    if request.method =='POST':
        # create a form instance and populate it with data from the request:
        f_data=request.POST
        Sname = f_data['Sname']
        school = f_data['school']
        contact = f_data['contact']
        Sclass = f_data['Sclass']
        mailid = f_data['admit-mail']
        wlocation = f_data['location']
        scourse = f_data['Scourse']
        #data=('Name:{0} School: {1} contact: {2} Sclass:{3} Mail-id: {4} Location : {5} '
        #.format(Sname,school,contact,Sclass,mailid,wlocation))
        admit=Admision.objects.create(sname=Sname,school=school,contact=contact,ystudy=Sclass,mailid=mailid,slocation=wlocation,scourse=scourse)
        #print(admit)
        return render(request,'home/Wcourses_service.html',{'result':'1','data':admit})
    return render(request,'home/Wcourses_service.html')

def gallery(request):
    return render(request,'home/WGallery.html')

def Faculty_portal(request):
    if request.method =='POST':
        Fid = request.POST['Fid']
        Fname = request.POST['Fname']
        upload_content = request.POST['upload']
        #data = ('Faculty-id : {0}, Name: {1}, content: {2}'
        #    .format(Fid,Fname,upload_content))
        staffd= Staff.objects.all().filter(empid=Fid)
        
        if len(staffd)==1:
            #print(staffd[0].empid)
            #print(data)
            if upload_content == 'notes':
                if request.FILES:
                    upfile = request.FILES['notes-d0']
                    comment = request.POST['notesd1']
                    up = Fupload.objects.create(empid=staffd[0],mtype=upload_content,comment=comment,fdata=upfile)
                    #print("files received ==",upfile,comment)
            elif upload_content == 'attendance':
                if request.FILES:
                    upfile = request.FILES['attendance-d0']
                    comment = "Student attendance report"
                    up = Fupload.objects.create(empid=staffd[0],mtype=upload_content,comment=comment,fdata=upfile)
                    #print("files received ==",upfile,comment)
            elif upload_content == 'mark':
                if request.FILES:
                    upfile = request.FILES['mark-d0']
                    comment = "Student mark list"
                    up = Fupload.objects.create(empid=staffd[0],mtype=upload_content,comment=comment,fdata=upfile)
                    #print("files received ==",upfile,comment)
            
            messages.info(request,"We have received your upload successfully !")
            return redirect('Faculty-portal')
        
        messages.info(request,"Please use proper credentials as per register")
        return redirect('/')
            #render(request, 'home/WFaculty_portal.html')
    #messages.info(request,"Please use proper credentials as per register")
    return render(request, 'home/WFaculty_portal.html')

@register.filter
def get_range(value):
    return list(range(value))