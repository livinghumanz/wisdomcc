from django.db import models

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