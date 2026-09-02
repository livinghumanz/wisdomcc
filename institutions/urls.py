from django.urls import path

from . import views

urlpatterns = [
    path('', views.preschool_home, name='preschool-home'),
]
