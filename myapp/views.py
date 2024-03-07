from django.shortcuts import render,redirect
from django.contrib import messages
import pandas as pd
import hashlib
from PIL import Image, ImageDraw, ImageFont
import os

from . models import appointment,reportsupload
from django.conf import settings
from django.core.mail import send_mail
from django.db import connection
cur=connection.cursor()
# Create your views here.



def index(request):
    return render(request,'index.html')


def about(request):
    return render(request,'about.html')

# admin session
def loginadmin(request):
    if request.method=="POST":
        name=request.POST['name']
        password=request.POST['password']
        print(name,password)
        if name =='admin' and password =='admin':
            return render(request,'adminhome.html')
        messages.error(request,'Admin Not Authenticated')
        return render(request,'admin.html')

    return render(request,'admin.html')


def successlogin(request):
    return render(request,'successlogin.html')






#Doctor Login
def doclogin(request):
    if request.method=="POST":
        Name=request.POST['name']
        Password=request.POST['password']
        request.session['docname']=Name
        request.session['Password']=Password
        sql = "select * from myapp_doctorregistration where doctorname='%s' and password='%s'" % (Name, Password)
        cur.execute(sql)
        data = cur.fetchall()
        connection.commit()
        data = [i for i in data]
        print(data)
        if data ==[]:
            msg="Invalid Credentials"
            return render(request, 'doclogin.html',{'msg':msg})
        print(data[0][2])
        print(data[0][4])
        if Name == data[0][2] and Password == data[0][4]:
            return render(request,'doctorhome.html')
        messages.error(request, 'Admin Not Authenticated')
        return render(request, 'doclogin.html')
    return render(request,'doclogin.html')

def docpatients(request):
    sql = "select id,patientemail,fever,cough,throat,breath,smoking,alcohol,cholestrol,bp,sugar from myapp_reportsupload"
    data = pd.read_sql_query(sql, connection)
    return render(request, 'docpatients.html', {'cols': data.columns.values, 'rows': data.values.tolist()})


def docappointments(request):
    # sql="select id,patientname,vaccinename,date,patientemail from myapp_appointment where doctorname='%s' and status='pending'"%(request.session['docname'])
    # cur.execute(sql)
    # connection.commit()
    # data=cur.fetchall()
    # print(data)
    # data=[j for i in data for j in i]
    data = appointment.objects.filter(doctorname=request.session['docname'],status='pending')
    return render(request,'docappointments.html',{'data':data})


def acceptappointment(request,id):
    print('----------',id)
    x=str(id)
    sql="update myapp_appointment set status='accepted' where id=%s and status='pending'"
    val=(x)
    cur.execute(sql,val)
    connection.commit()
    return redirect(docappointments)

def diseaseinfo(request):
    # sql="select * from myapp_appointment where status='accepted' and doctorname=%s"
    # val=(request.session['docname'])
    # cur.execute(sql,val)
    # data=cur.fetchall()
    # connection.commit()
    # print(data)
    da=appointment.objects.filter(doctorname=request.session['docname'],status='accepted')
    return render(request,"diseaseinfo.html",{'da':da})


def generatecertificate(request,id,patientname,patientemail):
    x=str(id)
    request.session['fileid']=x
    print(patientname)
    request.session['username'] = patientname
    print(patientemail)

    request.session['patientemail'] = patientemail
    sql="select * from myapp_appointment where id=%s"
    val=(x)
    cur.execute(sql,val)
    data=cur.fetchall()
    connection.commit()
    content=data[0]
    print(content)
    content=str(content)
    import pathlib
    new_dir_name = patientname
    new_dir = pathlib.Path('myproject/uploadfiles/', new_dir_name)
    new_dir.mkdir(parents=True, exist_ok=True)
    # You have to make a file inside the new directory
    new_file = new_dir / 'myfile.txt'
    new_file.write_text(content)

    subject = 'Vaccine Booking Management System using Blokchain'
    message = f"Hi {request.session['username']}"
    content = 'Your medical report upoloaded successfully.'
    m1 = "This message is automatic generated so dont reply to this Mail"
    m2 = "Thanking you"
    m3 = "Regards"
    m4 = "ADMIN."
    print(message)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [request.session['patientemail']]
    print(recipient_list)
    text = message + '\n' + content + '\n' + m1 + '\n' + m2 + '\n' + m3 + '\n' + m4
    send_mail(subject, text, email_from, recipient_list, fail_silently=False, )

    return render(request,'upload.html')


