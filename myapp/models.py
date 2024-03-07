from django.db import models

# Create your models here.
class patientdetails(models.Model):
    slno=models.IntegerField()
    name=models.CharField(max_length=100)
    age=models.CharField(max_length=100)
    email=models.EmailField(primary_key="True",max_length=100)
    Aadharno=models.CharField(max_length=100,unique='True')
    password=models.CharField(max_length=100)
    contact=models.CharField(max_length=100,default='')
    address=models.CharField(max_length=100,default='')
    Status=models.CharField(max_length=100,default='pending')



class docrequest(models.Model):
    Id=models.IntegerField()
    name=models.CharField(max_length=100)
    age=models.CharField(max_length=100)
    email=models.EmailField(primary_key="True",max_length=100)
    Aadharno = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    Status = models.CharField(max_length=100, default='Pending')


class reportsupload(models.Model):

    fever=models.CharField(max_length=100)
    cough=models.CharField(max_length=100)
    throat=models.CharField(max_length=100)
    breath=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    smoking=models.CharField(max_length=100)
    alcohol=models.CharField(max_length=100)
    saltdiet=models.CharField(max_length=100)
    fatdiet=models.CharField(max_length=100)
    exercise=models.CharField(max_length=100)
    cholestrol=models.CharField(max_length=100)
    bp=models.CharField(max_length=100)
    sugar=models.CharField(max_length=100)
    patientemail=models.CharField(max_length=100)


class doctorregistration(models.Model):
    hospitalname=models.CharField(max_length=100)
    doctorname=models.CharField(max_length=100)
    doctoremail=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    status=models.CharField(max_length=10,default='pending')


class appointment(models.Model):
    hospitalname=models.CharField(max_length=100)
    vaccinename=models.CharField(max_length=100)
    date=models.DateField()
    patientname=models.CharField(max_length=100)
    patientemail=models.CharField(max_length=100)
    doctorname=models.CharField(max_length=100)
    status=models.CharField(max_length=100,default='pending')

class medicalreport(models.Model):
    title=models.CharField(max_length=100)
    file=models.FileField()
    Filedata=models.BinaryField()
    Dataone=models.BinaryField()
    Datatwo=models.BinaryField()
    Hash1=models.CharField(max_length=100)
    Hash2=models.CharField(max_length=100)




