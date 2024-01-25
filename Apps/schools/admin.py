from django.contrib import admin
from .models import SCHOOL
# Register your models here.


@admin.register(SCHOOL)
class SchoolAdmin(admin.ModelAdmin):
    
    list_display = ('uc', 'name', 'emis', 'latitude','langitude', 'ddo', 'yearOfConstruction', 'slug')
    