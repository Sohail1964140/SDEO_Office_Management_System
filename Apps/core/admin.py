from django.contrib import admin
from .models import (CIRCLE, UC, VC, ITEM_CATEGORY, STOCK_ITEM, CLASS, POST)
# Register your models here.


@admin.register(CIRCLE)
class CircleAdmin(admin.ModelAdmin):
    
    list_display  = ['name']


@admin.register(UC)
class UCAdmin(admin.ModelAdmin):
    
    list_display  = ['name', 'circle']



@admin.register(VC)
class VCAdmin(admin.ModelAdmin):
    
    list_display  = ['name', 'uc']



@admin.register(CLASS)
class CLASSAdmin(admin.ModelAdmin):
    
    list_display  = ['name']


@admin.register(POST)
class POSTAdmin(admin.ModelAdmin):
    
    list_display  = ('name', 'bps')


@admin.register(ITEM_CATEGORY)
class ITEM_CATEGORYAdmin(admin.ModelAdmin):
    
    list_display  = ('name', )


@admin.register(STOCK_ITEM)
class STOCK_ITEMAdmin(admin.ModelAdmin):
    
    list_display  = ('name', 'category')