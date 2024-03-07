from django.urls import path

from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('loginadmin/',views.loginadmin,name='loginadmin'),

    path('doclogin/',views.doclogin,name='doclogin'),
    path('viewpatients/',views.viewpatients,name='viewpatients'),
    path('doctorregistration/',views.doctorregistration,name='doctorregistration'),
    path('docpatients/',views.docpatients,name='docpatients'),
    path('docappointments/',views.docappointments,name='docappointments'),
    path('acceptappointment/<int:id>/',views.acceptappointment,name='acceptappointment'),
    path('appointmentstatus/',views.appointmentstatus,name='appointmentstatus'),
    path('generatecertificate/<int:id>/<str:patientname>/<str:patientemail>',views.generatecertificate,name='generatecertificate'),
    path('fileupload/',views.fileupload,name='fileupload'),
    path('myreport/',views.myreport,name='myreport'),
    path('adminlogout',views.adminlogout,name='adminlogout'),

    path('diseaseinfo/',views.diseaseinfo,name='diseaseinfo'),
    path('patientlogout/',views.patientlogout,name='patientlogout'),
    path('doclogout/',views.doclogout,name='doclogout'),




    path('patientregistration/',views.patientregistration,name='patientregistration'),
    path('patientlogin/',views.patientlogin,name='patientlogin'),
    path('applytest/<str:val1>/<str:val2>',views.applytest,name='applytest'),
    path('patientreport/',views.patientreport,name='patientreport'),
    path('appointmentbooking',views.appointmentbooking,name='appointmentbooking'),
]