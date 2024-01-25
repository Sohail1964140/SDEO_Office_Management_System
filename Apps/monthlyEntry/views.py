from django.shortcuts import render,redirect, HttpResponse, get_object_or_404
from .models import (SchoolBuilding, SchoolStock, StaffAvalibility,
                     MonthlyRecord, TeacherMonthlyEntry, StudentStrength,
                     MonthlyRecordForProfessionalQualification,
                     MonthlyRecordForAcademicQualification
                     ,PTC_Information
                     )
from .forms import (SchoolBuildingForm, 
                    SchoolStockForm, 
                    StaffAvalibilityForm,
                    TeacherMonthlyEntryForm,
                    StudentStrengthEntryForm, PTC_InformationForm
                    )
from Apps.schools.models import SCHOOL
from django.views.generic import ListView
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from render_block import render_block_to_string
from django.core.paginator import Paginator
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.db import transaction
import json
from django.views import View
from django_htmx.http import HttpResponseClientRedirect
from django.urls import reverse_lazy as _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from Apps.core.models import hx_Redirect, POST, CLASS_CHOICES, STOCK_ITEM
from django.views.generic import DetailView
from time import sleep
from django.template.loader import get_template, render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.urls import reverse_lazy
# from formtools.wizard.views import SessionWizardView


# Create your views here.

def get_template(request, name, path=""):
    
    template = f'Entry/{path}/{name}.html'
    
    if request.htmx:
        
        template = f'Entry/{path}/partials/{name}.html'
    
    return template


def get_data_for_radioButton(obj):
    data = [
        {'id':'id_boundryWall','val':obj.boundryWall},
        {'id':'id_playGroud','val':obj.playGroud},
        {'id':'id_scienceLaboratory','val':obj.scienceLaboratory},
        {'id':'id_computerlaboratory','val':obj.computerLaboratory},
        {'id':'id_electricSuply','val':obj.electricSuply},
        {'id':'id_internalElectrification','val':obj.internalElectrification},
        {'id':'id_waterSource ','val':obj.waterSource},
    ]
    return data

def get_redirect_url(record: MonthlyRecord)-> dict:
    
    
    if not TeacherMonthlyEntry.objects.filter(record=record).exists():

        return {'url': 'entry:teacherMonthlyAdd'}
    
    if not SchoolBuilding.objects.filter(record=record).exists():
        
        return {'url':'entry:buildingAdd'}
    
    if not StaffAvalibility.objects.filter(record=record).exists():
        
        return {'url':'entry:staffAvalibilityAdd'}
    
    if not StudentStrength.objects.filter(record=record).exists():
        
        return {'url': 'entry:studentStrengthAdd'}
    
    if not PTC_Information.objects.filter(record=record).exists():
    
        return {'url': 'entry:ptcInformationAdd'}

    if not SchoolStock.objects.filter(record=record).exists():
        
        return {'url': 'entry:schoolStockAdd'}

    return {'url': None}

"""
=== ========== === ========== === ===== Setting for Monthly Entry  ===== === ========== === ==========
"""

class SettingForMonthlyEntryView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        template = get_template(request, 'setting', path="setting")
        context = {
            'emiss': SCHOOL.objects.values_list('emis', flat=True)
        }
        
        
        return render(request, template, context)
    
    def post(self, request):
        
        emis = request.POST.get('emis')
        date = datetime.strptime(request.POST.get('date'), "%m/%d/%Y")
        csvFile = request.FILES.get('datafile')
        isCsv = request.POST.get('isCsv')
       
        
        school = SCHOOL.objects.filter(emis=emis).first()
        # Check if the school exsit or not
        if not school:
            
            messages.error(request, "School with this emis code dosn't exist")
            return hx_Redirect('entry:setting')
            
        record = MonthlyRecord.objects.filter(
                                            Q(date__year = date.year) & 
                                            Q(date__month=date.month) &
                                            Q(school__pk=school.pk)
                                              )

        if record.exists():
            
            url = get_redirect_url(record=record.first())['url']
            
            if url is None:
                    
                messages.info(request, "Entry for this month is already done")
                return hx_Redirect("entry:setting")
            
            request.session['record'] = record.first().pk
            return HttpResponseClientRedirect(_(url))
            
            
        record = MonthlyRecord.objects.create(date=date, school=school)
       
        if isCsv:
            pass
        

        
        request.session['record'] = record.pk
        if "fromProfile" in request.session.keys():
            del request.session["fromProfile"]
            
        return HttpResponseClientRedirect(_("entry:teacherMonthlyAdd"))
        



