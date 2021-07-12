from django.shortcuts import redirect, render
from django.http import HttpResponse, request, HttpResponseRedirect
from home.models import Admision
from django.template.defaulttags import register
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
        #data=('Name:{0} School: {1} contact: {2} Sclass:{3} Mail-id: {4} Location : {5} '
        #.format(Sname,school,contact,Sclass,mailid,wlocation))
        admit=Admision.objects.create(sname=Sname,school=school,contact=contact,ystudy=Sclass,mailid=mailid,slocation=wlocation)
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
        data = ('Faculty-id : {0}, Name: {1}, content: {2}'
            .format(Fid,Fname,upload_content))
        #print(data)
        #return HttpResponse(data)
        render(request, 'home/WFaculty_portal.html')

    return render(request, 'home/WFaculty_portal.html')

@register.filter
def get_range(value):
    return list(range(value))