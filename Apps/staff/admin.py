from django.contrib import admin
from .models import TEACHER, Transfer,Promotion
# Register your models here.

@admin.register(TEACHER)
class TeacherAdmin(admin.ModelAdmin):
    
    list_display =('school', 'post', 'name', 'fname', 'g_fund_no', 'salary', 'cnic', 'image', 'address', 'dob', 'personal_no', 'gender')


@admin.register(Transfer)
class TeacherAdmin(admin.ModelAdmin):
    
    list_display =('teacher', 'fromSchool', 'toSchool', 'date')


@admin.register(Promotion)
class TeacherAdmin(admin.ModelAdmin):
    
    list_display = ('teacher', 'fromPost', 'toPost', 'date')