from django.contrib import admin
from .models import *

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'type', 'branch')
    list_filter = ('type', 'branch')
    search_fields = ('username', 'email')

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city')
    search_fields = ('name', 'address')

@admin.register(LessonSchedule)
class LessonScheduleAdmin(admin.ModelAdmin):
    list_display = ('group', 'days_of_week', 'start_time', 'end_time')
    list_filter = ('group',)
    search_fields = ('group__name',)

@admin.register(WorkSchedule)
class WorkSchedule(admin.ModelAdmin):
    list_display = ('teacher', 'days_of_week', 'start_time', 'end_time')
    list_filter = ('teacher',)
    search_fields = ('teacher__name',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'status', 'start_date', 'end_date', 'max_students')
    list_filter = ('branch', 'status')
    search_fields = ('name',)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'branch', 'group', 'status', 'salary_rate', 'start_date', 'next_payment_date')
    list_filter = ('branch', 'group', 'status')
    search_fields = ('name', 'surname')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'branch', 'group', 'status', 'payment', 'next_payment_date', 'study_start_date')
    list_filter = ('branch', 'group', 'status')
    search_fields = ('name', 'surname')

@admin.register(FinanceRecord)
class FinanceRecordAdmin(admin.ModelAdmin):
    list_display = ('type', 'amount', 'description', 'date')
    list_filter = ('type',)
    search_fields = ('description',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'date')
    search_fields = ('student__name', 'lesson__group__name', 'date')
    list_filter = ('date', 'lesson')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('group', 'date', 'time')
    search_fields = ('group__name', 'date__name', 'time')