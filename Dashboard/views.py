import csv
from django.shortcuts import redirect, render
from django.http import HttpResponse, request, HttpResponseRedirect
from home.models import Admision
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
            self.lid = self.request.POST['loginid']
            self.passwd = self.request.POST['lpassword']
            self.user = auth.authenticate(username=self.lid.lower(),password=self.passwd)
            #data = "loginid: {0} <br> Password: {1}".format(lid,passwd)
            #return HttpResponse(data)
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
        writer.writerow(entry)
    
    response['Content-Disposition'] = 'attachment; filename="applications.csv"'
    return response