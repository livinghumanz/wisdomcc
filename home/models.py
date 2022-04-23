from django.db import models
from datetime import date,datetime
from Dashboard.models import Staff
from django.template.defaulttags import comment

# Create your models here.
class Admision(models.Model):
    sname = models.CharField(max_length=100)
    school = models.TextField()
    contact = models.BigIntegerField()
    slocation = models.CharField(max_length=20)
    ystudy = models.CharField(max_length=10)
    mailid = models.EmailField(max_length=100)
    
    def __str__(self):
        return '{0} from {1}'.format(self.sname,self.school)

class Fupload(models.Model):
    empid = models.ForeignKey(Staff,on_delete=models.DO_NOTHING)
    mtype = models.CharField(max_length=20)
    update = models.DateField(auto_now_add=True)
    comment = models.TextField()
    fdata = models.FileField(upload_to='uploadedfiles/facultyportal/%y/%m/%d/')

    def __str__(self) -> str:
        return '{0} uploaded {1} on {2}'.format(self.empid,self.mtype,self.update)