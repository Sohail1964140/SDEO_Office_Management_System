from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from openpyxl import Workbook
from xhtml2pdf import pisa
from io import BytesIO
from Apps.staff.models import TEACHER, CONTACT
from Apps.monthlyEntry.models import MonthlyRecord
from Apps.schools.models import SCHOOL
from Apps.core.models import CIRCLE, POST, UC
from django.conf import settings
from django.views.generic import TemplateView
from .resources import School_List, TEACHER_Govt_Election_Resource
from django.utils.timezone import now
from django.db.models import F, Q,Value, CharField
from django.db.models.functions import Concat
import pandas as pd
from pandas import DataFrame
from dateutil.relativedelta import relativedelta
from datetime import datetime
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

"""
Monthly Report
"""
class MonthlyReturnProFormaView(LoginRequiredMixin,View):
    
    
    def get(self, request, pk):
        
        
        record = MonthlyRecord.objects.filter(pk=pk).first()
        ptcInfo = record.ptcInfo.all().first()
        pdf = render_to_pdf('reports/record.html', {'record': record, 'ptcInfo':ptcInfo})
        
        return HttpResponse(pdf, content_type='application/pdf')

class DownloadMonthlyReturnProForma(LoginRequiredMixin,View):
    
    def get(self, request, pk):
        
        record = MonthlyRecord.objects.filter(pk=pk).first()
        pdf = render_to_pdf('reports/record.html', {'record': record})

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Proforma_%s.pdf" %(str(record.date))
        content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
     

"""
Load Reports Template
"""

class Report_Tempalte(LoginRequiredMixin,TemplateView):
    
    def get_template_names(self, *args, **kwargs):
        
        if self.request.htmx:
            return ["reports/partials/common.html"]
        
        return ['reports/common.html']

    def get_context_data(self, *args, **kwargs):
        
        context = super().get_context_data(*args, **kwargs)
        context['circles'] = CIRCLE.objects.all().order_by("pk")
        context['ucs'] = UC.objects.all().order_by("pk")
        context['posts'] = POST.objects.all().order_by("pk")
        context['schools'] = SCHOOL.objects.all().order_by("pk")
        return context

"""
School Reports
"""
class School_List_Report(LoginRequiredMixin,View):
    
    def get(self, request):
        
        if request.GET.get('custome'):
            
            schools = SCHOOL.objects.all()
            circleID = request.GET.get('circleDD')
            ucID = request.GET.get('ucDD')
            
            if circleID:
                schools = schools.filter(uc__circle__pk=circleID)
            if ucID:
                schools  = UC.objects.get(pk=ucID).schools.all()
            
        else:
            schools = SCHOOL.objects.all()
        
        school_list = School_List()
        dataset = school_list.export(schools)
        
        filename = request.GET.get('filename',f'all_school_list')
        format = request.GET.get('format', 'xls')
        
        if format == 'xls':
            response = HttpResponse(dataset.xls, content_type="application/vnd.ms-excel")
        elif format == 'csv':
            response = HttpResponse(dataset.csv, content_type="text/csv")
        
        if format == 'pdf':
            pdf = render_to_pdf('reports/schools/all_school_list.html',{'schools':schools})
            
            response = HttpResponse(pdf, content_type="application/pdf")
        
        
        response['Content-Disposition'] = f'attachment; filename="{filename}_{now().strftime("%H:%M:%S")}.{format}"'
        
        return response
    


"""
Teacher Reports
"""

@login_required
def list_of_teachers_for_govt_election(request):
    
    teachers = TEACHER.objects.annotate(t_post=Concat(F('post__name'),Value('  PBS-'),F('post__bps'),output_field=CharField()))
    

    
    teacher_list = []
    
    # print(CONTACT.objects.filter(teacher__pk=teachers[0].pk))
    
    for teacher in teachers:
        
        
        teacher_list.append({
            'School':teacher.school.name,
            'Name': teacher.name,
            'Designation':teacher.t_post,
            'Tehsile': teacher.school.uc.circle.name,
            'UC': teacher.school.uc.name,
            'Contact': '' if not  teacher.contacts.all().exists() else  teacher.contacts.all().first().contact
        })
    
    
    
    
    teacher_df = DataFrame(teacher_list)
    
    format = request.GET.get('format')
    filename = request.GET.get('filename', 'download')
    

    
    if format == 'pdf':
        
        pdf = render_to_pdf('reports/teachers/local_govt_election.html',{'teachers':teacher_list})
        
        response = HttpResponse(pdf,content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}_{now().strftime("%H:%M:%S")}.pdf"'
        return response
    
    if format == 'csv':
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}_{now().strftime("%H:%M:%S")}.{format}"'
        teacher_df.to_csv(path_or_buf=response, index=False)
        return response
        
    else:
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}_{now().strftime("%H:%M:%S")}.{format}"'
        teacher_df.to_excel(response, index=False)
        return response
    