def fileupload(request):
    if request.method=="POST":
        file=request.FILES['files']
        print(file)
        x=file.read()
        datalen = int(len(x) / 2)
        print(datalen, len(x))
        g = 0
        a = ''
        b = ''
        c = ''
        for i in range(0, 2):
            if i == 0:
                a = x[g: datalen:1]
                a = a.decode('utf-8')
                print(a)
                result = hashlib.sha1(a.encode())
                hash1 = result.hexdigest()
                print(hash1)
                print("===================================")
                # result = hashlib.sha1(a.encode())
                # hash1 = result.hexdigest()
                # print(hash1)
                print("++++++++++++++++++++++++++")
                # print(g)
                # print(len(data))
                # b = data[g: len(data):1]
                # print(c)

                print(g)
                print(len(x))
                c = x[datalen: len(x):1]
                c = c.decode('utf-8')
                print(c)

                result = hashlib.sha1(c.encode())
                hash2 = result.hexdigest()
                print(hash2)


                # val=(file,file,x,a,c,hash1,hash2)
                # cur.execute(sql,val)
                # connection.commit()
                subject = 'Vaccine Booking Management System using Blockchain'
                message = f"Hi {request.session['username']}"
                content = 'your keys to decrypt file hash1 : {} and hash2 : {}'.format(hash1,hash2)
                m1 = "This message is automatic generated so dont reply to this Mail"
                m2 = "Thanking you"
                m3 = "Regards"
                m4 = "ADMIN."
                print(message)
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.session['patientemail']]
                print(recipient_list)
                text = message + '\n' + content + '\n' + m1 + '\n' + m2 + '\n' + m3 + '\n' + m4
                send_mail(subject, text, email_from, recipient_list, fail_silently=False, )
                new_file = 'myfile.txt'

                sql = "insert into myapp_medicalreport(title,file,Filedata,Dataone,Datatwo,Hash1,Hash2)values(%s,%s,AES_ENCRYPT(%s,'keys'),AES_ENCRYPT(%s,'keys'),AES_ENCRYPT(%s,'keys'),%s,%s)"
                val = (new_file, new_file, x, a, c, hash1, hash2)
                cur.execute(sql, val)
                connection.commit()



    return render(request,'upload.html')

def myreport(request):
    if request.method=="POST":
        hashone=request.POST['hashone']
        hashtwo=request.POST['hashtwo']
        print("888888888888888888")
        sql="select DISTINCT AES_DECRYPT(Filedata,'keys') from myapp_medicalreport where Hash1=%s and Hash2=%s"
        val=(hashone,hashtwo)
        cur.execute(sql,val)
        data = cur.fetchall()
        data=list((data))
        print(data)
        x=data[0][0]
        data=x.decode()
        return render(request, 'viewdata.html',{'data':data})
    return render(request,'hashcodes.html')



def viewpatients(request):
    # sql="select id,patientemail,fever,gender,smoking,alcohol,Covid from myapp_reportsupload"
    # data=pd.read_sql_query(sql,connection)
    # , {'cols': data.columns.values, 'rows': data.values.tolist()},
    info=reportsupload.objects.all()
    return render(request,'viewpatients.html',{'info':info})



