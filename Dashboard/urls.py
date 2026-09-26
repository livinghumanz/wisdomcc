from django.urls import path

from . import views
from . import admin_views

urlpatterns = [
    path("", views.dashboard, name="Dashboard"),
    path("logout/", views.logout_view, name="dashboard-logout"),
    path("export/", views.export, name="export"),

    # ---- admin portal ----
    path("admin/students/", admin_views.student_list, name="admin-students"),
    path("admin/students/new/", admin_views.student_form, name="admin-student-new"),
    path("admin/students/<str:regnum>/edit/", admin_views.student_form, name="admin-student-edit"),
    path("admin/students/<str:regnum>/delete/", admin_views.student_delete, name="admin-student-delete"),
    path("admin/marks/", admin_views.marks_screen, name="admin-marks"),
    path("admin/marks/<str:regnum>/growth-card/", admin_views.growth_card, name="admin-growth-card"),
    path("admin/attendance/", admin_views.attendance_register, name="admin-attendance"),
    path("admin/fees/", admin_views.fee_sheet, name="admin-fees"),
    path("admin/faculty-analysis/", admin_views.faculty_analysis, name="admin-faculty-analysis"),

    path('<str:stid>', views.reportdown, name='report'),
]