"""
Teacher Custome Report
"""

def getHeading(columns: list)->list:
    heading = list()
    
    for column in columns:
        
        match column:
            
            case 'Accadqualification':
                
                heading.append('Accad Qualification')
                
            case 'Proffqualification':
                heading.append('Proff Qualification')
            case 'teacherFirstAppointment':
                heading.append('Year of Recruitment')
            case 'g_fund_no':
                
                heading.append('Govt Fund No')
            
            case 'personal_no':
                
                heading.append('Personal No')
                
            case 'post':
                heading.append('Designation')
            
            case 'personal_no':
                
                heading.append('Personal No')
            
            case 'dateOfTakingOverChargeInPresentSchool':
                
                heading.append('Date of taking over charge in present school')
            case 'dateOfTakingOverChargeOnPresentPost':
                
                heading.append('Date of taking over charge on present post')
            case _:
                heading.append(column)
    
    return heading
    
    

@login_required   
def list_of_teachers_Report(request):
    
    columns = request.GET.getlist('columns[]')
    teachers = TEACHER.objects.all()
    teacher_list = []
    format = request.GET.get('format')
    filename = request.GET.get('filename', 'download_Teachers')
    reportHeading = request.GET.get('reportHeading')
    reportSubHeading = request.GET.get('reportSubHeading')

    

    if 'schoolCB' in request.GET:
        teachers = teachers.filter(school__pk=request.GET.get('school') or 0) 
    
    elif 'ucCB' in request.GET:
        teachers = teachers.filter(school__uc__circle__pk=request.GET.get('uc') or 0) 
    
    elif 'circleCB' in request.GET:
        teachers = teachers.filter(school__uc__circle__pk=request.GET.get('circle') or 0) 
    
    if 'postCB' in request.GET:
        teachers = teachers.filter(post__pk=request.GET.get('post') or 0) 
        
    
    if 'experienceCB' in request.GET:
        filterYears = int(request.GET.get("year", 0))
        filter = request.GET.get("match", 'eq')
        
        for teacher in teachers:            
            experienceYears = relativedelta(datetime.today().date(), teacher.teacherFirstAppointment.dateOfFirstAppointment).years
            
            
            match filter:
                case 'eq':
                    if experienceYears == filterYears:
                        teacher_list.append(teacher)
                    
                case 'gt':
                    
                    if experienceYears > filterYears:
                        teacher_list.append(teacher)
                    
                case 'lt':
                    if experienceYears < filterYears:
                        teacher_list.append(teacher)
                case 'lte':
                    
                    if experienceYears <= filterYears:
                        teacher_list.append(teacher)
                        
                case 'gte':
                    
                    if experienceYears >= filterYears:
                        teacher_list.append(teacher)
            



        
    outFields = [
                 'school','post', 'contact', 'Proffqualification',
                 'Accadqualification','teacherFirstAppointment',
                 'district','tehsil','circle','uc','emis','level'
                 'gender',
                 ]
    
    if 'experienceCB' in request.GET:
        _teacher_list = teacher_list.copy()
        teacher_list.clear()
        
    else:
        _teacher_list = teachers
        teacher_list.clear()
        
        
    for teacher in _teacher_list:
        _teacher = {}
        
        for column in columns:
            if not column in outFields and not column == 'level':
                
                if column == 'gender':
                    _teacher[column] = 'Male' if teacher.gender == '1' else 'FeMale'
                else:
                       
                    _teacher[column] = getattr(teacher, column)
            
            else:
                
                match column:
                    
                    case 'school':
                        
                        _teacher[column] = teacher.school.name
                    
                    case  'post':
                        
                        _teacher[column] = f'{teacher.post.name} BPS-{teacher.post.bps}'

                    case 'contact':
                        
                        
                        _teacher[column] = '' if not  teacher.contacts.all().exists() else  teacher.contacts.all().first().contact
                        
                    case 'Proffqualification':
                        
                        _teacher[column] = ", ".join(name for name in teacher.Proffqualification.all().values_list('name', flat=True))
                    
                    case 'Accadqualification':
                        _teacher[column] = ", ".join(name for name in  teacher.Accadqualification.all().values_list('name', flat=True))
                    
                    case 'teacherFirstAppointment':
                        
                        _teacher[column] = teacher.teacherFirstAppointment.dateOfFirstAppointment

                    case 'district':
                        _teacher[column] = 'Swat'
                    case 'tehsil':
                        _teacher[column] = 'Matta'
                    case 'level':
                        _teacher[column] = 'Primary'
                    case 'gender':
                        _teacher[column] = 'Male' if teacher.gender == '0' else 'FeMale'
                    case 'circle':
                        _teacher[column] = teacher.school.uc.circle.name
                        
                    case 'emis':
                        _teacher[column] = teacher.school.emis
                        
                    case 'uc':
                        _teacher[column] = teacher.school.uc.name
                        
        teacher_list.append(_teacher)
        
    
    teacher_df = DataFrame(teacher_list)
    
    match format:
        
        case 'pdf':
            
            headings = getHeading(columns=columns)
            pdf = render_to_pdf('reports/teachers/custome.html', {'reportHeading': reportHeading,'reportSubHeading':reportSubHeading, 'teachers':teacher_list,'columns':columns, 'headings':headings, 'size': len(columns)})
            response = HttpResponse(pdf,content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}_{now().strftime("%H:%M:%S")}.pdf"'
            return response
        
        case  'csv':
            
             response = HttpResponse(content_type='text/csv')
             response['Content-Disposition'] = f'attachment; filename="{filename}_{now().strftime("%H:%M:%S")}.{format}"'
             teacher_df.to_csv(path_or_buf=response, index=False)
             return response
         
        case  _:
            
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{filename}_{now().strftime("%H:%M:%S")}.{format}"'
            teacher_df.to_excel(response, index=False)
            return response



