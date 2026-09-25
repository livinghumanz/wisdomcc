from django.contrib import admin

from .models import (
    Attendance, Course, FeeRecord, Mark, MarkEntry, Staff, Student, Subject,
)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['regnum', 'name', 'std', 'branch', 'active_status', 'team', 'school']
    list_filter = ['active_status', 'branch', 'std', 'curriculum', 'team', 'category']
    search_fields = ['regnum', 'name', 'school', 'fname', 'mname', 'aadhar']
    ordering = ['name']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    search_fields = ['name']


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['empid', 'name']
    search_fields = ['empid', 'name']


@admin.register(MarkEntry)
class MarkEntryAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'exam_type', 'examdate', 'mark', 'out_of', 'faculty']
    list_filter = ['exam_type', 'subject', 'faculty', 'examdate']
    search_fields = ['student__regnum', 'student__name']
    autocomplete_fields = ['student', 'subject', 'faculty']
    date_hierarchy = 'examdate'


@admin.register(FeeRecord)
class FeeRecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'academic_year', 'fee_amount', 'paid_amount', 'updated_on']
    list_filter = ['academic_year']
    search_fields = ['student__regnum', 'student__name']
    autocomplete_fields = ['student']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['studentid', 'edate', 'status', 'late']
    list_filter = ['status', 'edate']
    search_fields = ['studentid__regnum', 'studentid__name']
    date_hierarchy = 'edate'


admin.site.register(Course)
admin.site.register(Mark)

admin.site.site_header = 'Wisdom Group — Django Admin'
admin.site.site_title = 'Wisdom Group'
admin.site.index_title = 'Data administration'