"""
=== ========== === ========== === ===== Teacher Monthly Entry  ===== === ========== === ==========
"""


class TeacherMonthlyEntryView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        template = get_template(request, 'add', path="Teacher")
        
        record = MonthlyRecord.objects.get(pk=request.session['record'])
        btnText = "Submit form for all teachers"
        isSubmited = False
        
        if TeacherMonthlyEntry.objects.filter(record=record).exists():
            
            btnText = "Teacher form is  already sumbited"
            isSubmited = True
        
        context = {
            'btnText':btnText,
            'current':'1',
            'isSubmited': isSubmited
        }
        
        
        return render(request, template, context)
        
        
    
    def post(self, request):
        
        try:
            with transaction.atomic():

                record = MonthlyRecord.objects.get(pk=request.session['record'])
                
                for teacher in record.school.teachers.all():
                    
                    # Entry in TeacherMonthlyEntry
                    teacherEntry = TeacherMonthlyEntry.objects.create(
                        record=record, teacher=teacher, post=teacher.post, salary=teacher.salary,
                        dateOfTakingOverChargeOnPresentPost = teacher.dateOfTakingOverChargeOnPresentPost,
                        dateOfTakingOverChargeInPresentSchool = teacher.dateOfTakingOverChargeInPresentSchool
                        )
                    
                    # Entry for Proffessional Qualification
                    for qualification in teacher.Proffqualification.all():
                        MonthlyRecordForProfessionalQualification.objects.create(
                            teacherEntry=teacherEntry,qualification=qualification)
                    

                    # Entry for Accademic Qualification
                    for qualification in teacher.Accadqualification.all():
                        
                        MonthlyRecordForAcademicQualification.objects.create(
                            teacherEntry=teacherEntry,qualification=qualification)
                    
                messages.success(request, "Form for teachers is submited")
                return hx_Redirect("entry:teacherMonthlyAdd")
                    
        except:
            
            messages.error(request, "Operation failed Please try again")
            return hx_Redirect("entry:teacherMonthlyAdd")

class TeacherMonthlyEntryListView(LoginRequiredMixin,View):
    
    def get(self, request, id):
        
        template = get_template(request, 'list', path="Teacher")
        record = MonthlyRecord.objects.get(pk=id)
    
        return render(request, template, {'record': record})

@login_required
def delete_TeacherMonthlyEntry(request, pk):

    if request.method == "DELETE":
        record = MonthlyRecord.objects.get(pk=pk)
        
        record.teachersRecords.all().delete()
        
        messages.success(request,"Teacher  record deleted successfully")
        return hx_Redirect("entry:showRecordsFromSession")

    

"""
=== ========== === ========== === ===== School Building   ===== === ========== === ==========
"""
class SchoolBuildingMonthlyEntryView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        template = get_template(request, name='add', path="Building")
        record = MonthlyRecord.objects.get(pk=request.session['record'])
        nextDisabled = True
        form = SchoolBuildingForm()
        extra = []
        
        
        # Fill form
        if SchoolBuilding.objects.filter(record=record).exists():
            return hx_Redirect("entry:staffAvalibilityAdd")
            nextDisabled = False
            schoolBuilding = SchoolBuilding.objects.get(record=record)
            form= SchoolBuildingForm(instance=schoolBuilding)
            extra = get_data_for_radioButton(schoolBuilding)
        
        # Check Prv Record
        
        currentSchoolsRecord = MonthlyRecord.objects.filter(school=record.school).order_by("-date")
        
        if len(currentSchoolsRecord) > 1:
            currentSchoolsRecord = currentSchoolsRecord[1]
        else:
            currentSchoolsRecord = currentSchoolsRecord.first()
        prevRecord = False
        if currentSchoolsRecord.building.all().exists():
            prevRecord = True
        
        context = {
            'form': form,
            'current': '2',
            'nextDisabled': nextDisabled,
            'extra': extra,
            'prevRecord': prevRecord
        }
        
        return render(request, template, context)
        
        
    def post(self, request):
        
        template = get_template(request, name='add', path="Building")
        record = MonthlyRecord.objects.get(pk=request.session['record'])
        form = SchoolBuildingForm(data=request.POST)
        print(request.POST)
        if form.is_valid():
            
            buildingRecord = form.save(commit=False)
            buildingRecord.record = record
            buildingRecord.save()
            
            return hx_Redirect("entry:staffAvalibilityAdd")
       
        context = {
            'form': form,
            'current': '2',
            'nextDisabled': True
        }
       
        messages.error(request, "Please correct the error bellow")
        return render(request, template, context)

