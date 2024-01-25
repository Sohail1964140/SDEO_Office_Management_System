from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, UpdateView
from .models import (BANK)
from .forms import (bankForm)
from django.contrib import messages
from django.http import Http404
from render_block import render_block_to_string
from django.core.paginator import Paginator
from django.contrib.auth.hashers import check_password
from django_htmx.http import trigger_client_event
# Create your views here.
from time import sleep
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
"""
BANK Operations
"""

def get_template(request, template):
    
    if request.htmx:
        return f'core/bank/partials/{template}'
    
    return f'core/bank/{template}'


class bankAddView(LoginRequiredMixin,View):
    
    
    def get(self, request):
        
        context = {'form': bankForm(), 'heading':'Add New bank'}
        template_name = get_template(request, 'add.html')
        return render(self.request, template_name, context)
    
    def post(self, request):
        
        form = bankForm(data=request.POST)
        if form.is_valid():
            
            bank = form.save()    
            
            messages.success(request, f"{bank} added successfully")
            form = bankForm()
        else:
            messages.error(request, "Please correct the Error Bellow")
        
        context = {'form': form}
        template_name = get_template(request, 'add.html')
        return render(request,template_name, context)
    
class bankListView(LoginRequiredMixin,ListView):
    
    model = BANK
    context_object_name = 'banks'
    paginate_by = 10
    paginate_orphans = 2
    
    def get_template_names(self): return get_template(self.request, 'list.html')
    
    
    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(bankListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            
            self.kwargs['page'] = 1
            return super(bankListView, self).paginate_queryset(queryset, page_size)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isSearch"] = False
        return context
    


class bankSearchView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        page_number = request.GET.get('page', 1)
        query = request.GET.get('query')
        
        if query is None:
            query = ""
        
        circles = BANK.objects.filter(name__istartswith=query).order_by('pk')
        paginator = Paginator(circles, per_page=10)
        
        
        
        page = paginator.get_page(page_number)
        
        context={
            
            'circles': page.object_list,
            'page_obj': page,
            'isSearch': True,
            'request':request
        
        }
        
        response = render_block_to_string('core/bank/partials/list.html', 'table', context)
        
        
        return HttpResponse(response)
        

class bankUpdateView(LoginRequiredMixin,View):
    
        

    def get(self, request, name):
        
        bank = get_object_or_404(BANK, slug=name)
        form = bankForm(instance=bank)
        context = {'form':form, 'heading':'Update bank','isUpdate':True, 'object': bank}
        template_name = get_template(request, 'add.html')
        
        return render(request, template_name, context)
    
    def post(self, request, name):
        
        bank = get_object_or_404(BANK , slug=name)
        form = bankForm(instance=bank, data=request.POST)
        
        if form.is_valid():
            
            bank = form.save()
            messages.success(request, f'{bank} Update Successfully')
        else:
            messages.error(request, 'Please correct the Error Bellow')
        
        context = {'form':form, 'heading':'Update BANK','isUpdate':True, 'object': bank}
        template_name = get_template(request, 'add.html')
        
        return render(request,template_name, context)
    
        
class bankDeleteView(LoginRequiredMixin,View):
    
    def get(self, request, name):
       
        try:
            
            bank = get_object_or_404(BANK, slug=name)
            
            context = {'object': bank, 'msg': f'Are you sure you want to delete  <strong> <i>{bank.name}</i></strong>? This action cannot be undone.'}
            
            return render(request,get_template(request, 'delete.html'), context)
        

        except Http404:
            
            
            return render(request, 'utils/404.html') 
    
    
    
    def post(self, request, name):
        
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        input_name = request.POST.get('name')
        user = request.user
        bank = get_object_or_404(BANK, slug=name)
        
        
        if user.email == email:
            
            if check_password(password, user.password):
                
                if name ==slugify(input_name):
                    
                    bank.delete()
                    messages.success(request, f'{bank.name} deleted successfully')

                    context = {'isDeleted': True,'msg': f'{bank.name} deleted Successfully'}
                    return render(request, get_template(request, 'delete.html'), context)
        
        
        messages.warning(request, "To ensure the security, please fill the given information")
        
        context = {
            'object':bank,
            'msg': 'Please ensure that all information is entered correctly before submitting the form <br> Your security is our top priority'
                   
                   }
        return render(request, get_template(request, 'delete.html'), context)
    
    

