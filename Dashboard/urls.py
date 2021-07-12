from django.urls import path
from . import views

urlpatterns=[
path("",views.dashboard,name="Dashboard"),
path("export/",views.export, name="export"),

]