class SchoolBuildingView(LoginRequiredMixin, DetailView):
    model=MonthlyRecord
    context_object_name="record"
    def get_template_names(self, *args, **kwargs):
        return get_template(self.request, 'list', path="Building")
@login_required
def delete_building(request, pk):

    if request.method == "DELETE":
        record = MonthlyRecord.objects.get(pk=pk)
        record.building.delete()
        
        messages.success(request,"building record deleted successfully")
        return hx_Redirect("entry:showRecordsFromSession")
@login_required
def buildingRecord_fill_from_prev(request):
    
    template = get_template(request, name='add', path="Building")
    record = MonthlyRecord.objects.get(pk=request.session['record'])
    # get prev
    prevRecord = MonthlyRecord.objects.filter(school=record.school).order_by("-date")
    if len(prevRecord) > 1:
        prevRecord = prevRecord[1]
    else:
        prevRecord = prevRecord.first()
    
    form= SchoolBuildingForm()
    extra = []
    if 'prevMonth' in  request.GET.keys():
    
        if SchoolBuilding.objects.filter(record=prevRecord).exists():
            form= SchoolBuildingForm(instance=prevRecord.building.all().first())
            extra = get_data_for_radioButton(prevRecord.building.all().first())
   
    context =  {
        'form':form,
        'extra':extra
                }
    
    template = render_block_to_string(template, 'form',context)
    
    return HttpResponse(template)

"""
=== ========== === ========== === ===== Student Strength  ===== === ========== === ==========
"""

class StudentStrengthMonthlyEntryView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        template = get_template(request, name='add', path="StudentStrength")
        record = MonthlyRecord.objects.get(pk=request.session['record'])
        nextDisabled = True
        form = StudentStrengthEntryForm(record=record.pk)
        
        
        if StudentStrength.objects.filter(record=record).exists():
            
            if len(CLASS_CHOICES) == StudentStrength.objects.filter(record=record).count():
                
                nextDisabled = False
                return hx_Redirect("entry:ptcInformationAdd")

        currentStudentStrengthRecords = MonthlyRecord.objects.filter(school=record.school).order_by("-date")
       
        if len(currentStudentStrengthRecords) > 1:
           currentStudentStrengthRecords = currentStudentStrengthRecords[1]
        else:
           currentStudentStrengthRecords = currentStudentStrengthRecords.first()
        
        prevRecord = False
        
        if currentStudentStrengthRecords.studentStrength.all().exists():
            prevRecord = True
        
        context = {
            'form': form,
            'current':'4',
            'nextDisabled': nextDisabled,
            "prevRecord":prevRecord
        }
        
        return render(request, template, context)
        
        
    def post(self, request):
        
        template = get_template(request, name='add', path="StudentStrength")
        record = MonthlyRecord.objects.get(pk=request.session['record'])
        nextDisabled = True
        form = StudentStrengthEntryForm(data=request.POST)
        
        if form.is_valid():
            
            strength = form.save(commit=False)
            strength.record = record
            strength.save()
            
            form = StudentStrengthEntryForm(record=record.pk)
            messages.success(request, "data enter successfully")

            if StudentStrength.objects.filter(record=record).exists():
                if len(CLASS_CHOICES) == StudentStrength.objects.filter(record=record).count():
                    
                    return hx_Redirect("entry:ptcInformationAdd")

        else:
            messages.error(request, "Correct the error bellow")
           
            
        context = {
            'form': form,
            'current':'4',
            'nextDisabled': nextDisabled,
             "prevRecord":False
        }
        
        return render(request, template, context)

