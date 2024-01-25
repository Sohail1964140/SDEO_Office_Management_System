from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.MonthlyRecord)
class RecordAdmin(admin.ModelAdmin):
    
    display_list =('date', 'school')
    



@admin.register(models.TeacherMonthlyEntry)
class TeacherMonthlyEntryAdmin(admin.ModelAdmin):
    
    list_display =('record', 'teacher', 'post', 'salary')
    
('monthlyEntry', 'qualification')


@admin.register(models.MonthlyRecordForProfessionalQualification)
class MonthlyRecordForProfessionalQualificationEntryAdmin(admin.ModelAdmin):
    
    list_display =('teacherEntry', 'qualification')


@admin.register(models.MonthlyRecordForAcademicQualification)
class MonthlyRecordForAcademicQualificationEntryAdmin(admin.ModelAdmin):
    
    list_display =('teacherEntry', 'qualification')
    

('record', 'post', 'sanctioned', 'filled', 'surplus')

@admin.register(models.StaffAvalibility)
class StaffAvalibilityAdmin(admin.ModelAdmin):
    
    list_display =('record', 'post', 'sanctioned', 'filled', 'surplus')
    
@admin.register(models.StudentStrength)
class StaffAvalibilityAdmin(admin.ModelAdmin):
    
    list_display = ('record', 'classID', 'boys', 'girls')