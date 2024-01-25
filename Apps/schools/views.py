from datetime import datetime
from django.shortcuts import render, HttpResponse, get_object_or_404

from Apps.monthlyEntry.models import MonthlyRecord
from Apps.monthlyEntry.views import get_redirect_url, get_year_months
from .forms import SchoolForm
from .models import SCHOOL
from Apps.core.models import UC, hx_Redirect
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
from django.http import Http404
from render_block import render_block_to_string
from django.core.paginator import Paginator
from django.contrib.auth.hashers import check_password
from django.db.models import Q
import json
from time import sleep
from django.template.loader import get_template, render_to_string
from django.urls import reverse_lazy as _
from django_htmx.http import HttpResponseClientRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# Create your views here.


def get_template(request, name):
    
    template = f'school/{name}.html'
    
    if request.htmx:
        template  = f'school/partials/{name}.html'

    return template
    



# School Crate View
class SchoolCreateView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        context = {'form': SchoolForm(), 'heading':'Add New School'}
        template = get_template(request, 'school_add')
        return render(request, template, context)
    
    
    def post(self, request):
        
        form = SchoolForm(data=request.POST)
        if form.is_valid():
            
            school = form.save()    
            
            messages.success(request, f"{school} added successfully")
            form = SchoolForm()
        else:
            messages.error(request, "Please correct the Error Bellow")
        
        context = {'form': form}
        template_name = get_template(request, 'school_add')
        return render(request,template_name, context)


"""
School List View
"""
class SchoolListView(LoginRequiredMixin,ListView):
    
    model = SCHOOL
    context_object_name = 'schools'
    paginate_by = 10
    paginate_orphans = 2
    
    def get_template_names(self): return get_template(self.request, 'school_list')
    
    
    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(SchoolListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            
            self.kwargs['page'] = 1
            return super(SchoolListView, self).paginate_queryset(queryset, page_size)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ucs'] =UC.objects.all().order_by('pk')
        context["isSearch"] = False
        return context


"""
School Search View
"""

class SchoolSearchView(LoginRequiredMixin,View):
    
    
    def get(self, request):
        

        page_number = request.GET.get('page', 1)
        query = json.loads(request.GET.get('query'))
        
        schools = SCHOOL.objects.all()
        
        if query.get("search"):
            schools = schools.filter(Q(name__istartswith=query.get('search')) | Q(emis__istartswith=query.get('search')) | Q(user__email__istartswith=query.get('search')))
        
        if query.get("uc"):
            
            uc = UC.objects.get(pk=query.get('uc'))
            schools = schools.filter(uc=uc)
        
        
        paginator = Paginator(schools.order_by('pk'), per_page=10)
        
        page = paginator.get_page(page_number)

        context={
            
            'schools': page.object_list,
            'page_obj': page,
            'isSearch': True,
            'ucs':UC.objects.all().order_by('pk'),
            'request':request
        
        }
        
        response = render_block_to_string('school/partials/school_list.html', 'table', context)
        return HttpResponse(response)
    
    
    
"""
School UPDATE VIEW
"""

class SchoolUpdateView(LoginRequiredMixin,View):
    
    
    def get(self, request, slug):
        
        school = get_object_or_404(SCHOOL, slug=slug)
        form = SchoolForm(instance=school)
        template_name = get_template(request, 'school_add')
        context = {'form':form, 'heading':'Update School','isUpdate':True, 'object': school}
        return render(request, template_name, context)
    
    def post(self, request, slug):
        
        school = get_object_or_404(SCHOOL, slug=slug)
        form = SchoolForm(instance=school,data=request.POST)
        template_name = get_template(request, 'school_add')
        sleep(3)
        if form.is_valid():
            school = form.save()
            messages.success(request, f'{school} Updated Successfully')
        else:
            messages.error(request, 'Please correct the Error Bellow')
        
        
        context = {'form':form, 'heading':'Update School','isUpdate':True, 'object': school}
        
        return render(request, template_name, context)



"""
SCHOOL DELETE VIEW
"""

class SchoolDeleteView(LoginRequiredMixin,View):
    
    
    def get(self, request, slug):
       
        try:
            school = get_object_or_404(SCHOOL, slug=slug)
            
            context = {'object': school, 'msg': f'Are you sure you want to delete  <strong> <i>{school.name}</i></strong>? This action cannot be undone.'}
            
            template_name = get_template(request, 'school_delete')
            return render(request, template_name, context)
        

        except Http404:
            
            
            return render(request, 'utils/404.html') 
    
    
    
    def post(self, request, slug):
        
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        input_name = request.POST.get('name')
        template_name = get_template(request, 'school_delete')
        user = request.user
        school = get_object_or_404(SCHOOL, slug=slug)
        
        
        if user.email == email:
            
            if check_password(password, user.password):
                
                if school.name == input_name:
                    
                    school.delete()
                    messages.success(request, f'{school.name} deleted successfully')

                    context = {'isDeleted': True,'msg': f'{school.name} deleted Successfully'}
                    return render(request, template_name, context)
        
        
        messages.warning(request, "To ensure the security, please fill the given information")
        
        context = {
            'object':school,
            'msg': 'Please ensure that all information is entered correctly before submitting the form <br> Your security is our top priority'
                   
                   }
        return render(request, template_name, context)






"""
SCHOOL PROFILE PAGE
"""

@login_required
def get_Records(request, pk):
    records = MonthlyRecord.objects.filter(pk=pk)
    context = {
        'records':records,
        'monthSearch':True,
        'school': records.first().school if records.first() else None,
        
    }
    
    template = render_block_to_string('school/partials/school_profile.html', 'email', context)
    template += render_to_string('Entry/partials/options.html',{'records':records})
    return HttpResponse(template)

@login_required
def add_Record(request, pk):
    
    school = SCHOOL.objects.get(pk=pk)
    date = datetime.strptime(request.GET.get('date'), "%m/%d/%Y")
    
    record = MonthlyRecord.objects.filter(
                                        Q(date__year = date.year) & 
                                        Q(date__month=date.month) &
                                        Q(school__pk=school.pk)
                                            )
    if record.exists():
        
        url = get_redirect_url(record=record.first())['url']
        
        if url is None:
            messages.info(request, "Entry for this month is already done")
            return hx_Redirect("core:message")

        request.session['record'] = record.first().pk
        return HttpResponseClientRedirect(_(url))


    record = MonthlyRecord.objects.create(date=date, school=school)
    request.session['record'] = record.pk
    request.session['fromProfile'] = True
    return HttpResponseClientRedirect(_("entry:teacherMonthlyAdd"))



class SchoolProfilePage(LoginRequiredMixin,View):
    
    def get(self, request, slug):
        
        school = SCHOOL.objects.get(slug=slug)
        user = school.user
        records = MonthlyRecord.objects.filter(school=school)
        monthSearch = False
            
        context = {
            'dates': get_year_months(records=records).get('dates'),
            'records':records,
            'recordList': get_year_months(records=records).get('recordList'),
            'monthSearch':monthSearch,
            'school': school,
            
        }
        
        
        
        return render(request, get_template(request, 'school_profile'), context)