def doctorregistration(request):
    if request.method=='POST':
        hospitalname=request.POST['hospitalname']
        doctorname=request.POST['doctorname']
        doctoremail=request.POST['doctoremail']
        password=request.POST['password']
        conpassword=request.POST['conpassword']
        if password == conpassword:
            sql="select * from myapp_doctorregistration where doctorname=%s and doctoremail=%s"
            val=(doctorname,doctoremail)
            cur.execute(sql,val)
            data=cur.fetchall()
            connection.commit()

            data=[j for i in data for j in i ]
            print(data)

            if data==[] or doctorname not in data[2] and doctoremail not in data[3]:
                status='pending'
                sql="insert into myapp_doctorregistration (hospitalname,doctorname,doctoremail,password,status) values(%s,%s,%s,%s,%s)"
                val=(hospitalname,doctorname,doctoremail,password,status)
                cur.execute(sql,val)
                connection.commit()
                subject = 'Vaccine Booking Management System using Blockchain'
                message = f'Hi {doctorname}'
                content = 'Your Registartion is successfully done by admin.'
                m1 = "This message is automatic generated so dont reply to this Mail"
                m2 = "Thanking you"
                m3 = "Regards"
                m4 = "ADMIN."
                print(message)
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [doctoremail]
                print(recipient_list)
                text = message + '\n' + content + '\n' + m1 + '\n' + m2 + '\n' + m3 + '\n' + m4
                send_mail(subject, text, email_from, recipient_list, fail_silently=False, )
                msg="Doctor Registration completed successfuly "
                return render(request, 'doctorregistration.html',{'msg':msg})

            msg="Registering an Existing Details"
            return render(request, 'doctorregistration.html', {'msg': msg})


    return render(request,'doctorregistration.html')


def patientregistration(request):
    if request.method=='POST':
        name=request.POST['name']
        age=request.POST['age']
        email=request.POST['email']
        Aadharno=request.POST['Aadharno']
        password=request.POST['password']
        conpassword=request.POST['conpassword']
        contact=request.POST['contact']
        address=request.POST['address']
        if password == conpassword :
            sql="select email from myapp_patientdetails where name=%s and email=%s"
            val=(name,email)
            cur.execute(sql,val)
            data=cur.fetchall()
            connection.commit()
            data=[j for i in data for j in i]
            if data ==[]:
                Status='pending'
                sql="insert into myapp_patientdetails(name,age,email,Aadharno,password,contact,address,Status) values (%s,%s,%s,%s,%s,%s,%s,%s)"
                val=(name,age,email,Aadharno,password,contact,address,Status)
                cur.execute(sql,val)
                connection.commit()

                msg="Account created Successully"
                return render(request,'patientregistration.html',{'msg':msg})
            msg="Details already Exists"
            return render(request, 'patientregistration.html',{'msg':msg})
        msg = "Password not Matching"
        return render(request, 'patientregistration.html', {'msg': msg})
    return render(request,'patientregistration.html')



def patientlogin(request):
    if request.method=='POST':
        name=request.POST['name']
        request.session['patientname']=name
        password=request.POST['password']
        sql="select * from myapp_patientdetails where name='%s' and password='%s'"%(name,password)
        cur.execute(sql)
        data=cur.fetchall()
        connection.commit()
        data=[i for i in data]

        if data !=[]:
            print(data[0][3])
            request.session['patientemail']=data[0][3]
            return render(request,'patienthome.html',{'data':data})
        msg="Invalid credentials"
        return render(request, 'patientlogin.html',{'msg':msg})
    return render(request,'patientlogin.html')

