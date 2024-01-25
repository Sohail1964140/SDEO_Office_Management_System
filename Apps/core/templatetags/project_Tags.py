from django import template

register = template.Library()
from Apps.core.models import CLASS_CHOICES
from Apps.monthlyEntry.models import SchoolBuilding
from django.contrib.auth import get_user_model
from Apps.schools.models import SCHOOL
from Apps.monthlyEntry.models import MonthlyRecord
from datetime import datetime

User = get_user_model()

"""
FILTERS
"""
@register.filter(name="make_list")
def make_list(value):
    return [str(x) for x in range(1, value + 1)]

months_in_order = { 1: "January",2: "February",3: "March", 4: "April",5: "May", 6: "June",
    7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
}

@register.filter(name="get_month_from_number")
def get_month_from_number(number):
    if number:
        return months_in_order[number]
    return "No Data yet"

@register.filter
def get_class_name(index):
    return CLASS_CHOICES[int(index)-1][1]


@register.filter
def isMonthEmpty(record):
    
    if record is not None:
        if record.teachersRecords.all():
            return False
        
        if SchoolBuilding.objects.filter(record=record).exists():
            return False
        
        if record.staffs.all():
            return False
        
        if record.studentStrength.all():
            return False
        
        if record.stock.all():
            return False
    
    return True




"""
SIMPLE TAGES
"""
@register.simple_tag
def get_record_id(recordList, year, m):
    return recordList[f'{year}-{m}']


@register.filter
def getValue(teacher, column):
    
    return teacher[column]



#  Authentication Tags
@register.filter
def hasPerm(user: User, perm: str)->bool:
    return user.has_perm(perm)


@register.filter
def is_added(id:int)->bool:
    
    return MonthlyRecord.objects.filter(school__pk=id,date__year=datetime.today().year, date__month=datetime.today().month).exists()
@register.filter
def YesNo(yes:bool)->str:
    return "Yes" if yes else "No"