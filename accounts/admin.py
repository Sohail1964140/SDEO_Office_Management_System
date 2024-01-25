from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
# Register your models here.

USER  = get_user_model()
@admin.register(USER)
class CustomUserAdmin(UserAdmin):  

    model = USER  

    list_display = ('email', 'is_staff', 'is_active','image')  
    list_filter = ('email', 'is_staff', 'is_active',)  
    fieldsets = (  
        (None, {'fields': ('email', 'password')}),  
        ('Personal Information', {'fields':('first_name','last_name','date_joined', 'image')}),
        ('Permissions', {'fields': ('groups','user_permissions','is_staff', 'is_active','is_superuser')}),  
    )  
    add_fieldsets = (  
        (None, {  
            'classes': ('wide',),  
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}  
        ),  
    )  
    search_fields = ('email',)  
    ordering = ('email',)  
    filter_horizontal = ()