class StudentStrengthDetailView(LoginRequiredMixin,DetailView):
    model=MonthlyRecord
    context_object_name="record"
    def get_template_names(self, *args, **kwargs):
        return get_template(self.request, 'list', path="StudentStrength")
@login_required
def delete_StudentStrength(request, pk):

    if request.method == "DELETE":
        record = MonthlyRecord.objects.get(pk=pk)
        
        record.studentStrength.all().delete()
        
        messages.success(request,"Students  record deleted successfully")
        return hx_Redirect("entry:showRecordsFromSession")


class StudentStrengthSavePrev(LoginRequiredMixin,View):
    # ('record', 'classID', 'boys', 'girls', )
    @transaction.atomic
    def post(self , request):
        
        record = MonthlyRecord.objects.get(pk=request.session['record'])
        prevRecord = MonthlyRecord.objects.filter(school=record.school).order_by("-date")
        if len(prevRecord) > 1:
            prevRecord = prevRecord[1]
        else:
            prevRecord = prevRecord.first()
        
        for strength in prevRecord.studentStrength.all():
            
            StudentStrength.objects.create(
                record = record,
                classID=strength.classID,
                boys=strength.boys,
                girls=strength.girls,
            )
    
        return hx_Redirect("entry:ptcInformationAdd")




      
"""
=== ========== === ========== === ===== School Stock  ===== === ========== === ==========
"""

class SchoolStockMonthlyEntryView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        template = get_template(request, name='add', path="Stock")
        record = MonthlyRecord.objects.get(pk=request.session['record'])
        nextDisabled = True
        if SchoolStock.objects.filter(record=record).exists():
            
            if STOCK_ITEM.objects.all().count() == SchoolStock.objects.filter(record=record).count():
                
                nextDisabled = False
                return hx_Redirect("entry:setting")
                
                
        prevRecord = False
        
        pre_record = MonthlyRecord.objects.filter(school=record.school).order_by("-date")
        if len(pre_record) > 1:
            pre_record = pre_record[1]
        else:
            pre_record = pre_record.first()
            
        if pre_record.stock.all().exists():
            prevRecord = True
        context = {
            'form': SchoolStockForm(record=record.pk),
            'current':'6',
            'nextDisabled' :nextDisabled,
            'prevRecord':prevRecord
        }
        
        return render(request, template, context)
    
    def post(self, request):
        
        template = get_template(request, name='add', path="Stock")
        record = MonthlyRecord.objects.get(pk=request.session['record'])
        form = SchoolStockForm(data=request.POST)
        nextDisabled = True
        if form.is_valid():
            
            stock = form.save(commit=False)
            stock.record = record
            stock.save()
            form = SchoolStockForm(record=record.pk)

            if STOCK_ITEM.objects.all().count() == SchoolStock.objects.filter(record=record).count():
                
                messages.success(request, f"School Record for {record.date} has been successfully saved.")
                fromProfile = request.session.get('fromProfile', False)
                print(fromProfile)
                if not fromProfile:
                    return hx_Redirect("entry:setting")

                return HttpResponseClientRedirect(_('school:schoolProfile', kwargs={'slug': record.school.slug}))
           
            messages.success(request, "Success! The data has been entered successfully.")
        else:   
            messages.error(request, "Kindly note the error below and make the necessary corrections. Thank you!")
        
        
        context = {
            'form': form,
            'current':'5',
            'nextDisabled' :nextDisabled
        }
        return render(request, template, context)
        
class StockDetailView(LoginRequiredMixin,DetailView):
    model=MonthlyRecord
    context_object_name="record"
    
    def get_template_names(self, *args, **kwargs):
        return get_template(self.request, 'list', path="Stock") 
@login_required
def delete_Stock(request, pk):

    if request.method == "DELETE":
        record = MonthlyRecord.objects.get(pk=pk)
        
        record.stock.all().delete()
        
        messages.success(request,"Stock  record deleted successfully")
        return hx_Redirect("entry:showRecordsFromSession")