def applytest(request,val1,val2):
    print(val1)
    print(val2)
    request.session['patientname']=val1
    request.session['patientemail']=val2
    sql="select * from myapp_patientdetails where name=%s and email=%s"
    val=(val1,val2)
    cur.execute(sql,val)
    data=cur.fetchall()
    connection.commit()
    print(data)
    if data !=[]:
        name=data[0][1]
        age=data[0][2]
        email=data[0][3]
        aadhar=data[0][4]
        address=data[0][7]
        contact=data[0][6]
        sql = "select * from myapp_docrequest where name=%s and email=%s"
        val = (val1, val2)
        cur.execute(sql, val)
        data = cur.fetchall()
        connection.commit()

        if data ==[]:
            sql="insert into myapp_docrequest (name,age,email,Aadharno,Contact,Address) values (%s,%s,%s,%s,%s,%s)"
            val=(name,age,email,aadhar,contact,address)
            cur.execute(sql,val)
            connection.commit()
            msg = "Request sent successfuly"
            return render(request,'applytest.html',{'msg':msg})
        return render(request, 'applytest.html')
    return render(request, 'applytest.html')

def patientreport(request):
    fever=request.POST['fever']
    cough=request.POST['cough']
    throat=request.POST['throat']
    breath=request.POST['breath']

    gender=request.POST['gender']
    smoking=request.POST['smoking']
    alcohol=request.POST['alcohol']
    saltdiet=request.POST['saltdiet']
    fatdiet=request.POST['fatdiet']
    exercise=request.POST['exercise']
    cholestrol=request.POST['cholestrol']
    bp=request.POST['bp']
    sugar=request.POST['sugar']
    if fever != 'null' or cough !='null' or throat !='null' or breath !='null' or gender != 'null' or smoking != 'null' or alcohol !='null' or saltdiet != 'null' or fatdiet != 'null' or exercise != 'null' or cholestrol != 'null' or bp !='null' or sugar !='null':
        sql="insert into myapp_reportsupload(fever,cough,throat,breath,gender,smoking,alcohol,saltdiet,fatdiet,exercise,cholestrol,bp,sugar,patientemail)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val=(fever,cough,throat,breath,gender,smoking,alcohol,saltdiet,fatdiet,exercise,cholestrol,bp,sugar,request.session['patientemail'])
        cur.execute(sql,val)
        connection.commit()
        val1=request.session['patientname']
        val2=request.session['patientemail']
        return render(request,"appointment.html",{'val1':val1})
    return redirect('/patientreport/')


def appointmentbooking(request):
    sql="select distinct hospitalname from myapp_doctorregistration"
    cur.execute(sql)
    data=cur.fetchall()
    connection.commit()

    data=[j for i in data for j in i ]

    if request.method=='POST':

        hospitalname=request.POST['hospitalname']
        vaccinename=request.POST['vaccinename']
        date=request.POST['date']

        sql="select patientname,patientemail from myapp_appointment where patientname=%s and patientemail=%s"
        val=(request.session['patientname'],request.session['patientemail'])
        cur.execute(sql,val)
        data=cur.fetchall()
        connection.commit()
        data=[j for i in data for j in i]
        data=[k for k in data]
        print(data)
        if request.session['patientname'] in data and request.session['patientemail'] in data:
            msg="your request sended already please wait....."
            return render(request, 'appointmentbooking.html', {'msg': msg})
        else:
            status='pending'
            sql="insert into myapp_appointment(hospitalname,vaccinename,date,patientname,patientemail,doctorname,status) values(%s,%s,%s,%s,%s,%s,%s)"
            val=(hospitalname,vaccinename,date,request.session['patientname'],request.session['patientemail'],request.session['docname'],status)
            cur.execute(sql,val)
            connection.commit()
            msg="Your appointment request sent Succesfuly"
            return render(request, 'appointmentbooking.html', {'msg': msg })
    return render(request,'appointmentbooking.html',{'data':data})


def appointmentstatus(request):

    # query="select * from myapp_appointment where patientemail=%s and status=accepted"
    # values=(request.session['patientemail'])
    # cur.execute(query, values)
    # info = cur.fetchall()
    # connection.commit()
    info=appointment.objects.filter(patientemail=request.session['patientemail'],status='accepted')
    print(info)
    return render(request,'myappointment.html',{'data':info})


def patientlogout(request):
    return redirect(index)




def doclogout(request):
    return redirect(index)

def adminlogout(request):
    return redirect(index)