'''
SEPARATE REPORTS
'''

@login_required
def showTeacherReport(request, pk):
    
    record = MonthlyRecord.objects.filter(pk=pk).first()
    # teachers = record.teachersRecords.all()

    pdf = render_to_pdf('reports/teachers/teacherMonthReocrd.html',{'record':record})
    
    response = HttpResponse(pdf,content_type='application/pdf')
    # response['Content-Disposition'] = f'attachment; filename="{filename}_{now().strftime("%H:%M:%S")}.pdf"'
    return response
    






@login_required
def showStaffReport(request, pk):
    
    record = MonthlyRecord.objects.filter(pk=pk).first()
    # teachers = record.teachersRecords.all()

    pdf = render_to_pdf('reports/teachers/staffRecord.html',{'record':record})
    
    response = HttpResponse(pdf,content_type='application/pdf')
    # response['Content-Disposition'] = f'attachment; filename="{filename}_{now().strftime("%H:%M:%S")}.pdf"'
    return response


@login_required
def showBuildingReport(request, pk):
    
    record = MonthlyRecord.objects.filter(pk=pk).first()
    pdf = render_to_pdf('reports/schools/schoolBuilding.html', {'record': record})
    
    return HttpResponse(pdf, content_type='application/pdf')


@login_required
def showStockReport(request, pk):
    
    record = MonthlyRecord.objects.filter(pk=pk).first()
    pdf = render_to_pdf('reports/schools/schoolStuck.html', {'record': record})
    
    return HttpResponse(pdf, content_type='application/pdf')


@login_required
def showPtcInformationReport(request, pk):
    
    record = MonthlyRecord.objects.filter(pk=pk).first()
    ptcInfo = record.ptcInfo.all().first()
    pdf = render_to_pdf('reports/schools/ptcInformation.html', {'record': record, 'ptcInfo':ptcInfo})
    
    return HttpResponse(pdf, content_type='application/pdf')




@login_required
def showStudentStrengthReport(request, pk):
    
    record = MonthlyRecord.objects.filter(pk=pk).first()
    pdf = render_to_pdf('reports/schools/studentStrength.html', {'record': record})
    
    return HttpResponse(pdf, content_type='application/pdf')