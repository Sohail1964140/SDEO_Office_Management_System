from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, UpdateView
from .models import (CHAIRMAN)
from .forms import (chairmanForm)
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
chairman Operations
"""

def get_template(request, template):
    
    if request.htmx:
        return f'core/chairman/partials/{template}'
    
    return f'core/chairman/{template}'


class chairmanAddView(LoginRequiredMixin,View):
    
    
    def get(self, request):
        
        context = {'form': chairmanForm(), 'heading':'Add New chairman'}
        template_name = get_template(request, 'add.html')
        return render(request, template_name, context)
    
    def post(self, request):
        
        form = chairmanForm(data=request.POST)
        if form.is_valid():
            
            chairman = form.save()    
            
            messages.success(request, f"{chairman} added successfully")
            form = chairmanForm()
        else:
            messages.error(request, "Please correct the Error Bellow")
        
        context = {'form': form}
        template_name = get_template(request, 'add.html')
        return render(request,template_name, context)
    
class chairmanListView(LoginRequiredMixin,ListView):
    
    model = CHAIRMAN
    context_object_name = 'chairmans'
    paginate_by = 10
    paginate_orphans = 2
    
    def get_template_names(self): return get_template(self.request, 'list.html')
    
    
    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(chairmanListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            
            self.kwargs['page'] = 1
            return super(chairmanListView, self).paginate_queryset(queryset, page_size)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isSearch"] = False
        return context
    


class chairmanSearchView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        
        
        page_number = request.GET.get('page', 1)
        query = request.GET.get('query')
        
        if query is None:
            query = ""
        
        chairmans = CHAIRMAN.objects.filter(name__istartswith=query).order_by('pk')
        paginator = Paginator(chairmans, per_page=10)
        
        
        page = paginator.get_page(page_number)
        
        context={
            
            'chairmans': page.object_list,
            'page_obj': page,
            'isSearch': True,
            'request':request
        
        }
        print(context)
        response = render_block_to_string('core/chairman/partials/list.html', 'table', context)
        
        
        return HttpResponse(response)
        

class chairmanUpdateView(LoginRequiredMixin,View):
    
        

    def get(self, request, name):
        
        chairman = get_object_or_404(CHAIRMAN, slug=name)
        form = chairmanForm(instance=chairman)
        context = {'form':form, 'heading':'Update CHAIRMAN','isUpdate':True, 'object': chairman}
        template_name = get_template(request, 'add.html')
        
        return render(request, template_name, context)
    
    def post(self, request, name):
        
        chairman = get_object_or_404(CHAIRMAN , slug=name)
        form = chairmanForm(instance=chairman, data=request.POST)
        
        if form.is_valid():
            
            chairman = form.save()
            messages.success(request, f'{chairman} Update Successfully')
        else:
            messages.error(request, 'Please correct the Error Bellow')
        
        context = {'form':form, 'heading':'Update chairman','isUpdate':True, 'object': chairman}
        template_name = get_template(request, 'add.html')
        
        return render(request,template_name, context)
    
        
class chairmanDeleteView(LoginRequiredMixin,View):
    
    def get(self, request, name):
       
        try:
            
            chairman = get_object_or_404(CHAIRMAN, slug=name)
            
            context = {'object': chairman, 'msg': f'Are you sure you want to delete  <strong> <i>{chairman.name}</i></strong>? This action cannot be undone.'}
            
            return render(request,get_template(request, 'delete.html'), context)
        

        except Http404:
            
            
            return render(request, 'utils/404.html') 
    
    
    
    def post(self, request, name):
        
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        input_name = request.POST.get('name')
        user = request.user
        chairman = get_object_or_404(CHAIRMAN, slug=name)
        
        
        if user.email == email:
            
            if check_password(password, user.password):
                
                if name ==slugify(input_name):
                    
                    chairman.delete()
                    messages.success(request, f'{chairman.name} deleted successfully')

                    context = {'isDeleted': True,'msg': f'{chairman.name} deleted Successfully'}
                    return render(request, get_template(request, 'delete.html'), context)
        
        
        messages.warning(request, "To ensure the security, please fill the given information")
        
        context = {
            'object':chairman,
            'msg': 'Please ensure that all information is entered correctly before submitting the form <br> Your security is our top priority'
                   
                   }
        return render(request, get_template(request, 'delete.html'), context)
    
    