class SchoolStockMonthlyEntrySavePrev(LoginRequiredMixin,View):
# ('record', 'item', 'noOfItems', 'required', 'surplus', )
    @transaction.atomic
    def post(self , request):
        
        record = MonthlyRecord.objects.get(pk=request.session['record'])
        prevRecord = MonthlyRecord.objects.filter(school=record.school).order_by("-date")
        if len(prevRecord) > 1:
            prevRecord = prevRecord[1]
        else:
            prevRecord = prevRecord.first()
        
        for preStockRec in prevRecord.stock.all():
            
            SchoolStock.objects.create(
                record = record,
                item=preStockRec.item,
                noOfItems=preStockRec.noOfItems, 
                required=preStockRec.required, 
                surplus=preStockRec.surplus
            )
    
        messages.success(request, f"School Record for {record.date} has been successfully saved.")
        fromProfile = request.session.get('fromProfile', False)
        if not fromProfile:
            return hx_Redirect("entry:setting")

        return HttpResponseClientRedirect(_('school:schoolProfile', kwargs={'slug': record.school.slug}))
    





    
"""     
=== ========== === ========== === ===== Staff Avalibility ===== === ========== === ==========
"""


@login_required
def get_filled_staff(request):
    record = MonthlyRecord.objects.get(pk=request.session['record'])
    post = request.GET['post']
    if post =="":
        post = 0
    value = record.school.teachers.filter(post__id=post).count()
    template = get_template(request, name='filled', path="StaffAvalibility")
    return render(request,template,{'value': value} )
    
    
    

class StaffAvalibilityMonthlyEntryView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        template = get_template(request, name='add', path="StaffAvalibility")
        record = MonthlyRecord.objects.get(pk=request.session['record'])
        nextDisabled = True
        form = StaffAvalibilityForm(record=request.session['record'])
        
        if StaffAvalibility.objects.filter(record=record).exists():
            
            staffRecordCount = StaffAvalibility.objects.filter(record=record).count()
            postCount = POST.objects.all().count()

            if staffRecordCount == postCount:
                nextDisabled = False
                return hx_Redirect("entry:studentStrengthAdd")
            
        currentSchoolsRecord = MonthlyRecord.objects.filter(school=record.school).order_by("-date")
        if len(currentSchoolsRecord) > 1:
            currentSchoolsRecord = currentSchoolsRecord[1]
        else:
            currentSchoolsRecord = currentSchoolsRecord.first()
            
        prevRecord = False
        
        if currentSchoolsRecord.staffs.all().exists():
            prevRecord = True
            
        context = {
            'form': form,
            'nextDisabled': nextDisabled,
            'current':'3',
            'prevRecord':prevRecord,
        }
        
        return render(request, template, context)
    def post(self, request):
        
        record = MonthlyRecord.objects.get(pk=request.session['record'])
        template = get_template(request, name='add', path="StaffAvalibility")

        form = StaffAvalibilityForm(data=request.POST, record=request.session['record'])
        
        if form.is_valid():
            
            staff = form.save(commit=False)
            staff.record = record
            staff.save()
            form = StaffAvalibilityForm(record=request.session['record'])
            staffRecordCount = StaffAvalibility.objects.filter(record=record).count()
            postCount = POST.objects.all().count()
            
            if postCount == staffRecordCount:
                
                return hx_Redirect("entry:studentStrengthAdd")

            messages.success(request, "data enter successfully")
        else:
            
             messages.error(request, "Kindly note the error below and make the necessary corrections. Thank you!")
            
        
        context = {
            'form': form,
            'current': '3',
            'nextDisabled': True
        }
       
        return render(request, template, context)


class StaffAvalibilityDetailView(LoginRequiredMixin,DetailView):
    model=MonthlyRecord
    context_object_name="record"
    def get_template_names(self, *args, **kwargs):
        return get_template(self.request, 'list', path="StaffAvalibility")
    
@login_required
def delete_staff(request, pk):

    if request.method == "DELETE":
        record = MonthlyRecord.objects.get(pk=pk)
        
        record.staffs.all().delete()
        
        messages.success(request,"staff  record deleted successfully")
        return hx_Redirect("entry:showRecordsFromSession")


