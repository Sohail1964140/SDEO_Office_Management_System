from .forms import UcForm
from .models import UC, CIRCLE
from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, CreateView
from django.http import Http404
from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator
from render_block import render_block_to_string
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
import json
from time import sleep
from django.contrib.auth.mixins import LoginRequiredMixin
"""
UC CREATE VIEW
"""
class UcCreateView(LoginRequiredMixin,CreateView):
    
    success_url = None
    model = UC
    template_name = "core/uc/uc_add.html"
    form_class = UcForm
    
    def get_template_names(self):
        
        if self.request.htmx:
            self.template_name="core/uc/partials/uc_add.html"

        return self.template_name
    
    def get_success_url(self): return None

    def get_context_data(self):
        
        context = super(UcCreateView, self).get_context_data()
        context['heading'] = "Add New Uc"
        return context
    
    def post(self, request, *args, **kwargs):
        
        form = self.form_class(data=request.POST)
        
        if form.is_valid():
            
            uc = form.save()
            messages.success(request, f"New Uc `{uc}` Added Successfully")
            self.template_name = self.get_template_names()
            context = {'heading':'Add New Uc', 'form': self.form_class}
            return render(request, self.template_name, context)
        
        messages.error(request, "Please correct error bellow")
        self.template_name = self.get_template_names()
        context = {'heading':'Add New Uc', 'form': form}
        return render(request, self.template_name, context)
    
    
    
    
"""
UC LIST VIEW
"""
class UcListView(LoginRequiredMixin,ListView):
    
    model = UC
    template_name = "core/uc/uc_list.html"
    context_object_name = 'ucs'
    paginate_by = 10
    paginate_orphans = 2
    
    def get_template_names(self):
        if self.request.htmx:
            
            self.template_name="core/uc/partials/uc_list.html"
        
        return self.template_name
    

    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(UcListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            
            self.kwargs['page'] = 1
            return super(UcListView, self).paginate_queryset(queryset, page_size)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isSearch"] = False
        context['circles'] = CIRCLE.objects.all().order_by('pk')
        return context
    
    
"""
UC LIST VIEW
"""

class UcSearch(LoginRequiredMixin,View):
    
    
    def get(self, request):
        

        page_number = request.GET.get('page', 1)
        query = json.loads(request.GET.get('query'))
        
        Ucs = UC.objects.all()
        
        if query.get("search"):
            
            
            
            Ucs = Ucs.filter(name__istartswith=query.get('search'))
        
        if query.get("circle"):
            
            circle = CIRCLE.objects.get(pk=query.get('circle'))
            
            Ucs = Ucs.filter(circle=circle)
        
        
        paginator = Paginator(Ucs, per_page=10)
        
        page = paginator.get_page(page_number)

        data={
            
            'ucs': paginator.object_list,
            'page_obj': page,
            'isSearch': True,
            'circles':CIRCLE.objects.all().order_by('pk'),
            'request':request
        
        }
        response = render_block_to_string(template_name='core/uc/partials/uc_list.html', block_name='table', context=data)
        
        

        return HttpResponse(response)
    


"""
UC UPDATE VIEW
"""

class UcUpdateView(LoginRequiredMixin,View):
    
    
    def get(self, request, name):
        
        uc = get_object_or_404(UC, name=name)
        form = UcForm(instance=uc)
        template_name = "core/uc/uc_add.html"
        
        if request.htmx:
            
            template_name = "core/uc/partials/uc_add.html"
        
        
        context = {'form':form, 'heading':'Update Uc','isUpdate':True, 'object': uc}
        
        
        return render(request, template_name, context)
    
    def post(self, request, name):
        
        uc = get_object_or_404(UC, name=name)
        form = UcForm(instance=uc,data=request.POST)
        template_name = "core/uc/partials/uc_add.html"
        
        if form.is_valid():
            
            uc = form.save()
            messages.success(request, f'{uc} Update Successfully')
        else:
            messages.error(request, 'Please correct the Error Bellow')
        
        
        context = {'form':form, 'heading':'Update Uc','isUpdate':True, 'object': uc}
        
        return render(request, template_name, context)


"""
UC DELETE VIEW
"""

class UcDeleteView(LoginRequiredMixin,View):
    
    
    def get(self, request, name):
       
        try:
            template_name = "core/uc/delete.html"
            uc = get_object_or_404(UC, name=name)
            
            if request.htmx:
                
                template_name = "core/uc/partials/delete.html"
            
            context = {'object': uc, 'msg': f'Are you sure you want to delete  <strong> <i>{uc.name}</i></strong>? This action cannot be undone.'}
            
            
            return render(request, template_name, context)
        

        except Http404:
            
            
            return render(request, 'utils/404.html') 
    
    
    
    def post(self, request, name):
        
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        input_name = request.POST.get('name')
        template_name = "core/uc/delete.html"
        user = request.user
        uc = get_object_or_404(UC, name=name)
        
        if request.htmx:
            template_name = "core/uc/partials/delete.html"
        

        if user.email == email:
            
            if check_password(password, user.password):
                
                if name == input_name:
                    
                    uc.delete()
                    messages.success(request, f'{uc.name} deleted successfully')

                    context = {'isDeleted': True,'msg': f'{uc.name} deleted Successfully'}
                    return render(request, template_name, context)
        
        
        messages.warning(request, "To ensure the security, please fill the given information")
        
        context = {
            'object':uc,
            'msg': 'Please ensure that all information is entered correctly before submitting the form <br> Your security is our top priority'
                   
                   }
        return render(request, template_name, context)


