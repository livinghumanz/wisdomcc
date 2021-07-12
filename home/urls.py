from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns=[
path("",views.HomeIndex,name="Home"),
path("Gallery/",views.gallery,name="gallery"),
path("About/",views.about,name="about"),
path("Course-Services/",views.course_service,name="course"),
#path("Dashboard/",views.login,name="login"),
path("Faculty-portal/",views.Faculty_portal,name="Faculty-portal"),
]