class StaffAvalibilitySavePrev(LoginRequiredMixin,View):
    # ('record', 'post', 'sanctioned', 'filled', 'surplus', )
    @transaction.atomic
    def post(self , request):
        
        record = MonthlyRecord.objects.get(pk=request.session['record'])
        prevRecord = MonthlyRecord.objects.filter(school=record.school).order_by("-date")
        if len(prevRecord) > 1:
            prevRecord = prevRecord[1]
        else:
            prevRecord = prevRecord.first()
        
        for preStaffRec in prevRecord.staffs.all():
            
            StaffAvalibility.objects.create(
                record = record,
                post=preStaffRec.post,
                sanctioned=preStaffRec.sanctioned, 
                filled=preStaffRec.filled, 
                surplus=preStaffRec.surplus
            )
    
        return hx_Redirect("entry:studentStrengthAdd")



"""
=== ========== === ========== === ===== SHOW RECORD ===== === ========== === ==========
"""
def get_year_months(records: MonthlyRecord):
    
    output = {}
    recordList = {}
    start = 0
    for record in records:
        if str(record.date.year) not in output:
            output[str(record.date.year)] = []
            for in_record in records[start: ]:
                
                if in_record.date.year == record.date.year:
                    output[str(record.date.year)].append(in_record.date.month)
                    recordList[f'{record.date.year}-{in_record.date.month}'] = in_record.pk
        start = start + 1
        
    return {'dates':output,'recordList':recordList}
                
class get_filter_template(View):
    
    def get(self, request):
        
        template = "Entry/filter.html"
        
        if request.htmx:
            template = "Entry/partials/filter.html"        
        
        context = {
            'emiss': SCHOOL.objects.values_list('emis', flat=True)
        }
        
        return render(request,template, context)
@login_required
def showRecordFromSession(request):
    
    template = "Entry/show.html"
    
    if request.htmx:
        template = "Entry/partials/show.html" 
        
    filter = json.loads(request.session['filter'])
    cbRange = filter.get('cbRange', None)
    cbYear = filter.get('cbYear', None)
    emis = filter.get("emis")
    date = datetime.strptime(filter.get("date"), "%m/%d/%Y")


    records = MonthlyRecord.objects.filter(Q(school__emis=emis) & Q(date__year=date.year) & Q(date__month=date.month))
    monthSearch = True
    if cbYear:
        records = MonthlyRecord.objects.filter(Q(school__emis=emis) & Q(date__year=date.year))
        monthSearch = False
    
    if cbRange:
        startDate = datetime.strptime(filter.get("from"), "%m/%d/%Y")
        endDate  = datetime.strptime(filter.get("to"), "%m/%d/%Y")
        monthSearch = False
        
        records = MonthlyRecord.objects.filter(Q(school__emis=emis) & Q(date__gte=startDate) & Q(date__lte=endDate))
    

    
    context = {
        'dates': get_year_months(records=records).get('dates'),
        'records':records,
        'recordList': get_year_months(records=records).get('recordList'),
        'monthSearch':monthSearch,
        'school': SCHOOL.objects.get(emis=emis)
    }
    
    return render(request,template ,context)

class ShowRecordsView(LoginRequiredMixin,View):
    
    def get(self, request, id=None):
        
        if id is None:
            template = "Entry/show.html"
            
            if request.htmx:
                template = "Entry/partials/show.html"        
            
            
                
            cbRange = request.GET.get('cbRange', None)
            cbYear = request.GET.get('cbYear', None)
            emis = request.GET.get("emis")
            date = datetime.strptime(request.GET.get("date"), "%m/%d/%Y")
                
            if not SCHOOL.objects.filter(emis=emis).exists():
                messages.warning(request,"Enter valid emis code")
                return hx_Redirect("entry:getFilterTemplate")
            
            
            
            records = MonthlyRecord.objects.filter(Q(school__emis=emis) & Q(date__year=date.year) & Q(date__month=date.month))
            monthSearch = True
            if cbYear:
                records = MonthlyRecord.objects.filter(Q(school__emis=emis) & Q(date__year=date.year))
                monthSearch = False
            
            if cbRange:
                startDate = datetime.strptime(request.GET.get("from"), "%m/%d/%Y")
                endDate  = datetime.strptime(request.GET.get("to"), "%m/%d/%Y")
                monthSearch = False
                
                records = MonthlyRecord.objects.filter(Q(school__emis=emis) & Q(date__gte=startDate) & Q(date__lte=endDate))
            

            
            context = {
                'dates': get_year_months(records=records).get('dates'),
                'records':records,
                'recordList': get_year_months(records=records).get('recordList'),
                'monthSearch':monthSearch,
                'school': SCHOOL.objects.get(emis=emis),
                
            }
            
            
            request.session['filter'] = json.dumps(request.GET)
            
            return render(request,template ,context)
        
        else:
            records = MonthlyRecord.objects.filter(pk=id)
            context = {
                'records':records,
                'monthSearch':True,
                'school': records.first().school,
                
            }
            
            template = render_block_to_string('Entry/partials/show.html', 'email', context)
            template += render_to_string('Entry/partials/options.html',{'records':records})
            return HttpResponse(template)
        
