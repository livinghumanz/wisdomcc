from datetime import datetime
from django.db import models

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