@login_required        
def delete_record(request, pk):
    
    record = MonthlyRecord.objects.get(pk=pk)
    record.delete()
    messages.success(request,"record deleted successfully")
    return hx_Redirect("entry:showRecordsFromSession")

@login_required        
def delete_record_from_clientSide(request, pk):
    
    record = MonthlyRecord.objects.get(pk=pk)
    record.delete()
    messages.success(request,"record deleted successfully")
    school = request.user.school or None
    return redirect(reverse_lazy("school:schoolProfile", kwargs={'slug':school.slug}))



"""
=== ========== === ========== === ===== PTC INFORMATION   ===== === ========== === ==========
"""
class PTC_INFORMATIONEntryView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        template = get_template(request, name='add', path="PtcInformation")
        record = MonthlyRecord.objects.get(pk=request.session['record'])
        nextDisabled = True
        form = PTC_InformationForm()
        
        # Fill form
        if PTC_Information.objects.filter(record=record).exists():
            return hx_Redirect("entry:schoolStockAdd")
            nextDisabled = False
            ptc_object = PTC_Information.objects.get(record=record)
            form= PTC_InformationForm(instance=ptc_object)
            
        
        # Check Prv Record
        currentPtcRecords = MonthlyRecord.objects.filter(school=record.school).order_by("-date")
        if len(currentPtcRecords) > 1:
            currentPtcRecords = currentPtcRecords[1]
        else:
            currentPtcRecords = currentPtcRecords.first()
            
        prevRecord = False
        if currentPtcRecords.ptcInfo.all().exists():
            prevRecord = True
        
        context = {
            'form': form,
            'current': '5',
            'nextDisabled': nextDisabled,
            'prevRecord': prevRecord
        }
        
        return render(request, template, context)
        
        
    def post(self, request):
        
        template = get_template(request, name='add', path="PtcInformation")
        record = MonthlyRecord.objects.get(pk=request.session['record'])
        form = PTC_InformationForm(data=request.POST)
        if form.is_valid():
            
            ptcInfo = form.save(commit=False)
            ptcInfo.record = record
            ptcInfo.save()
            
            return hx_Redirect("entry:schoolStockAdd")
       
        context = {
            'form': form,
            'current': '5',
            'nextDisabled': True
        }
       
        messages.error(request, "Please correct the error bellow")
        return render(request, template, context)


class PTC_INFOLISTView(LoginRequiredMixin,DetailView):
    model=PTC_Information
    context_object_name="record"
    def get_template_names(self, *args, **kwargs):
        return get_template(self.request, 'list', path="PtcInformation")
@login_required
def delete_ptcInfo(request, pk):

    if request.method == "DELETE":
        record = PTC_Information.objects.get(pk=pk)
        record.ptcInfo.delete()
        
        messages.success(request,"Ptc Information record deleted successfully")
        return hx_Redirect("entry:showRecordsFromSession")


@login_required
def ptcRecord_fill_from_prev(request):
    
    template = get_template(request, name='add', path="PtcInformation")
    record = MonthlyRecord.objects.get(pk=request.session['record'])
    # get prev
    prevRecord = MonthlyRecord.objects.filter(school=record.school).order_by("-date")
    if len(prevRecord) > 1:
        prevRecord = prevRecord[1]
    else:
        prevRecord = prevRecord.first()
    
    form = PTC_InformationForm()
    
    if 'prevMonth' in  request.GET.keys():
    
        if PTC_Information.objects.filter(record=prevRecord).exists():
            form= PTC_InformationForm(instance=prevRecord.ptcInfo.all().first())
           
   
    context =  {
        'form':form
                }
    
    template = render_block_to_string(template, 'form',context)
    
    return HttpResponse(template)